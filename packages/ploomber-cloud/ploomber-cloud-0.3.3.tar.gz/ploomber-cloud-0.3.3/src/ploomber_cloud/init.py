import os
from pathlib import Path
import click
import re
from typing import Callable, Any

from ploomber_cloud.util import spinner, write_project_to_disk
from ploomber_cloud.models import AuthCompatibleFeatures
from ploomber_core.exceptions import modify_exceptions

from ploomber_cloud.exceptions import BasePloomberCloudException
from ploomber_cloud import api

from ploomber_cloud.constants import (
    VALID_PROJECT_TYPES,
    VALID_DOCKER_PROJECT_TYPES,
    RETAINED_RESOURCES_WARNING,
    CONFIGURE_RESOURCES_MESSAGE,
    RETAINED_LABELS_WARNING,
)
from ploomber_cloud.config import PloomberCloudConfig, path_to_config
from ploomber_cloud.github import display_github_workflow_info_message
from ploomber_cloud._telemetry import telemetry
from ploomber_cloud.util import pretty_print, get_project_details_mappings


def _check_imports_for_project_type(types):
    """Search app.py for imports to infer project type"""
    if not Path("app.py").exists():
        return None

    text = Path("app.py").read_text()
    for proj in types:
        regex_import = r"\bimport " + proj + r"\b"
        regex_from_import = r"\bfrom " + proj + r" import\b"
        if re.findall(regex_import, text) or re.findall(regex_from_import, text):
            return proj

    return None


def _warn_if_auth(project_info: dict):
    """
    Warns the user if authentication is present on the current project.
    """
    map_feature_to_job_auth_info = {
        AuthCompatibleFeatures.ANALYTICS: "auth_analytics_enabled",
        AuthCompatibleFeatures.MAIN_APP: "auth_enabled",
    }
    map_auth_type_to_msg: dict[AuthCompatibleFeatures, str] = {
        AuthCompatibleFeatures.ANALYTICS: "WARNING: Project has "
        "authentication enabled for analytics.\n"
        "Please overwrite credentials with the 'ploomber-cloud auth \
        --add --overwrite' command",
        AuthCompatibleFeatures.MAIN_APP: "WARNING: Project has authentication "
        "enabled for the main application.\n"
        "Please overwrite credentials with the 'ploomber-cloud auth \
        --add --overwrite' command",
    }
    for auth_type in AuthCompatibleFeatures:
        if project_info.get("jobs", None) and project_info["jobs"][0].get(
            map_feature_to_job_auth_info[auth_type], None
        ):
            click.secho(map_auth_type_to_msg[auth_type], fg="yellow")


def _infer_project_type():
    """Infer project type based on the existing files in the current directory"""
    native_type = _check_imports_for_project_type(sorted(list(VALID_PROJECT_TYPES)))
    docker_type = _check_imports_for_project_type(
        sorted(list(VALID_DOCKER_PROJECT_TYPES))
    )
    found_dockerfile = Path("Dockerfile").exists()

    if docker_type:
        click.echo(
            f"This looks like a {docker_type.capitalize()} project, \
which is supported via Docker."
        )
        if not found_dockerfile:
            click.secho(
                f"Your app is missing a Dockerfile. To learn more, \
go to: https://docs.cloud.ploomber.io/en/latest/apps/{docker_type}.html",
                fg="yellow",
            )
        return "docker"
    elif found_dockerfile:
        return "docker"
    elif Path("app.R").exists():
        return "shiny-r"
    elif Path("app.ipynb").exists():
        return "voila"
    elif native_type:
        return native_type
    else:
        return None


def _prompt_for_project_type(prefix=None):
    """Prompt the user for a project type"""
    prefix = prefix or ""
    click.echo(f"{prefix}Please specify one of: " f"{', '.join(VALID_PROJECT_TYPES)}")

    return click.prompt(
        "Project type",
        type=click.Choice(VALID_PROJECT_TYPES),
        show_choices=False,
    )


