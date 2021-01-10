"""Data model

@author Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass, field
from typing import TypeVar, Generic, List, Dict
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

    @staticmethod
    def from_dict(d: Dict[str, str]):
        return URL(d['href'])


@dataclass
class Measurement:
    value: float
    dimension: str

    @staticmethod
    def from_dict(d: Dict[str, str]):
        return Measurement(float(d['value']), d['dimension'])


@dataclass
class MeasuredUrl:
    url: URL
    measurement: Measurement

    @staticmethod
    def from_dict(d: Dict[str, Dict]):
        return MeasuredUrl(URL.from_dict(d['url']), Measurement.from_dict(d['measurement']))


@dataclass
class Result:
    data: List[MeasuredUrl]
