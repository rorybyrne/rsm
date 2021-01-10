"""Race command

@author Rory Byrne <rory@rory.bio>
"""
import asyncio

import click

from msr.service.measurement_service import MeasurementService


@click.command()
def race():
    """Measures the average response times of domains in the URL registry"""
    measurement_service = MeasurementService()
    asyncio.run(measurement_service.run('ResponseTime'))
