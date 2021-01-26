from __future__ import annotations

from typing import TYPE_CHECKING, List

from .bases import Item, Runnable, Updateable
from .location import Location

if TYPE_CHECKING:
    from .index import Index


class Source(Item, Runnable):

    name: str
    """ Name of the source. """

    make: List[Runnable]
    """ Make list for the source """

    def __init__(self, name: str, location: Location, control: dict):
        super().__init__(control, location)
        self.name = name
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
