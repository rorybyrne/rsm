"""Body Size Sensor

@author Rory Byrne <rory@rory.bio>
"""
from abc import abstractmethod

from msr.model import URL, Measurement
from msr.sensor.base import Sensor


class BodySizeSensor(Sensor[float]):

    def measure(self, url: URL) -> Measurement[float]:
        """Measure the body size of a page

        @todo - build this, Rory!
        """
        return Measurement(1.5, "Body Size")
