import json
import os

import pytest

from msr.model import URL
from msr.storage.exceptions import RegistryNotFoundException
from msr.storage.url import FileUrlStorage

TEST_FILE = 'test_registry'


def test_fetching_should_raise_an_exception_if_file_doesnt_exist():
    storage = FileUrlStorage()

    with pytest.raises(RegistryNotFoundException):
        storage.get_all()


def test_saving_should_raise_an_exception_if_file_doesnt_exist():
    storage = FileUrlStorage(TEST_FILE)
    storage.save(URL('https://howdy.doody'))

    storage.clear()


def test_fetching_from_a_populated_file_should_return_a_list_of_url_objects():
    storage = FileUrlStorage(TEST_FILE)
    urls = [
        URL('https://howdy.doody/index.html'),
        URL('https://foo.bar/index.html'),
        URL('https://bar.baz/index.html'),
    ]

    data = json.dumps([url.__dict__ for url in urls])

    filename = os.path.join(FileUrlStorage.DATA_HOME, f'{TEST_FILE}.json')
    with open(filename, 'a') as file:
        file.write(data)

    urls = storage.get_all()
    assert urls[0].domain == 'howdy.doody'
    storage.clear()


def test_fetching_from_an_empty_file_should_return_an_empty_list():
    storage = FileUrlStorage(TEST_FILE)

    filename = os.path.join(FileUrlStorage.DATA_HOME, f'{TEST_FILE}.json')
    with open(filename, 'a') as file:
        file.write('[]')

    urls = storage.get_all()
    assert type(urls) == list
    assert len(urls) == 0
    storage.clear()
