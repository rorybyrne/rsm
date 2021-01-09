"""Base Sensor

@author Rory Byrne <rory@rory.bio>
"""
from abc import ABC, abstractmethod
from typing import Generic

from msr.model import URL, MT, Measurement
from msr.util.log import Logger


class Sensor(ABC, Logger, Generic[MT]):

    @abstractmethod
    def measure(self, url: URL) -> Measurement[MT]:
        raise NotImplementedError()
