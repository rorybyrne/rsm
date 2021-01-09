"""Registry service to store URLs

@author Rory Byrne <rory@rory.bio>
"""
from typing import List

from msr.storage.exceptions import StorageAccessException
from msr.storage.url.FileRegistry import FileRegistry
from msr.util.log import Logger


class RegistryException(Exception):
    """Failed to access the registry"""
    pass


class UrlService(Logger):
    """Service exposing the registry backend to consumers

    Note: This should probably be a data layer rather than a service, but we're being concise.
    """

    def __init__(self):
        super().__init__()
        self.registry = FileRegistry()  # Later we should inject this via dependency injection

    def store_url(self, url: str) -> None:
        """Store the given URL in the registry"""
        try:
            self.registry.save(url)
        except StorageAccessException as e:
            self.log.error(e)
            raise RegistryException("Could not save URL in the registry.")
        except Exception as e:
            self.log.error(e)
            raise RegistryException(e)

    def fetch_urls(self) -> List[str]:
        """Fetch all of the URLs from the registry"""
        try:
            return self.registry.get_all()
        except StorageAccessException as e:
            self.log.error(e)
            raise RegistryException("Could not find URLs")
        except Exception as e:
            self.log.error(e)
            raise RegistryException(e)
