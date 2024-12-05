import os
from pathlib import Path
from typing import Dict, List, Union
import click
import time
import json
from os import environ
from datetime import datetime, timezone

from ploomber_core.exceptions import modify_exceptions

from ploomber_cloud.exceptions import (
    BasePloomberCloudException,
    InvalidPloomberResourcesException,
)
from ploomber_cloud import api, zip_
from ploomber_cloud.config import PloomberCloudConfig
from ploomber_cloud.github import display_github_workflow_info_message
from ploomber_cloud._telemetry import telemetry
from ploomber_cloud.util import (
    convert_byte_to_appropriate_unit,
    fetch_previously_used_secret,
    get_env_suggestion,
    get_user_type,
    is_running_in_ci,
    print_divider,
    show_github_env_var_setup_guide,
    get_max_allowed_app_size_for_user_type,
)
from ploomber_cloud.resources import _get_resource_choices

STATUS_COLOR = {
    "pending": "white",
    "active": "yellow",
    "finished": "green",
    "success": "green",
    "failed": "red",
    "inactive": "red",
    "stopped": "magenta",
}

FAILED_STATUSES = (
    "docker-failed",
    "provisioning-failed",
    "infrastructure-failed",
    "failed",
)

INTERVAL_SECS = 15.0
TIMEOUT_MINS = 15.0

FILE_SIZE_EXCEEDED_ERR = "The size of the zip file exceeds the maximum limit of %s MB. Current file size: %s MB"  # noqa


def error_on_zip_file_too_large(path_to_zip: Path):
    """
    Verify that the zip file size is within the limits of the Ploomber Cloud API.

    Parameters
    ----------
    path_to_zip: str
        The path to zip to be verify

    Raises
    ------
    BasePloomberCloudException
        If the file size exceeds the maximum limit.
    """
    click.echo("Verifying file size...")
    BYTES_TO_MB = 1e-6

    max_allowed_size_mb = get_max_allowed_app_size_for_user_type(get_user_type())
    file_size_mb = os.path.getsize(path_to_zip) * BYTES_TO_MB
    if file_size_mb > max_allowed_size_mb:
        raise BasePloomberCloudException(
            FILE_SIZE_EXCEEDED_ERR % (max_allowed_size_mb, round(file_size_mb, 2))
        )
    click.echo(
        f"Zipped files size "
        f"{' '.join(convert_byte_to_appropriate_unit(int(file_size_mb / BYTES_TO_MB)))}"
        f" is within the limits"
    )


def _unpack_job_status(job, print_status=True):
    """
    Format and output a job status message.
    Return job status (and URL if success).

    Parameters
    ----------
    job: JSON
        Contains job status information to output and process.

    print_status: Boolean
        Flag for printing the task status table

    Returns
    ----------
    job_status: str
        Status of job. Possible values: "success", "running", or "failed".

    app_url: str
        URL to view dashboard. Only returned if job_status == "success".
    """
    tasks = job["summary"]
    status_msg = []

    if print_status:
        for name, status in tasks:
            status_msg.append(
                f"{name}: {click.style(status, fg=STATUS_COLOR[status])} | "
            )

        click.echo("".join(status_msg))

    # grab job status as reported by backend api
    status = job["status"]

    # job is running and reporting healthy
    if status == "running":
        return "success", job["resources"]["webservice"]

    # job has failed or stopped
    if status in FAILED_STATUSES:
        return "failed", None

    # job is still pending, continue watching
    return "pending", None


def _get_intervals():
    return time.time(), INTERVAL_SECS, 60.0 * TIMEOUT_MINS


def _deployment_succeeded_or_failed(job_status, status_page, app_url):
    """Check if job has succeeded or failed"""
    if job_status != "pending":
        click.secho(f"Deployment {job_status}.", fg=STATUS_COLOR[job_status])
        click.echo(f"View project dashboard: {status_page}")
        if job_status == "success":
            click.echo(f"View your deployed app: {app_url}")
        return True
    return False


def _convert_timestamp(timestamp):
    """Convert timestamp string in ISO format to Unix timestamp"""
    timestamp_iso = datetime.fromisoformat(timestamp).replace(tzinfo=timezone.utc)
    last_unix_timestamp = int(timestamp_iso.timestamp() * 1000)
    return last_unix_timestamp


def _get_last_log_timestamp(job_logs):
    """Get the timestamp of the last log fetched"""
    first_record_timestamp = _convert_timestamp(
        job_logs.split("\n")[0].split(" ")[0].strip()
    )
    last_record_timestamp = _convert_timestamp(
        job_logs.split("\n")[-1].split(" ")[0].strip()
    )

    # Sometimes the webservice logs are in reverse order
    last_record_timestamp = (
        first_record_timestamp
        if first_record_timestamp >= last_record_timestamp
        else last_record_timestamp
    )
    return last_record_timestamp


