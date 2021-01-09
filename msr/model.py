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

    def __post_init__(self):
        self._validate_href(self.href)
        domain = urlparse(self.href).netloc
        if not domain:
            raise ValueError(f"Invalid URL: {self.href}")
        self.domain = domain

    @staticmethod
    def _validate_href(href: str):
        parsed_url = urlparse(href)
        if not parsed_url.netloc and parsed_url.scheme:
            raise ValueError(f"Invalid URL: {href}")


T = TypeVar('T', int, float)


@dataclass
class Measurement(Generic[T]):
    value: T


@dataclass
class MeasuredUrl(Generic[T]):
    url: URL
    measurement: Measurement[T]


@dataclass
class Result(Generic[T]):
    data: List[MeasuredUrl[T]]
