from dataclasses import dataclass, field
from typing import List
from .location import Location
from .types import Runnable, Index
from . import types


@dataclass
class Source(types.Source):
    source: str
    location: Location
    make: List[Runnable] = field(default_factory=list)

    @property
    def id(self) -> str:
        return str(self.location.path_rel.parent / self.source).replace("\\", "/")

    def update(self, index: Index) -> None:
        for action in self.make:
            action.update(index)
