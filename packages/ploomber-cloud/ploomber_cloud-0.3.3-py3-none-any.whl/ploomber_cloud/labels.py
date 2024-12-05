import click

from ploomber_cloud import api
from ploomber_cloud.util import pretty_print
from ploomber_cloud.config import PloomberCloudConfig
from ploomber_cloud.exceptions import BasePloomberCloudException


def _get_non_duplicate_labels_to_add(config_labels, labels_to_add):
    """Function to filter out the labels that are not already added to the project"""
    unique_labels = list(dict.fromkeys(labels_to_add))
    new_labels = [label for label in unique_labels if label not in config_labels]
    if len(new_labels) == 0:
        raise BasePloomberCloudException(
            "All labels already added. Please try adding a new label."
        )
    return new_labels


def _get_valid_labels_to_delete(config_labels, labels_to_delete):
    """Function to filter the labels that are actually added to the project.
    Labels that are not added will be skipped from deletion"""
    existing_labels_to_delete = [
        label for label in labels_to_delete if label in config_labels
    ]

    if len(existing_labels_to_delete) == 0:
        raise BasePloomberCloudException(
            "Failed to delete labels " "as they are not associated " "with the project."
        )
    else:
        missing_labels = list(set(labels_to_delete) - set(existing_labels_to_delete))
        if len(missing_labels) > 0:
            click.echo(
                f"WARNING: Skipping deletion of non-existing labels: "
                f"{pretty_print(missing_labels)}"
            )
    return existing_labels_to_delete


def _generate_updated_labels_list(config_labels, labels_to_add, labels_to_delete):
    """Update the list of labels to be added:
    1. Combine existing labels with the new labels to be added
    2. Exclude labels to be deleted
    """

    new_labels_to_add = config_labels + labels_to_add

    final_labels = [
        label for label in new_labels_to_add if label not in labels_to_delete
    ]

    # Raise error if all labels to be added already exist
    if sorted(final_labels) == sorted(config_labels):
        raise BasePloomberCloudException("No new labels to add")

    return final_labels


def _view_all_labels(client, project_id):
    """View all labels already added to a deployed project"""

    projects = client.get_project_by_id(project_id)
    project_labels = projects["labels"]
    if project_labels:
        click.echo(f"Labels added to your project: {pretty_print(projects['labels'])}")
    else:
        click.echo("No labels added to your project.")


def sync_labels():
    config = PloomberCloudConfig()
    client = api.PloomberCloudClient()
    config.load()
    project = client.get_project_by_id(config.data["id"])

    if config.data.get("labels") != project["labels"]:
        if project["labels"] is None and "labels" in config.data:
            del config["labels"]
        else:
            config["labels"] = project["labels"]
        click.echo("Labels in config updated.")
    else:
        click.echo("Labels are already up-to-date.")


def labels(labels_to_add, labels_to_delete):
    """Add or delete labels from a project"""
    config = PloomberCloudConfig()
    client = api.PloomberCloudClient()
    config.load()
    if not config.exists():
        raise BasePloomberCloudException(
            "Project not initialized. "
            "Run 'ploomber-cloud init' to initialize your project."
        )

    data = config.data
    project_id = data["id"]

    if not (labels_to_add or labels_to_delete):
        _view_all_labels(client, project_id)
        return

    config_labels = config.data.get("labels", [])
    config_labels = config_labels if config_labels else []

    if len(labels_to_add) > 0:
        labels_to_add = _get_non_duplicate_labels_to_add(config_labels, labels_to_add)

    if len(labels_to_delete) > 0:
        labels_to_delete = _get_valid_labels_to_delete(config_labels, labels_to_delete)

    updated_labels = _generate_updated_labels_list(
        config_labels, labels_to_add, labels_to_delete
    )

    client.update_application_labels(project_id, updated_labels)

    success_msg = "Successfully updated."

    if len(updated_labels) > 0:
        config["labels"] = updated_labels
        success_msg = (
            f"{success_msg} New set of labels: {pretty_print(updated_labels)}."
        )
    else:
        if "labels" in config.data:
            del config["labels"]
        success_msg = f"{success_msg} All labels of the project have been deleted."

    click.echo(success_msg)
