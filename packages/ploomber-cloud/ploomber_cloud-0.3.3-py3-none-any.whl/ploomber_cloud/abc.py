from copy import deepcopy
from pathlib import Path
import abc

from ploomber_cloud.exceptions import InvalidPloomberConfigException


class PersistedMapping(abc.ABC):
    """
    An abstract class with a mapping-like interface that persists data
    into a file
    """

    PATH_TO_CONFIG = None

    def __init__(self) -> None:
        if self.PATH_TO_CONFIG is None:
            raise RuntimeError("PATH_TO_CONFIG must be set to a valid path")

        self._validate_path(self.PATH_TO_CONFIG)

        self._path = Path(self.PATH_TO_CONFIG)
        self._data = None

    @property
    def data(self):
        """Return the data stored in the config file"""
        if self._data is None:
            raise RuntimeError("Data has not been loaded")

        return self._data

    def exists(self):
        """Return True if the config file exists, False otherwise"""
        return self._path.exists()

    def __setitem__(self, key, value):
        """Store a key-value pair in the config file, runs validation and dumps"""
        self._data[key] = value
        self._validate_config()
        self.dump(self._data)

    def pop(self, key, default=None):
        try:
            value = self._data[key]
            del self._data[key]
            return value
        except KeyError:
            return default

    def load(self):
        """
        Load the config file. Accessing data will raise an error if this
        method hasn't been executed
        """
        self._data = self._load()
        self._validate_config()

    def dump(self, data_new):
        """Dump data to the config file"""
        self._data = data_new
        self._path.write_text(self._dump(data_new))

    def get_data(self) -> dict:
        """Return a copy of the data stored in the config file"""
        return deepcopy(self._data) or {}

    @abc.abstractmethod
    def _load(self):
        """
        Must be implemented by subclasses. Load the data from the config file and
        return it
        """
        pass

    @abc.abstractmethod
    def _validate_config(self):
        """Validate the config file data, raise an exception if invalid"""
        pass

    @abc.abstractmethod
    def _dump(self, data_new):
        """Dump data to the config file, must return a string to write to the file"""
        pass

    @abc.abstractmethod
    def _validate_path(self, path_to_config):
        """Validate the path to the config file, called in the constructor. Must raise
        an exception if invalid"""
        pass

    def __delitem__(self, key):
        """Delete a key from the config file, the new data is dumped"""
        if key not in self._data:
            raise InvalidPloomberConfigException(f"Key does not exist: {key}")

        del self._data[key]
        self.dump(self._data)
