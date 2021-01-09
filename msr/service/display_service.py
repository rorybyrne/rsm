"""Service to display results

@author Rory Byrne <rory@rory.bio>
"""
from typing import Any, List

from rich.console import Console
from rich.table import Table

from msr.model import Result
from msr.util.log import Logger


class DisplayService(Logger):
    """Displays results in a pretty format"""

    def __init__(self):
        super().__init__()

    def render(self, result: Result[Any]):
        console = Console()
        measurement_type = result.data[0].measurement.title
        table = self._build_table(result, measurement_type)

        console.print(table)

    @staticmethod
    def _build_table(result: Result[Any], measurement_type: str):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Domain", style="dim", width=12)
        table.add_column("Path")
        table.add_column(measurement_type, justify="right")

        for measured_url in result.data:
            table.add_row(
                measured_url.url.domain,
                measured_url.url.path,
                str(measured_url.measurement.value)
            )

        return table