def _watch(client, project_id, job_id):
    """Display status bar and logs of project deployment"""
    start_time, interval, timeout = _get_intervals()

    # poll every 'interval' secs until 'timeout' mins
    while True:
        status_page = api.PloomberCloudEndpoints().status_page(project_id, job_id)

        curr_time = time.time()
        time_diff = curr_time - start_time

        if time_diff >= timeout:
            click.secho("Timeout reached.", fg="yellow")
            click.echo(f"For more details, go to: {status_page}")
            return

        # get job status and logs from API
        job = client.get_job_by_id(job_id)
        logs = client.get_job_logs_by_id(job_id)

        # decide which logs to show based on status
        logs_to_show = "build-docker"
        # if deploy-docker is finished, show webservice logs
        if job["summary"][1][1] in ("success", "finished"):
            logs_to_show = "webservice"

        curr_time_formatted = time.strftime("%H:%M:%S", time.localtime(curr_time))

        # Display link to status page, status bar, and logs
        click.clear()
        click.echo(
            f"[{curr_time_formatted}] \
Deploying project: {project_id} with job ID: {job_id}..."
        )
        print_divider()
        click.echo(f"Web status page: {status_page}")
        print_divider()
        job_status, app_url = _unpack_job_status(job)
        print_divider()
        click.echo(f"Showing {logs_to_show} logs...")
        print_divider()
        click.echo(logs["logs"][logs_to_show])

        # deploy has either succeeded or failed
        if _deployment_succeeded_or_failed(job_status, status_page, app_url):
            break

        time.sleep(interval - (time_diff % interval))


def _watch_incremental(client, project_id, job_id):
    """Display status bar and incremental logs of project deployment"""

    start_time, interval, timeout = _get_intervals()

    last_log_timestamp = 0

    build_status = {
        "build-docker": "pending",
        "deploy": "pending",
        "webservice": "pending",
        "serving-traffic": "pending",
    }

    status_page = api.PloomberCloudEndpoints().status_page(project_id, job_id)
    click.echo("\nTracking deployment progress...\n")

    # poll every 'interval' secs until 'timeout' mins
    while True:
        curr_time = time.time()
        time_diff = curr_time - start_time

        if time_diff >= timeout:
            click.secho("Timeout reached.", fg="yellow")
            click.echo(f"For more details, go to: {status_page}")
            return

        # get job status and logs from API
        job = client.get_job_by_id(job_id)

        if last_log_timestamp != 0:
            logs = client.get_job_logs_by_id_and_timestamp(
                job_id, last_log_timestamp + 1
            )
        else:
            logs = client.get_job_logs_by_id(job_id)

        # decide which logs to show based on status
        logs_to_show = "build-docker"

        # if deploy-docker is finished, show webservice logs
        if job["summary"][1][1] in ("success", "finished"):
            logs_to_show = "webservice"

        tasks = job["summary"]
        for task in tasks:
            stage, current_status = task
            if current_status != build_status[stage]:
                if current_status != "pending":
                    click.echo(
                        f"{click.style('Stage', bold=True)}: "
                        f"{stage}; {click.style('Status', bold=True)}: "
                        f"{click.style(current_status, fg=STATUS_COLOR[current_status], bold=True)}"  # noqa
                    )
                build_status[stage] = current_status

        job_logs = logs["logs"][logs_to_show]
        if job_logs:
            logs_msg = f"Showing {logs_to_show} logs:"
            click.echo(f"\n{click.style(logs_msg, bold=True)}")
            click.echo(job_logs)

        # Update timestamp of last log fetched if any new logs found
        if job_logs:
            new_last_log_timestamp = _get_last_log_timestamp(job_logs)
            if new_last_log_timestamp != last_log_timestamp:
                last_log_timestamp = new_last_log_timestamp

        job_status, app_url = _unpack_job_status(job, print_status=False)

        if _deployment_succeeded_or_failed(job_status, status_page, app_url):
            break

        time.sleep(interval - (time_diff % interval))


def generate_secrets_from_env(keys):
    """
    From a list of keys, read the value of each one and
    package the key-value pairs into a JSON string.

    For this to work, the secrets must be defined as
    environment variables.
    """
    secrets_arr = []
    output_message = [
        "Adding the following secrets to the app: ",
    ]

    for key in keys:
        value = environ.get(key)
        if not value:
            if similar_env_var := get_env_suggestion(key):
                click.secho(
                    f"WARNING: Environment variable '{key}' not found. "
                    f"Did you mean '{similar_env_var}'? "
                    f"Make sure to define '{key}' or use the suggested alternative.",
                    fg="yellow",
                )
            if is_running_in_ci():
                show_github_env_var_setup_guide()
            raise BasePloomberCloudException(
                f"Value for key '{key}' not found. "
                f"Set the value using 'export {key}=value' "
                "or remove it from 'secret-keys'"
            )
        secrets_arr.append({"key": key, "value": value})
        output_message.append(f"{key}, ")

    click.echo("".join(output_message))
    return json.dumps(secrets_arr)


