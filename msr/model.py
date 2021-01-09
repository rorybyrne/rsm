"""Data model

@author Rory Byrne <rory@rory.bio>
"""
from dataclasses import dataclass, field
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
