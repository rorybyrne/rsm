"""Service to measure phenomena

@author Rory Byrne <rory@rory.bio>
"""
import asyncio
import json
from dataclasses import asdict
from typing import Callable, Coroutine

from aiohttp import ClientSession
from rich.live import Live

from msr.aggregators import Aggregator, Identity
from msr.model import URL, MeasuredUrl, Result
from msr.sensor.base import Sensor
from msr.sensor.body_size_sensor import BodySizeSensor
from msr.sensor.response_time_sensor import ResponseTimeSensor
from msr.service.display_service import DisplayService
from msr.service.url_service import UrlService
from msr.util.log import Logger


class MeasurementService(Logger):
    """Measures things and produces consumable results"""

    def __init__(self):
        super().__init__()
        self.display_service = DisplayService()
        self.url_service = UrlService()

    async def measure(self, sensor: Sensor, aggregator: Aggregator):
        """Generates and executes a set of asynchronous measurement tasks"""
        urls = self.url_service.fetch_urls()

        temp_filename = f'{sensor.dimension}_temp.txt'
        self._create_temp_file(temp_filename)

        with self.display_service.live_table() as live:
            async with ClientSession() as session:
                sensor.attach_session(session)

                callback = self._build_update_callback(live, sensor, temp_filename, aggregator)

                tasks = [self._measure(url, sensor, callback) for url in urls]
                await asyncio.gather(*tasks)

    # Private

    @staticmethod
    async def _measure(url: URL, sensor: Sensor, callback: Callable[[MeasuredUrl], Coroutine]):
        """Async measurement with callback"""
        measurement = await sensor.measure(url)
        await callback(MeasuredUrl(url, measurement))

    def _build_update_callback(
            self,
            live: Live,
            sensor: Sensor,
            temp_filename: str,
            aggregator: Aggregator = Identity()
    ):
        async def callback(measured_url: MeasuredUrl) -> None:
            """Receive the URL measurement and update the table"""
            with open(temp_filename, 'r+') as f:
                # Read the temp data and parse it into a list of dicts
                raw = f.read()
                if len(raw) == 0:
                    dicts = []
                else:
                    dicts = json.loads(raw)

                # Parse the dicts into MSR models
                # noinspection PyListCreation
                measured_urls = [MeasuredUrl.from_dict(d) for d in dicts]
                measured_urls.append(measured_url)
                result = Result(measured_urls)

                # Write the raw data back out to the temp file
                out = json.dumps([asdict(mu) for mu in result.data])
                f.seek(0)
                f.write(out)

                # Aggregate the data and update the live display
                aggregated_result = aggregator(result)
                aggregated_result.data.sort()

                rows = [measurement.row_data(sensor.unit) for measurement in aggregated_result.data]
                columns = self.display_service.build_columns(aggregator, sensor)
                new_table = self.display_service.build_table(columns, rows)
                live.update(new_table)

        return callback

    @staticmethod
    def _get_sensor(sensor_id: str):
        # Init services
        if sensor_id == 'BodySize':
            return BodySizeSensor
        elif sensor_id == 'ResponseTime':
            return ResponseTimeSensor
        else:
            raise ValueError(f'Invalid sensor: {sensor_id}')

    @staticmethod
    def _create_temp_file(filename: str):
        with open(filename, 'w') as fl:
            fl.write('[]')


