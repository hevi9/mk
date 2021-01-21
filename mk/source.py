from typing import List
from .location import Location
from .types import Runnable, Index
from . import types


class Source(types.Source):

    name: str
    location: Location
    make: List[Runnable]

    def __init__(self, name: str, location: Location):
        self.name = name
        self.location = location
        self.make = []

    def __str__(self):
        return self.id

    @property
    def id(self) -> str:
        return str(self.location.path_rel.parent / self.name).replace("\\", "/")

    @property
    def dir(self) -> str:
        """ Directory where the source is defined. """
        return str(self.location.path_abs.parent)

    def update(self, index: Index) -> None:
        for action in self.make:
            action.update(index)

    def run(self, context: dict) -> None:
        for action in self.make:
            action.run(dict(context, source=self))
