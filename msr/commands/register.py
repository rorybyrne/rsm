"""Register command

@author Rory Byrne <rory@rory.bio>
"""
import asyncio

import click

from msr.model import URL
from msr.service.url_service import UrlService


@click.command()
@click.argument('url')
def register(url: str):
    """Adds a new URL to the registry

    Params:
        url     The URL to be registered.
    """
    url_service = UrlService()

    try:
        url = URL(url)
        print(f"Storing {url.href}")
        asyncio.run(url_service.store_url(url))
    except ValueError as e:
        print("Invalid URL.")
        exit(1)
