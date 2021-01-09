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
        domain = urlparse(self.href).netloc
        self.domain = domain
