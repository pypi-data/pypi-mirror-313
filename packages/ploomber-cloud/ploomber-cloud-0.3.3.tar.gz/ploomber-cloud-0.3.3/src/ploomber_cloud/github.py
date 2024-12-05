from pathlib import Path
import click
import requests
import json
from ploomber_core.exceptions import modify_exceptions

from ploomber_cloud import api
from ploomber_cloud.config import PloomberCloudConfig
from ploomber_cloud.exceptions import (
    BasePloomberCloudException,
    InvalidPloomberConfigException,
)
from ploomber_cloud._telemetry import telemetry
from ploomber_cloud.util import (
    fetch_previously_used_secret,
    show_github_env_var_setup_guide,
)
from ploomber_cloud.zip_ import _load_env_file_contents

GITHUB_DOCS_URL = "https://docs.cloud.ploomber.io/en/latest/user-guide/github.html"


def fetch_workflow_template_from_github():
    """Function to fetch the template GitHub workflow file"""
    yaml_file_url = "https://raw.githubusercontent.com/ploomber/cloud-template/main/.github/workflows/ploomber-cloud.yaml"  # noqa

    response = requests.get(yaml_file_url)

    if response.status_code == 200:
        return response.content
    else:
        raise BasePloomberCloudException(
            "Failed to fetch GitHub workflow template. Please refer: "
            f"{GITHUB_DOCS_URL}"
        )


def _workflow_add_config_secret(file_path):
    """
    Add environment secrets from the current config
    to a specific job's deploy action.

    Rely on finding the `PLOOMBER_CLOUD_KEY: ...` in the workflow file
    since we want to keep the comments as a way to educate the user

    Parameters
    ----------
    file_path: str
        The location of the ploomber workflow YAML

    Returns
    ---------
    None
    """
    try:
        config = PloomberCloudConfig()
        config.load()
        secret_names = config.data.get("secret-keys", [])
        if not secret_names:
            return

        with open(file_path, "r") as file:
            lines = file.readlines()

        ploomber_cloud_key_index = None
        for i, line in enumerate(lines):
            if "PLOOMBER_CLOUD_KEY:" in line:
                ploomber_cloud_key_index = i
                break

        if ploomber_cloud_key_index is None:
            raise ValueError("Could not find PLOOMBER_CLOUD_KEY in the workflow file")

        indent = " " * (
            len(lines[ploomber_cloud_key_index])
            - len(lines[ploomber_cloud_key_index].lstrip())
        )

        for secret_name in secret_names:
            new_line = f"{indent}{secret_name}: ${{{{ secrets.{secret_name} }}}}\n"
            lines.insert(ploomber_cloud_key_index + 1, new_line)
            ploomber_cloud_key_index += 1

        with open(file_path, "w") as file:
            file.writelines(lines)

    except InvalidPloomberConfigException:
        click.echo("No ploomber config file found - Skipping adding secrets")
        return  # No config file
    except Exception as e:
        click.secho(f"Error modifying workflow file: {e}", fg="yellow")
        click.secho(
            f"Please add the value manually. Check the documentation at {GITHUB_DOCS_URL} for instructions on how to set up GitHub secrets.",  # noqa
            fg="yellow",
        )


def _create_github_workflow_file():
    """Function to create a local copy of the GitHub
    workflow template"""

    file_path = "./.github/workflows/ploomber-cloud.yaml"

    content = fetch_workflow_template_from_github()
    with open(file_path, "wb") as file:
        file.write(content)

    # Add all secret in the config file to the pipeline
    _workflow_add_config_secret(file_path)

    click.echo(
        "'ploomber-cloud.yaml' file created in the path "
        ".github/workflows.\nPlease add, commit and push "
        "this file along with the 'ploomber-cloud.json' "
        "file to trigger an action.\nFor details on "
        "configuring a GitHub secret please refer: "
        f"{GITHUB_DOCS_URL}"
    )


def _warning_pipeline_missing_secret():
    """Warn the user if some secrets will be missing in the CI pipeline."""
    try:
        client = api.PloomberCloudClient()
        config = PloomberCloudConfig()
        config.load()
        project_id = config.data["id"]

        # Fetch previously set secrets
        remote_secrets = set(fetch_previously_used_secret(client, project_id))
        env_contents = _load_env_file_contents(verbose=False)

        # Get the current .env secrets
        dotenv_secrets = set()
        if env_contents:
            dotenv_secrets = {item["key"] for item in json.loads(env_contents)}

        # Check if they are all in the ploomber-config.json
        all_secrets = remote_secrets.union(dotenv_secrets)
        config_secrets = set(config.data.get("secret-keys", []))
        missing_secrets = all_secrets - config_secrets

        # Ask the user if we should add them for him
        if missing_secrets:
            msg = (
                "The following secrets are not in your config file: "
                f"{', '.join(missing_secrets)}. "
            )
            click.secho(msg, fg="yellow")
            add_missing_secrets = click.confirm(
                "Do you want to add them so the CI will deploy with them?", default=True
            )
            if add_missing_secrets:
                show_github_env_var_setup_guide()
                config["secret-keys"] = list(config_secrets.union(missing_secrets))
                click.echo("Configuration updated with new secrets.")
        else:
            click.echo("All secrets are properly configured.")
    except InvalidPloomberConfigException:
        return  # No config file


def _workflow_file_exists():
    """Function to check if GitHub workflow file
    is present in repository"""
    return Path(".github", "workflows", "ploomber-cloud.yaml").exists()


def _workflow_needs_update():
    """Function to check if the GitHub workflow
    file needs to be updated with the latest template"""
    if _workflow_file_exists():
        latest_workflow_template = fetch_workflow_template_from_github()
        # Check if the workflow template has been updated
        if (
            Path(".github", "workflows", "ploomber-cloud.yaml").read_text().strip()
            != latest_workflow_template.decode("utf-8").strip()
        ):
            return True
    return False


def display_github_workflow_info_message():
    """Display informative messages on creation
    or updation of GitHub workflow file"""
    if Path(".git").is_dir():
        workflow_message = (
            f"To learn more about GitHub actions refer: {GITHUB_DOCS_URL}"
        )
        if _workflow_needs_update():
            click.echo(
                ".github/workflows/ploomber-cloud.yaml seems outdated. "
                "You may update it by running 'ploomber-cloud github'.\n"
                f"{workflow_message}"
            )

        elif _workflow_file_exists() is False:
            click.echo(
                "You may create a GitHub workflow file for "
                "deploying your application by running 'ploomber-cloud github'.\n"
                f"{workflow_message}"
            )


@modify_exceptions
@telemetry.log_call()
def github():
    """Create or update GitHub workflow file ploomber-cloud.yaml"""
    if Path(".git").is_dir():
        if Path(".github", "workflows", "ploomber-cloud.yaml").exists():
            if _workflow_needs_update():
                confirm_msg = (
                    "Please confirm that you want to update the GitHub workflow file"
                )
            else:
                click.echo("Workflow file is up-to-date.")
                return
        else:
            confirm_msg = (
                "Please confirm that you want to generate a GitHub workflow file"
            )
        create_github_action = click.confirm(confirm_msg, default=True)
        if create_github_action:
            _warning_pipeline_missing_secret()
            Path(".github", "workflows").mkdir(exist_ok=True, parents=True)
            _create_github_workflow_file()
    else:
        raise BasePloomberCloudException(
            "Expected a .git/ directory in the current working "
            "directory. Run this from the repository root directory."
        )
