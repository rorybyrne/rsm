"""Measure command

@author Rory Byrne <rory@rory.bio>
"""
import asyncio

import click

from msr.aggregators import Identity
from msr.sensor.body_size_sensor import BodySizeSensor
from msr.service.measurement_service import MeasurementService


@click.command()
def measure():
    """Measures the body sizes of all URLs in the registry"""
    try:
        measurement_service = MeasurementService()
        aggregator = Identity()
        sensor = BodySizeSensor()
        asyncio.run(measurement_service.measure(sensor, aggregator))
    except Exception as e:
        print(e)
        exit(1)
