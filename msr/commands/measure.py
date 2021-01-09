"""Measure command

@author Rory Byrne <rory@rory.bio>
"""
import click

from msr.service.display_service import DisplayService
from msr.service.measurement_service import MeasurementService
from msr.service.url_service import UrlService


@click.command()
def measure():
    """Measures the body sizes of all URLs in the registry

    ...
    """
    # Init services
    url_service = UrlService()
    measurement_service = MeasurementService()
    display_service = DisplayService()

    # Measure URLs
    urls = url_service.fetch_urls()
    result = measurement_service.measure_size(urls)

    # Render results
    display_service.render(result)
