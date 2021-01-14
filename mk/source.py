from dataclasses import dataclass, field
from typing import List
from .location import Location
from .types import Runnable


@dataclass
class Source:
    source: str
    location: Location
    make: List[Runnable] = field(default_factory=list)

    @property
    def id(self):
        return str(self.location.path_rel.parent / self.source).replace("\\", "/")
