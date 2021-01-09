"""Data model

@author Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass, field
from typing import TypeVar, Generic, List
from urllib.parse import urlparse


@dataclass
class URL:
    href: str
    domain: str = field(init=False)
    path: str = field(init=False)

    def __post_init__(self):
        self._validate_href(self.href)
        url_components = urlparse(self.href)
        self.domain = url_components.netloc
        self.path = url_components.path or '/'

    @staticmethod
    def _validate_href(href: str):
        parsed_url = urlparse(href)
        if not parsed_url.netloc and parsed_url.scheme:
            raise ValueError(f"Invalid URL: {href}")


MT = TypeVar('MT', int, float)  # MeasurementType


@dataclass
class Measurement(Generic[MT]):
    value: MT
    title: str


@dataclass
class MeasuredUrl(Generic[MT]):
    url: URL
    measurement: Measurement[MT]


@dataclass
class Result(Generic[MT]):
    data: List[MeasuredUrl[MT]]
