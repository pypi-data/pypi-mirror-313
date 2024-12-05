import click

from ploomber_core.telemetry.telemetry import UserSettings

from ploomber_cloud.exceptions import BasePloomberCloudException
from ploomber_cloud._telemetry import telemetry


def get():
    """Get API key from the user's settings"""
    api_key = UserSettings().get_cloud_key()

    if api_key is None:
        raise BasePloomberCloudException(
            "API key not found. Please run 'ploomber-cloud key YOURKEY', "
            "or set the key in environment variable 'PLOOMBER_CLOUD_KEY'"
        )

    return api_key


@telemetry.log_call()
def set_api_key(api_key):
    """Set API key in the user's settings"""
    settings = UserSettings()
    existing_key = settings.cloud_key is not None

    settings.cloud_key = api_key

    if existing_key:
        click.secho("Your API key has been replaced successfully.", fg="green")
    else:
        click.secho("Your API key has been stored successfully.", fg="green")
