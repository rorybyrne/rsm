import os

import pytest

from msr.model import URL
from msr.storage.exceptions import RegistryNotFoundException
from msr.storage.url import FileUrlStorage

REGISTRY_FILE = os.environ.get('MSR_REGISTRY_FILE', 'test_registry')


def test_fetching_should_raise_an_exception_if_file_doesnt_exist():
    storage = FileUrlStorage()

    with pytest.raises(RegistryNotFoundException):
        storage.clear()
        storage.get_all()


def test_saving_should_raise_an_exception_if_file_doesnt_exist():
    storage = FileUrlStorage()
    href = 'https://howdy.doody'

    with pytest.raises(RegistryNotFoundException):
        storage.clear()
        storage.save(URL(href))


def test_fetching_from_a_populated_file_should_return_a_list_of_url_objects():
    storage = FileUrlStorage()
    urls = [
        URL('https://howdy.doody/index.html'),
        URL('https://foo.bar/index.html'),
        URL('https://bar.baz/index.html'),
    ]

    for url in urls:
        storage.save(url)

    urls = storage.get_all()
    assert urls[0].domain == 'howdy.doody'
    storage.clear()


def test_fetching_from_an_empty_file_should_return_an_empty_list():
    storage = FileUrlStorage()

    urls = storage.get_all()
    assert type(urls) == list
    assert len(urls) == 0
    storage.clear()
