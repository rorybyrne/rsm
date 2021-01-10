"""Service to display results

@author Rory Byrne <rory@rory.bio>
"""
from contextlib import contextmanager
from typing import ContextManager

from rich.live import Live
from rich.table import Table

from msr.model import Result
from msr.util.log import Logger


class DisplayService(Logger):
    """Displays results in a pretty format"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def build_table(result: Result, dimension: str, unit: str):
        """Construct a table for the given result"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Domain", style="dim", width=12)
        table.add_column("Path", width=32)
        table.add_column(dimension, justify="right")

        for measured_url in result.data:
            table.add_row(
                measured_url.url.domain,
                measured_url.url.path,
                f'{measured_url.measurement.value:0.4f} {unit}'
            )

        return table

    @contextmanager
    def live_table(self, refresh_rate: int = 5) -> ContextManager[Live]:
        """Context manager providing a live UI which can be updated dynamically"""
        live_table = Live(refresh_per_second=refresh_rate)
        live_table.start()
        try:
            yield live_table
        finally:
            live_table.stop()

