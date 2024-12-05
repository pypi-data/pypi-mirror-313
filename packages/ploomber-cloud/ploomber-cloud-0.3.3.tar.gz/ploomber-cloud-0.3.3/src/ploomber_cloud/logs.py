import click
from ploomber_cloud.exceptions import (
    BasePloomberCloudException,
    PloomberCloudRuntimeException,
)
from ploomber_cloud.api import PloomberCloudClient
from ploomber_cloud.util import print_divider


def logs(job_id, project_id, type):
    """
    Print logs for a particular job.

    Parameters
    ----------
    job_id: str or None
        ID of job. Will be prioritized over project_id

    project_id: str or None
        ID of project. Will be used to find latest job under this project,
        then print logs from that job.

    type: str or None
        Type of logs to print. If specified, options are: docker, web.
        If not specified, both docker and web logs are printed.
    """

    if not (job_id or project_id):
        raise BasePloomberCloudException("You must specify a job-id or project-id.")

    if type and type not in ("docker", "web"):
        raise BasePloomberCloudException(
            "Invalid logs type. Available options: 'docker' or 'webservice'"
        )

    client = PloomberCloudClient()

    if job_id:
        try:
            logs = client.get_job_logs_by_id(job_id)
        except Exception as e:
            raise PloomberCloudRuntimeException(
                f"Couldn't find job with ID: {job_id}"
            ) from e
    elif project_id:
        try:
            project = client.get_project_by_id(project_id)
        except Exception as e:
            raise PloomberCloudRuntimeException(
                f"Couldn't find project with ID: {project_id} or project has no jobs"
            ) from e

        job_id = project["jobs"][0]["id"]
        logs = client.get_job_logs_by_id(job_id)

    type_output_mapping = {
        "docker": ["build-docker"],
        "web": ["webservice"],
        None: ["build-docker", "webservice"],
    }

    output_types = type_output_mapping[type]

    for type in output_types:
        print_divider()
        output = logs["logs"][type]

        if not output:
            output = "Waiting for logs..."

        click.echo(f"Showing {type} logs:\n")
        click.echo(output)
