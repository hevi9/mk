from abc import ABC, abstractmethod
from typing import Iterable


class Source(ABC):
    """ """

    @property
    @abstractmethod
    def id(self) -> str:
        """ """

    @abstractmethod
    def update(self, index: "Index") -> None:
        """ """


class Index(ABC):
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


class Updateable(ABC):
    @abstractmethod
    def update(self, index: Index) -> None:
        """ """


class Runnable(Updateable):
    @abstractmethod
    def run(self) -> None:
        """ """

    @abstractmethod
    def programs(self) -> Iterable[str]:
        """ """
