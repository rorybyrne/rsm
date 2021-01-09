"""Service to measure phenomena

@author Rory Byrne <rory@rory.bio>
"""
from typing import List

from msr.model import URL, Result, MeasuredUrl, Measurement
from msr.util.log import Logger


class MeasurementService(Logger):
    """Measures things and produces consumable results"""

    def __init__(self):
        super().__init__()

    def measure_size(self, urls: List[URL]) -> Result[float]:
        result = [MeasuredUrl(url, Measurement(1.3)) for url in urls]

        return Result(result)

