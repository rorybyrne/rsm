"""Base Sensor

@author Rory Byrne <rory@rory.bio>
"""
from abc import ABC, abstractmethod

from aiohttp import ClientSession

from msr.model import URL, Measurement
from msr.util.log import Logger


class Sensor(ABC, Logger):

    dimension: str
    unit: str

    def __init__(self):
        super().__init__()
        self.session = None

    def attach_session(self, session: ClientSession):
        self.session = session

    @abstractmethod
    async def measure(self, url: URL) -> Measurement:
        raise NotImplementedError()
