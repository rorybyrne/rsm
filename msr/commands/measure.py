"""Measure command

@author Rory Byrne <rory@rory.bio>
"""
import asyncio

import click

from msr.service.measurement_service import MeasurementService


@click.command()
@click.option('--sensor', default='BodySize', help='Choose BodySize or ResponseTime')
def measure(sensor: str):
    """Measures the body sizes of all URLs in the registry"""
    measurement_service = MeasurementService()
    asyncio.run(measurement_service.run(sensor))
