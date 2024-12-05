import zipfile
from pathlib import Path
from contextlib import contextmanager
from uuid import uuid4

import click
import shutil
import json

from ploomber_cloud.config import ProjectEnv

IGNORED = {".DS_Store", ".ipynb_checkpoints", "ploomber-cloud.json"}

ENV_PATH = ".env"


def _is_git(path):
    """Return True if path is in a .git directory"""
    return ".git" in Path(path).parts


def _is_pyc(path):
    """Return True if path is a .pyc file"""
    return Path(path).suffix == ".pyc"


def _is_env(path):
    """Return True if path is an .env file"""
    return str(path) == ENV_PATH


def _is_blacklisted_file(path, user_ignored):
    """Return True if path is ignored by user or in IGNORED"""
    for ignored_path in user_ignored:
        if not ignored_path:
            continue

        p = Path(path)

        # If ignored_path is a directory (trailing "/"")
        if ignored_path[-1] == "/":
            p = p.parent  # Only check ignored_path against the file's directory
            ignored_path = ignored_path[:-1]  # Remove trailing "/"

        # If ignored_path exists in root directory or anywhere in the directories
        # when specified as individual name
        if p.is_relative_to(Path(ignored_path)) or ignored_path in p.parts:
            return True

    return Path(path).name in IGNORED


def _is_ignored_file(path, user_ignored):
    return _is_git(path) or _is_pyc(path) or _is_blacklisted_file(path, user_ignored)


def _generate_random_suffix():
    return str(uuid4()).replace("-", "")[:8]


def _clear_env_file():
    """Overwrite .env file with an empty file"""
    copied_path = f"copy_{ENV_PATH}"
    shutil.copy(ENV_PATH, copied_path)

    env = ProjectEnv()
    env.dump({})

    return True, copied_path


def _load_env_file_contents(verbose=True):
    """Load .env secrets into JSON string to send to API"""
    env = ProjectEnv()
    if not env.exists():
        return None

    env.load()
    if verbose:
        click.echo("Reading .env file...")
    secrets_arr = []
    output_message = [
        "Adding the following secrets to the app: ",
    ]

    for key, value in env.data.items():
        secrets_arr.append({"key": key, "value": value})
        output_message.append(f"{key}, ")

    if verbose:
        click.echo("".join(output_message))
    return json.dumps(secrets_arr)


def get_file_size(file_path):
    """Return size of file in bytes"""
    return Path(file_path).stat().st_size


@contextmanager
def zip_app(verbose, user_ignored=None, base_dir=None):
    """Compress app in a zip file.
    Parses secrets from .env and empties .env before zipping it.
    Returns path to zip file, and secrets as JSON string."""
    user_ignored = user_ignored or []
    base_dir = Path(base_dir or "")

    suffix = _generate_random_suffix()
    path_to_zip = base_dir / f"app-{suffix}.zip"
    env_found, copied_env_path = False, None
    secrets = None

    if path_to_zip.exists():
        if verbose:
            click.echo(f"Deleting existing {path_to_zip}...")

        path_to_zip.unlink()

    if verbose:
        click.secho("Compressing app...", fg="green")

    files = [f for f in Path(base_dir).glob("**/*") if Path(f).is_file()]
    files.sort()  # Sorting so that .env is processed first if present

    with zipfile.ZipFile(path_to_zip, "w", zipfile.ZIP_DEFLATED) as zip:
        for path in files:
            if (
                _is_ignored_file(path, user_ignored)
                or Path(path).name == path_to_zip.name
            ):
                click.secho(f"Ignoring file: {path}", fg="yellow")
                continue

            # If .env file found, read and empty it before adding to zip
            if _is_env(path):
                secrets = _load_env_file_contents()
                env_found, copied_env_path = _clear_env_file()
            else:
                click.echo(f"Adding {path}...")

            arcname = Path(path).relative_to(base_dir)
            zip.write(path, arcname=arcname)

    # If we cleared the .env file, put its contents back in
    if env_found:
        shutil.copy(copied_env_path, ENV_PATH)
        Path(copied_env_path).unlink()

    if verbose:
        click.secho("App compressed successfully!", fg="green")

    try:
        yield path_to_zip, secrets
    finally:
        if path_to_zip.exists():
            path_to_zip.unlink()
