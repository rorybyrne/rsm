"""Base Sensor

@author Rory Byrne <rory@rory.bio>
"""
from abc import ABC, abstractmethod

from msr.model import URL, Measurement
from msr.util.log import Logger


class Sensor(ABC, Logger):

    dimension: str
    unit: str

    @abstractmethod
    async def measure(self, url: URL) -> Measurement:
        raise NotImplementedError()
