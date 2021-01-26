from abc import abstractmethod

from mk.bases import Item, Runnable
from mk.index import Index
from mk.location import Location
from mk.source import Source


class MakeBase(Item, Runnable):
    """ Base implementation for make items. """

    source: Source

    def __init__(self, source: Source, control: dict):
        super().__init__(control, source.location)
        self.source = source

    def update(self, index: Index) -> None:
        pass

    @abstractmethod
    def run(self, context: dict) -> None:
        pass
