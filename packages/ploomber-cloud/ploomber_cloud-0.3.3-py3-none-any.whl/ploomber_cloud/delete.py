import click
from pathlib import Path

from ploomber_cloud import api, io
from ploomber_cloud.config import PloomberCloudConfig
from ploomber_cloud.util import get_project_details_mappings
from ploomber_cloud.exceptions import PloomberCloudRuntimeException


def _find_project_id():
    """Parse config file for project ID"""
    config = PloomberCloudConfig()
    config.load()
    data = config.data
    return data["id"]


def _remove_config_file():
    """Remove the config file"""
    if Path("ploomber-cloud.json").exists():
        Path("ploomber-cloud.json").unlink()


def delete(project_id=None):
    """Delete an application"""
    if not project_id:
        project_id = _find_project_id()
    client = api.PloomberCloudClient()

    try:
        client.delete(project_id=project_id)
    except Exception as e:
        raise PloomberCloudRuntimeException(
            f"Error deleting project {project_id}",
        ) from e

    _remove_config_file()

    click.echo(f"Project {project_id} has been successfully deleted.")


def is_valid_confirmation(value):
    if value in ["delete all", "N", "n"]:
        return io.ValidationResult(
            is_valid=True,
            error_message=None,
            value_validated=value,
        )

    else:
        return io.ValidationResult(
            is_valid=False,
            error_message="Enter 'delete all' to confirm or 'N' to cancel.",
            value_validated=None,
        )


def delete_all():
    """Delete all applications"""

    client = api.PloomberCloudClient()
    all_projects, _ = get_project_details_mappings(client.get_projects()["projects"])

    if len(all_projects) == 0:
        click.echo("There are no projects to delete.")
        return

    numbered_id = "\n".join(
        [f"{i}. {string}" for i, string in enumerate(all_projects, start=1)]
    )
    prompt_str = (
        f"Here are all your projects: \n{numbered_id}\n"
        "If you are sure you want to delete all projects, type 'delete all'.\n"
        "Note that this action is irreversible and will result in a loss of "
        "all project data and configurations.\n"
        "If you wish to cancel press 'N'"
    )

    choice = io.prompt(
        validator=is_valid_confirmation,
        text=prompt_str,
    )
    if choice.lower() == "n":
        click.echo("Deletion cancelled.")
        return

    try:
        client.delete_all()
    except Exception as e:
        raise PloomberCloudRuntimeException(
            "Error deleting all projects",
        ) from e

    click.echo("All projects have been successfully deleted.")
