from __future__ import annotations

from abc import abstractmethod, ABCMeta
from typing import Iterable, TYPE_CHECKING


if TYPE_CHECKING:
    from .source import Source
    from .index import Index


class Updateable(metaclass=ABCMeta):
    """ """

    @abstractmethod
    def update(self, index: Index) -> None:
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


# class Source(Updateable):
#     """ """
#
#     location: Location
#
#     @property
#     @abstractmethod
#     def id(self) -> str:
#         """ """
#
#     @abstractmethod
#     def run(self, context: dict) -> None:
#         """ """


# class Index(ABC):
#     @abstractmethod
#     def add_source(self, source: "Source") -> None:
#         """ """
#
#     @abstractmethod
#     def list(self) -> Iterable["Source"]:
#         """ """
#
#     @abstractmethod
#     def find(self, source_id: str) -> "Source":
#         """ """
#
#     @abstractmethod
#     def find_from(self, use_source_name: str, from_source: "Source") -> "Source":
#         """ """