def _init_from_existing(only_config: bool = False) -> None:
    """
    Initialize a local project from an existing cloud project.
    Params:
    _______
    - only_config: Optional[bool]
        If True, download only the configuration.
        If False, download both configuration and code.
        Defaults to False.
    """
    click.echo("Initializing from existing project...")
    client = api.PloomberCloudClient()

    # Get user's available projects
    all_projects = client.get_projects()["projects"]

    display_id_lookup, name_id_lookup = get_project_details_mappings(all_projects)

    project_choices = list(display_id_lookup.keys())
    if len(project_choices) == 0:
        click.echo("You have no existing projects. Initialize without --from-existing.")
        return

    project_choices.append("exit")
    prompt = ["These are your existing projects, choose the one you're configuring:\n"]
    for i, item in enumerate(project_choices):
        prompt.append(f"  {i + 1}. {item}\n")
    prompt_str = "".join(prompt)

    # Prompt user for choice of existing project
    while True:
        choice = click.prompt(prompt_str, type=str)
        # Case: user enters number
        if choice.isnumeric() and 0 < int(choice) <= len(project_choices):
            choice = project_choices[int(choice) - 1]
            # get original project ID for choice
            if choice in display_id_lookup:
                choice = display_id_lookup[choice]
            break
        # Case: user entered ID as displayed.
        # Get original project ID if any
        elif choice in display_id_lookup:
            choice = display_id_lookup[choice]
            break
        # Case: user enters the custom name of project
        elif choice in name_id_lookup:
            choice = name_id_lookup[choice]
            break
        # Case: choice is original project ID
        # of project with custom name
        elif choice in list(display_id_lookup.values()):
            break
        else:  # Case: user enters invalid
            click.echo("Please enter a valid choice.")

    # Allow user to exit menu without init
    if choice == "exit":
        click.echo("Exited.")
        return

    # Call API to get project type
    click.echo(f"Configuring project with id '{choice}'.")
    config_json = {"id": choice}
    project_info = client.get_project_by_id(config_json["id"])

    # Send a warning if a type of authentication is enabled
    _warn_if_auth(project_info)

    config_json["type"] = project_info["type"]
    if "labels" in project_info:
        config_json["labels"] = project_info["labels"]
    if "jobs" in project_info and len(project_info["jobs"]) > 0:
        cpu, ram, gpu = (
            float(project_info["jobs"][0]["cpu"]),
            int(float(project_info["jobs"][0]["ram"])),
            int(float(project_info["jobs"][0]["gpu"])),
        )
        config_json["resources"] = {"cpu": cpu, "ram": ram, "gpu": gpu}
        click.echo(RETAINED_RESOURCES_WARNING.format(cpu=cpu, ram=ram, gpu=gpu))

    if only_config:
        # Write id and type to ploomber-cloud.json
        config = PloomberCloudConfig()
        config.dump(config_json)
        click.echo(f"Your app {config_json['id']!r} has been configured successfully!")
    else:
        # Prompt user for download directory
        default_dir = f"./{choice}"
        download_dir = click.prompt(
            "Enter the directory to download the project", default=default_dir, type=str
        )
        # Convert to full path for internal use
        download_dir = os.path.abspath(download_dir)

        # Download and write files and config to the chosen directory
        with path_to_config(download_dir):
            with spinner(f"Downloading {choice}"):

                write_project_to_disk(client.get_project_files(choice), download_dir)
                config = PloomberCloudConfig()
                config.dump(config_json)
        click.echo(
            f"Your project {config_json['id']!r} has been downloaded successfully \
 in {download_dir}!"
        )

    display_github_workflow_info_message()


########################################################################
# This code is used to retain parts of the config when re-initializing #
########################################################################

FIELDS_TO_RETAIN = [
    "resources",
    "labels",
    "authentication",
    "authentication_analytics",
]


def _resource_msg(val: dict) -> str:
    return RETAINED_RESOURCES_WARNING.format(
        cpu=val["cpu"], ram=val["ram"], gpu=val["gpu"]
    )


def _labels_msg(val: list) -> str:
    return RETAINED_LABELS_WARNING.format(labels=pretty_print(val))


def _authentication_msg(val: dict) -> str:
    return "Retained authentication information."


def _authentication_analytics_msg(val: dict) -> str:
    return "Retained authentication information for analytics."


map_field_to_message: dict[str, Callable[[Any], str]] = {
    "resources": _resource_msg,
    "labels": _labels_msg,
    "authentication": _authentication_msg,
    "authentication_analytics": _authentication_analytics_msg,
}


@modify_exceptions
@telemetry.log_call(log_args=True)
def init(from_existing, force, only_config=True, project_type=None, verbose=True):
    """Initialize a project"""
    config = PloomberCloudConfig()

    retained_fields = {}

    if config.exists() and not force:
        config.load()
        raise BasePloomberCloudException(
            f"Project already initialized with id: {config.data['id']}. "
            "Run 'ploomber-cloud deploy' to deploy your project. "
            "To track its progress, add the --watch flag."
        )
    else:
        if from_existing:
            _init_from_existing(only_config)
            return

        if force:
            click.echo("Re-initializing project...")
            if config.exists():
                config.load()
                for field in FIELDS_TO_RETAIN:
                    if field in config.data:
                        retained_fields[field] = config.data[field]
        else:
            click.echo("Initializing new project...")

        if project_type is None:
            project_type = _infer_project_type()

            if project_type is None:
                project_type = _prompt_for_project_type(
                    prefix="Could not infer project type. "
                )
            else:
                click.echo(f"Inferred project type: {project_type!r}")
                correct_project_type = click.confirm("Is this correct?", default=True)

                if not correct_project_type:
                    project_type = _prompt_for_project_type()

        client = api.PloomberCloudClient()
        output = client.create(project_type=project_type)

        # retain appropriate config fields
        for field, value in retained_fields.items():
            output[field] = value
            if verbose:
                click.echo(map_field_to_message[field](value))

        config.dump(output)
        click.echo(f"Your app {output['id']!r} has been configured successfully!")

        if verbose and not force:
            click.echo(f"{CONFIGURE_RESOURCES_MESSAGE}")

        if verbose:
            display_github_workflow_info_message()
