"""Data model

@author Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass, field
from typing import TypeVar, Generic, List, Dict, Union
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

    def __lt__(self, other: 'MeasuredUrl'):
        return self.measurement.value < other.measurement.value

    def row_data(self, unit: str):
        return self.url.domain, self.url.path, f'{self.measurement.value:0.4f} {unit}'


@dataclass
class MeasuredDomain:
    domain: str
    measurement: Measurement

    def row_data(self, unit: str):
        return self.domain, f'{self.measurement.value:0.4f} {unit}'

    def __lt__(self, other: 'MeasuredDomain'):
        return self.measurement.value < other.measurement.value


MeasuredResource = Union[MeasuredUrl, MeasuredDomain]

MT = TypeVar('MT', MeasuredDomain, MeasuredUrl)


@dataclass
class Result(Generic[MT]):
    data: List[MT]
