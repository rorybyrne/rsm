"""Registry base class

@author Rory Byrne <rory@rory.bio>
"""
import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict

from msr.model import URL
from msr.storage.exceptions import RegistryNotFoundException, StorageAccessException
from msr.util.log import Logger

# Types
StoredUrl = Dict[str, str]


class UrlStorage(ABC, Logger):
    """An abstraction for storing and retrieving URLs"""

    def save(self, url: URL) -> None:
        if not self._storage_exists():
            raise RegistryNotFoundException()

        try:
            self._save(url)
        except Exception as e:
            #  @todo - better error handling here
            self.log.error(e)
            raise StorageAccessException()

    @abstractmethod
    def get_all(self) -> List[URL]:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

    @abstractmethod
    def _storage_exists(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _create_storage(self):
        raise NotImplementedError()

    @abstractmethod
    def _save(self, url: URL):
        raise NotImplementedError()


class FileUrlStorage(UrlStorage):
    """URL storage backed by a file"""
    DATA_HOME = os.environ.get('XDG_DATA_HOME', '.')  # Use the current dir if no XDG configuration is found

    def __init__(self):
        super().__init__()
        # @todo - Add dependency injection
        filename = os.environ.get('MSR_REGISTRY_FILE', 'registry')
        self.file = os.path.join(self.DATA_HOME, f'{filename}.json')
        if not self._storage_exists():
            self._create_storage()

    def get_all(self) -> List[URL]:
        """Load all URLs from the file, then parse them into URL objects and return

        Raises:
            RegistryNotFoundException
        """
        if not self._storage_exists():
            raise RegistryNotFoundException()

        try:
            storage_data: List[StoredUrl] = self._load_file()
            return [URL(stored_url['href']) for stored_url in storage_data]
        except KeyError as e:
            self.log.error(e)
            raise ValueError("Data from the registry could not be parsed")
        except Exception as e:
            #  @todo - improve error handling
            self.log.error(e)
            raise e

    def _load_file(self):
        """Load the registry data from disk

        Raises:
            StorageAccessException
        """
        try:
            with open(self.file) as file:
                storage_data: List[StoredUrl] = json.load(file)
                return storage_data
        except Exception as e:
            raise StorageAccessException("Could not load registry data from file")

    def _storage_exists(self) -> bool:
        """Check that the file exists on disk"""
        return os.path.isfile(self.file)

    def _create_storage(self):
        """Create an empty file"""
        with open(self.file, 'a') as file:
            file.write('[]')  # An empty JSON array

    def _save(self, url: URL):
        """Load the data from file, add the new URL, and then save"""
        urls: List[StoredUrl] = self._load_file()
        for stored_url in urls:
            if stored_url['href'] == url.href:
                # don't add duplicates
                return

        urls.append({'href': url.href, 'domain': url.domain})

        with open(self.file, 'w') as file:
            file.write(json.dumps(urls))

    def clear(self):
        os.remove(self.file)
