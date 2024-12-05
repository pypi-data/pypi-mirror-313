import os
from pathlib import Path
import json
from contextlib import contextmanager


from dotenv import dotenv_values

from ploomber_cloud.util import pretty_print, raise_error_on_duplicate_keys
from ploomber_cloud.constants import VALID_PROJECT_TYPES, FORCE_INIT_MESSAGE
from ploomber_cloud.exceptions import InvalidPloomberConfigException
from ploomber_cloud.abc import PersistedMapping


@contextmanager
def path_to_config(path_or_directory: str):
    """
    Context manager to temporarily change the path that PloomberCloudConfig uses to
    read/write the config file.
    Args:
      path_or_directory (str):
        - If it's a full path (including filename), it will be used as is.
        - If it's just a directory, the current filename will be kept and only
          the directory will change.
        - If None, no changes will be made.
    """
    CURRENT_PATH = PloomberCloudConfig.PATH_TO_CONFIG

    if path_or_directory is not None:
        if os.path.splitext(path_or_directory)[1]:
            # Is a full path
            new_path = path_or_directory
        else:
            # It's just a directory, keep the current filename
            _, current_filename = os.path.split(CURRENT_PATH)
            new_path = os.path.join(path_or_directory, current_filename)

        PloomberCloudConfig.PATH_TO_CONFIG = new_path

    try:
        yield
    finally:
        PloomberCloudConfig.PATH_TO_CONFIG = CURRENT_PATH


class PloomberCloudConfig(PersistedMapping):
    """Manages the ploomber-cloud.json file"""

    PATH_TO_CONFIG = "ploomber-cloud.json"

    def _validate_labels(self):
        if "labels" not in self._data.keys():
            return None
        for label in self._data["labels"]:
            if not isinstance(label, str):
                return (
                    f"'labels' must be a list of strings. "
                    f"Found invalid label: {label}.\n"
                )

    def _validate_secret_keys(self):
        if "secret-keys" not in self._data.keys():
            return None
        for key in self._data["secret-keys"]:
            if not isinstance(key, str):
                return (
                    f"'secret-keys' must be a list of strings. "
                    f"Found invalid key: {key}.\n"
                )

    def _validate_resources(self):
        if "resources" not in self._data.keys():
            return None

        error = ""
        resources = self._data["resources"]

        KEYS_RESOURCES = {"cpu", "ram", "gpu"}
        RESOURCES_TYPES = {"cpu": float, "ram": int, "gpu": int}
        for required_key in KEYS_RESOURCES:
            if required_key not in resources.keys():
                error = f"{error}Mandatory key '{required_key}' is missing.\n"

        for resource, resource_value in resources.items():
            if resource not in KEYS_RESOURCES:
                error = (
                    f"{error}Invalid resource: '{resource}'. "
                    f"Valid keys are: {pretty_print(KEYS_RESOURCES)}\n"
                )
            elif not isinstance(resource_value, RESOURCES_TYPES[resource]):
                error = (
                    f"{error}Only {RESOURCES_TYPES[resource].__name__} "
                    f"values allowed for resource '{resource}'\n"
                )

        if error:  # Add fix resources message if resources have error
            error = f"{error}To fix it, run 'ploomber-cloud resources --force'\n"

        return error

    def _validate_config(self):
        """Method to validate the ploomber-cloud.json file
        for common issues"""
        KEYS_REQUIRED = {"id", "type"}
        KEYS_OPTIONAL = {
            "resources",
            "template",
            "labels",
            "secret-keys",
            "ignore",
            "authentication",
            "authentication_analytics",
        }
        TYPES = {
            "id": str,
            "type": str,
            "resources": dict,
            "template": str,
        }

        error = ""

        for key in KEYS_REQUIRED:
            if key not in self._data.keys():
                error = f"{error}Mandatory key '{key}' is missing.\n"

        for key, value in self._data.items():
            if key not in KEYS_REQUIRED | KEYS_OPTIONAL:
                error = (
                    f"{error}Invalid key: '{key}'. "
                    f"Valid keys are: {pretty_print(KEYS_REQUIRED | KEYS_OPTIONAL)}\n"
                )
            elif value == "":
                error = f"{error}Missing value for key '{key}'\n"
            elif key in TYPES and not isinstance(value, TYPES[key]):
                error = (
                    f"{error}Only {TYPES[key].__name__} "
                    f"values allowed for key '{key}'\n"
                )
            elif key == "labels" and not isinstance(value, list):
                error = "'labels' must be a list of strings.\n"
            elif key == "secret-keys" and not isinstance(value, list):
                error = "'secret-keys' must be a list of strings.\n"
            elif key == "ignore" and not isinstance(value, list):
                error = "'ignore' must be a list of strings.\n"
            elif key == "type" and value not in VALID_PROJECT_TYPES:
                error = (
                    f"{error}Invalid type '{value}'. "
                    f"Valid project types are: "
                    f"{pretty_print(VALID_PROJECT_TYPES)}\n"
                )

        resources_error = self._validate_resources()
        if resources_error:
            error = f"{error}{resources_error}"

        labels_error = self._validate_labels()
        if labels_error:
            error = f"{error}{labels_error}"

        secret_keys_error = self._validate_secret_keys()
        if secret_keys_error:
            error = f"{error}{secret_keys_error}"

        if error:
            raise InvalidPloomberConfigException(
                f"There are some issues with the ploomber-cloud.json file:\n{error}\n"
                f"{FORCE_INIT_MESSAGE}\n"
            )

    def _load(self):
        if not self.exists():
            raise InvalidPloomberConfigException(
                "Project not initialized. "
                "Run 'ploomber-cloud init' to initialize your project."
            )

        try:
            return json.loads(
                self._path.read_text(), object_pairs_hook=raise_error_on_duplicate_keys
            )
        except ValueError as e:
            error_message = "Please add a valid ploomber-cloud.json file."
            if "Duplicate keys" in str(e):
                error_message = f"{error_message} {str(e)}"
            raise InvalidPloomberConfigException(
                f"{error_message}\n{FORCE_INIT_MESSAGE}"
            ) from e

    def _dump(self, data_new):
        """Dump data to the config file"""
        return json.dumps(data_new, indent=4)

    def _validate_path(self, path_to_config):
        if Path(path_to_config).suffix != ".json":
            raise InvalidPloomberConfigException(
                f"Invalid config file name: {path_to_config}. "
                "Must have .json extension"
            )


class ProjectEnv(PersistedMapping):
    PATH_TO_CONFIG = ".env"

    def _validate_config(self):
        pass

    def _load(self):
        return dotenv_values(self._path)

    def _dump(self, data_new):
        lines = [f"{key}={value}" for key, value in data_new.items()]
        return "\n".join(lines)

    def _validate_path(self, path_to_config):
        pass
