"""Service to measure phenomena

@author Rory Byrne <rory@rory.bio>
"""
import asyncio
import json
import os
from dataclasses import asdict
from typing import Callable, Coroutine

from aiohttp import ClientSession

from msr.model import URL, MeasuredUrl, Result
from msr.sensor.base import Sensor
from msr.sensor.body_size_sensor import BodySizeSensor
from msr.sensor.response_time_sensor import ResponseTimeSensor
from msr.service.display_service import DisplayService
from msr.service.url_service import UrlService
from msr.util.log import Logger


class MeasurementService(Logger):
    """Measures things and produces consumable results"""

    async def measure(self, url: URL, sensor: Sensor, callback: Callable[[MeasuredUrl], Coroutine]):
        """Async measurement with callback"""
        measurement = await sensor.measure(url)
        await callback(MeasuredUrl(url, measurement))

    async def run(self, sensor_id: str):
        """Generates and executes a set of asynchronous measurement tasks"""
        display_service = DisplayService()
        url_service = UrlService()
        urls = url_service.fetch_urls()

        # Create an empty temp file to store results
        temp_file = 'temp.txt'
        with open(temp_file, 'w') as fl:
            fl.write('[]')

        with display_service.live_table() as live:
            async with ClientSession() as session:
                # Init services
                if sensor_id == 'BodySize':
                    sensor = BodySizeSensor(session)
                elif sensor_id == 'ResponseTime':
                    sensor = ResponseTimeSensor(session)
                else:
                    raise ValueError(f'Invalid sensor: {sensor_id}')

                # Measure URLs
                async def callback(measured_url: MeasuredUrl) -> None:
                    """Receive the URL measurement and update the table"""
                    with open(temp_file, 'r+') as f:
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

                        # Use this to update the table
                        new_table = display_service.build_table(result, sensor.dimension, sensor.unit)
                        live.update(new_table)

                        # Finally, write the combined data back out to the temp file
                        out = json.dumps([asdict(mu) for mu in result.data])
                        f.seek(0)
                        f.write(out)
                        f.flush()
                        os.fsync(f)

                tasks = [self.measure(url, sensor, callback) for url in urls]
                await asyncio.gather(*tasks)