def check_for_secrets_in_config(secret_keys, secrets):
    """
    Check if secrets are defined in `.env` or `secret-keys`.
    If defined in both, returns an error.

    Parameters
    ----------
    secret_keys: list
        A list of keys (strings) of environment variables to be read
        from the current environment.
        It is only keys/names, not the values.

    secrets: JSON
        A list of key-value pairs from .env as a JSON string.
        If no secrets defined in .env, secrets is None.

    Returns
    ----------
    secrets: JSON
        A list of key-value pairs as a JSON string.
    """
    if secret_keys and secrets:
        raise BasePloomberCloudException(
            "Found 'secret-keys' section and '.env' file. "
            "Only one method for adding secrets may be used.\n"
            "Delete '.env' or remove 'secret-keys' from 'ploomber-cloud.json'."
        )
    elif secret_keys:
        click.echo("Generating secrets from 'secret-keys' and environment variables.")
        return generate_secrets_from_env(secret_keys)

    return secrets


def warning_on_missing_secrets(
    client,
    project_id,
    secrets,
):
    """
    Detect missing secrets by comparing to the previous deployment.

    This function compares the secrets provided for the current deployment
    with those from the previous deployment. If any secrets are missing,
    it prompts the user need to confirm that he want to continue. If the user
    refuse, the current deployment is canceled

    Parameters
    ----------
    client: api.PloomberCloudClient
        Ploomber cloud client to fetch the projects secret from
    project_id: str
        The id of project that will be deployed
    secrets: JSON
        A list of key-value pairs from .env as a JSON string.
        If no secrets defined in .env, secrets is None.

    Returns
    ----------
    None

    Throws
    ----------
    BasePloomberCloudException: when the user want to cancel the deployment
    """
    remote_secrets = fetch_previously_used_secret(client, project_id)
    if len(remote_secrets) == 0:
        return

    # Check for secrets that were present in the previous deployment but are missing
    defined_secrets: List[Dict[str, Union[str, None]]] = (
        json.loads(secrets) if secrets else []
    )  # noqa
    defined_secret_keys = {s["key"] for s in defined_secrets}
    missing_secrets = set(remote_secrets) - defined_secret_keys

    if len(missing_secrets) == 0:
        return

    # Confirm with the user if the missing secrets are intentional
    click.secho(
        "Warning: The following secrets from the previous deployment are missing:",
        fg="yellow",
    )
    click.secho(f"  {', '.join(missing_secrets)}", fg="yellow")

    confirm_message = "Are you sure you want to deploy without these secrets?"
    if click.confirm(confirm_message, default=False):
        return

    # Display help
    link = "https://docs.cloud.ploomber.io/en/latest/user-guide/cli.html#defining-secrets"  # noqa
    click.secho("For information on how to set up secrets, please refer to:", fg="cyan")
    click.secho(link, fg="cyan")

    raise BasePloomberCloudException("Deployment canceled")


@modify_exceptions
@telemetry.log_call(log_args=True)
def deploy(watch, watch_incremental=None):
    """Deploy a project to Ploomber Cloud, requires a project to be initialized"""

    client = api.PloomberCloudClient()
    config = PloomberCloudConfig()
    config.load()

    ignored = config.data.get("ignore", [])
    project_id = config.data["id"]

    with zip_.zip_app(verbose=True, user_ignored=ignored) as (path_to_zip, secrets):
        secrets = check_for_secrets_in_config(config.data.get("secret-keys"), secrets)

        # Pre-flight checks
        error_on_zip_file_too_large(path_to_zip)
        if not is_running_in_ci():
            warning_on_missing_secrets(client, project_id, secrets)

        click.echo(f"Deploying project with id: {project_id}...")
        try:
            output = client.deploy(
                path_to_zip=path_to_zip,
                project_type=config.data["type"],
                project_id=config.data["id"],
                secrets=secrets,
                resources=config.data.get("resources"),
                template=config.data.get("template"),
                labels=config.data.get("labels"),
                authentication=config.data.get("authentication"),
                authentication_analytics=config.data.get("authentication_analytics"),
            )
        except BasePloomberCloudException as e:
            if "Invalid Resource" in e.get_message():
                cpu_options, ram_options, gpu_options = _get_resource_choices()
                cpu_options = [float(opt) for opt in cpu_options]
                ram_options = [int(float(opt)) for opt in ram_options]

                raise InvalidPloomberResourcesException(
                    "Resource choices are invalid.\n"
                    f"Valid CPU options: {cpu_options}\n"
                    f"Valid RAM options: {ram_options}\n"
                    f"Valid GPU options: {gpu_options}"
                ) from e
            else:
                raise

        if watch and watch_incremental:
            raise BasePloomberCloudException(
                "You should pass either --watch " "or --watch-incremental, not both."
            )
        if watch:
            _watch(client, output["project_id"], output["id"])
        elif watch_incremental:
            _watch_incremental(client, output["project_id"], output["id"])

    display_github_workflow_info_message()


@modify_exceptions
@telemetry.log_call(log_args=True)
def watch(project_id, job_id=None):
    """Watch the deployment status of a project"""
    client = api.PloomberCloudClient()
    if not job_id:
        project = client.get_project_by_id(project_id)
        job_id = project["jobs"][0]["id"]

    _watch(client, project_id, job_id)
