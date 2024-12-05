from ploomber_cloud.api import PloomberCloudClient


def _get_job_id(client, project_id):
    project = client.get_project_by_id(project_id)
    return project["jobs"][0]["id"]


def start(project_id):
    client = PloomberCloudClient()
    job_id = _get_job_id(client, project_id)
    client.start_job(job_id)


def stop(project_id):
    client = PloomberCloudClient()
    job_id = _get_job_id(client, project_id)
    client.stop_job(job_id)
