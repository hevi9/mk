from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Any, Iterable, Optional

from .ex import ValidateError
from .location import Location

if TYPE_CHECKING:
    from .source import Source
    from .index import Index


def scalar_to_bool(scalar: Any) -> bool:
    if isinstance(scalar, bool):
        return scalar
    if isinstance(scalar, str):
        value = str(scalar)
        if value in ("True", "true"):
            return True
        return False
    raise TypeError(f"{scalar} is not type of str or bool")


class Item(metaclass=ABCMeta):
    """ Base for control items. """

    doc: Optional[str]
    """ Description of the item. """

    show: bool
    """ Show item on UI. """

    location: Location
    """ File location of the item. """

    def __init__(self, control: dict, location: Location):
        """ """
        self.doc = control.get("doc", None)
        self.show = scalar_to_bool(control.get("show", True))
        self.location = location

    def validate(self):
        """ Validate item. Raise exception on error. """
        raise ValidateError(f"Validation error on item in location {self.location}")


class Updateable(metaclass=ABCMeta):
    """ """

    @abstractmethod
    def update(self, index: Index) -> None:
        """ """


class Runnable(Updateable):
    """ """

    @abstractmethod
    def run(self, context: dict) -> None:
        """ """

    def programs(self) -> Iterable[str]:
        """ """
        return []
