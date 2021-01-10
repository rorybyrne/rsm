"""Service to display results

@author Rory Byrne <rory@rory.bio>
"""
from contextlib import contextmanager
from typing import ContextManager, List, Tuple, Dict, Any

from rich.live import Live
from rich.table import Table

from msr.aggregators import Aggregator, AverageByDomain
from msr.model import Result
from msr.sensor.base import Sensor
from msr.util.log import Logger


class DisplayService(Logger):
    """Displays results in a pretty format"""

    def __init__(self):
        super().__init__()

    @staticmethod
    def build_table(columns: List[Dict[str, Any]], rows: List[Tuple]):
        """Construct a table for the given result"""
        table = Table(show_header=True, header_style="bold magenta")
        for col in columns:
            table.add_column(**col)

        for row in rows:
            table.add_row(*row)

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

    @staticmethod
    def build_columns(aggregator: Aggregator, sensor: Sensor) -> List[Dict[str, Any]]:
        columns = [
            {
                'header': 'Domain',
                'style': 'dim',
                'width': 24
            },
        ]

        if not isinstance(aggregator, AverageByDomain):
            columns.append({
                'header': 'Path',
                'width': 32
            })

        columns.append({
            'header': sensor.dimension,
            'justify': 'right'
        })

        return columns

