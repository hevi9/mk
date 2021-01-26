from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Iterable, Optional

if TYPE_CHECKING:
    from .source import Source
    from .index import Index


class Item(metaclass=ABCMeta):
    """ """

    doc: Optional[str]
    show: bool
    """ Show item on UI. """

    def __init__(self, control: dict):
        """ """
        self.doc = control.get("doc", None)
        self.show = control.get("show", True)

    def validate(self):
        """ Validate item. Raise exception on error. """


class Updateable(metaclass=ABCMeta):
    """ """

    @abstractmethod
    def update(self, index: Index) -> None:
        """ """


class Runnable(Item, Updateable):
    """ """

    @abstractmethod
    def __init__(self, source: Source, make_item: dict):
        """ """
        super().__init__(make_item)

    @abstractmethod
    def run(self, context: dict) -> None:
        """ """

    def programs(self) -> Iterable[str]:
        """ """
        return []
