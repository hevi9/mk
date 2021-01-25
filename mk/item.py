from abc import ABCMeta, abstractmethod
from typing import Optional


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
