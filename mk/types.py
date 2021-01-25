from abc import ABC, abstractmethod
from typing import Iterable

from mk.location import Location


class Updateable(ABC):
    """ """

    def update(self, index: "IIndex") -> None:
        """ """


class Source(Updateable):
    """ """

    location: Location

    @property
    @abstractmethod
    def id(self) -> str:
        """ """

    @abstractmethod
    def run(self, context: dict) -> None:
        """ """


class IIndex(ABC):
    @abstractmethod
    def add_source(self, source: Source) -> None:
        """ """

    @abstractmethod
    def list(self) -> Iterable[Source]:
        """ """

    @abstractmethod
    def find(self, source_id: str) -> Source:
        """ """

    @abstractmethod
    def find_from(self, use_source_name: str, from_source: Source) -> Source:
        """ """


class Runnable(Updateable):
    """ """

    @abstractmethod
    def __init__(self, source: Source, make_item: dict):
        """ """

    @abstractmethod
    def run(self, context: dict) -> None:
        """ """

    def programs(self) -> Iterable[str]:
        """ """
        return []
