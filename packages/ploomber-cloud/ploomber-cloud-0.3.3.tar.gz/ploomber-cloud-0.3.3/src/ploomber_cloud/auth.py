import click
from ploomber_cloud import io
from ploomber_cloud.config import PloomberCloudConfig, ProjectEnv
from ploomber_cloud.constants import CONFIGURE_RESOURCES_MESSAGE
from ploomber_cloud.exceptions import (
    InvalidPloomberConfigException,
)
from ploomber_cloud.messages import (
    CARRIED_OVER_CREDENTIALS_MSG,
    no_authentication_error_msg,
)
from ploomber_cloud.models import AuthCompatibleFeatures
from ploomber_cloud.util import requires_init

BASE_PREFIX_USERNAME = "username_"
BASE_PREFIX_PASSWORD = "password_"


def _make_authentication_field_for_secret(feature: AuthCompatibleFeatures):
    """
    Return the authentication fields (username and password) for an authenticated
    feature in the .env file
    """
    return (
        BASE_PREFIX_USERNAME + feature.value,
        BASE_PREFIX_PASSWORD + feature.value,
    )


def _make_authentication_field_for_config(feature: AuthCompatibleFeatures):
    """
    Return the authentication fields (username and password) for an authenticated
    feature in the ploomber-cloud.json file
    """
    config_field = "authentication"
    if feature != AuthCompatibleFeatures.MAIN_APP:
        config_field = f"authentication_{feature.value}"
    return config_field


def rm_nginx_auth(feature: AuthCompatibleFeatures):
    """
    Remove password protection for the existing project

    Parameters
    ______________________________________________________
    - feature: str
      Remove authentication for specified feature
    """

    # specify which fields to remove
    username, password = _make_authentication_field_for_secret(feature)

    # Load .env file
    env = ProjectEnv()
    if env.exists():
        env.load()
        user_secrets = env.data
    else:
        user_secrets = {}

    # Remove the authentication for the corresponding feature under `template`
    # in pcloud json
    config_field = _make_authentication_field_for_config(feature)

    config = PloomberCloudConfig()
    config.load()

    try:
        del config[config_field]
    except InvalidPloomberConfigException:
        raise InvalidPloomberConfigException(no_authentication_error_msg(feature))

    # Remove secrets from user_secrets
    user_secrets.pop(username, None)
    user_secrets.pop(password, None)

    # Write updated secrets to .env
    env.dump(user_secrets)

    click.echo(f"Successfully removed password authentication for {feature.value}.")
    click.echo(CONFIGURE_RESOURCES_MESSAGE)


@requires_init
def nginx_auth(feature: AuthCompatibleFeatures, overwrite: bool = False):
    """
    Configure password protection for the existing project

    Parameters
    ______________________________________________________
    - for_feature: str
      Makes password for specified feature. (For example, password protected main app,
      or password protected app analytics)
    """
    username_field, password_field = _make_authentication_field_for_secret(feature)

    # Check for `.env` and load secrets if they exist
    user_secrets = {}
    env = ProjectEnv()
    if env.exists():
        env.load()
        user_secrets = env.data

    # Prompt for secrets
    password_secrets = [
        username_field,
        password_field,
    ]

    # NOTE: not trivial to perform extra checks, since we cannot simply forward to
    # backend username and password: introduces a vulnerability.
    # Encryption key is accessible only on the backend currently.
    # TODO: If we want to validate credentials before deploying, we need a single
    # source of truth.
    def _ensure_not_empty(value) -> io.ValidationResult:
        if not value:
            return io.ValidationResult(False, "Value cannot be empty", value)
        return io.ValidationResult(True, "", value)

    # This flag will indicate whether we need to warn the user that
    # his credentials were extracted from the .env file
    should_send_warning_credentials_were_carried_over = False

    # If user has already saved a credential, don't prompt for it
    for key in password_secrets:
        if (
            not overwrite and key in user_secrets.keys()
        ):  # overwrite make sure we always prompt
            # add to the request the relevant fields if needed
            should_send_warning_credentials_were_carried_over = True
            continue

        user_secrets[key] = io.prompt(
            validator=_ensure_not_empty,
            text=f"Enter the value for {key}",
        )

    def _warn_credentials_were_carried_over():
        click.secho(CARRIED_OVER_CREDENTIALS_MSG, fg="yellow")

    if not overwrite and should_send_warning_credentials_were_carried_over:
        _warn_credentials_were_carried_over()

    # Write old and new secrets to .env
    env.dump(user_secrets)

    # Add the authentication for the corresponing feature under
    # `template` in pcloud json
    config_field = _make_authentication_field_for_config(feature)
    config = PloomberCloudConfig()
    config.load()
    config[config_field] = {
        "username": user_secrets[username_field],
        "password": user_secrets[password_field],
    }

    env_file_msg = "Your authentication credentials have been stored in .env"
    click.echo(env_file_msg)
    click.echo(f"Successfully configured password authentication for {feature.value}.")
    click.echo(CONFIGURE_RESOURCES_MESSAGE)
