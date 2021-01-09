"""Service to display results

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any

from msr.model import Result
from msr.util.log import Logger


class DisplayService(Logger):
    """Displays results in a pretty format"""

    def __init__(self):
        super().__init__()

    def render(self, result: Result[Any]):
        for foo in result.data:
            print(foo)
