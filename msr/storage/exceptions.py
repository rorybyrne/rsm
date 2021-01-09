"""Exceptions for the registry

@author Rory Byrne <rory@rory.bio>
"""


class StorageAccessException(Exception):
    """The registry exists but could not be accessed"""
    pass


class RegistryNotFoundException(Exception):
    """The registry could not be found"""
    pass
