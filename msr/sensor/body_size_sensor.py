"""Body Size Sensor

@author Rory Byrne <rory@rory.bio>
"""

from aiohttp import ClientSession

from msr.model import URL, Measurement
from msr.sensor.base import Sensor
from msr.sensor.exceptions import PhenomenonFailed
from msr.util.log import Logger


class BodySizeSensor(Sensor, Logger):

    dimension = 'Body Size'
    unit = 'bytes'

    def __init__(self, session: ClientSession = None):
        super().__init__()
        self.session = session

    async def measure(self, url: URL):
        """Perform a GET request and measure the byte size of its content

        Not all requests use the Content-Length header, so this seems to be the best
        way to get the byte size.

        Note:
            I haven't used AIOHTTP before, so I'm not familiar with its API.
        """
        try:
            resp = await self.session.get(url.href)

            return Measurement(float(resp.content.total_bytes), self.dimension)
        except Exception as e:
            # @todo - expand error handling
            self.log.error(e)
            raise PhenomenonFailed()

