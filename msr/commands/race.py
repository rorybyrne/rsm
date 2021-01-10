"""Race command

@author Rory Byrne <rory@rory.bio>
"""
import asyncio

import click

from msr.aggregators import AverageByDomain
from msr.sensor.response_time_sensor import ResponseTimeSensor
from msr.service.measurement_service import MeasurementService


@click.command()
def race():
    """Measures the average response times of domains in the URL registry"""
    try:
        measurement_service = MeasurementService()
        aggregator = AverageByDomain()
        sensor = ResponseTimeSensor()
        asyncio.run(measurement_service.measure(sensor, aggregator))
    except Exception as e:
        print(e)
        exit(1)
