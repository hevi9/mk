from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, List, Mapping, Optional

from .bases import Item, Runnable
from .context import render
from .location import Location

if TYPE_CHECKING:
    from .index import Index


class Source(Item, Runnable):

    name: str
    """ Name of the source. """

    make: List[Runnable]
    """ Make list for the source """

    _cd: Optional[Path]

    _env: dict

    def __init__(self, name: str, location: Location, control: dict):
        super().__init__(control, location)
        self.name = name
        self.make = []
        self._cd = Path(str(control.get("cd"))) if control.get("cd", False) else None
        self._env = control.get("env", {})

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
        # new_context = {}
        # for key in context.keys():
        #     new_context[key] = render(context[key], context)
        for action in self.make:
            action.run(dict(context, source=self))

    def programs(self) -> Iterable[str]:
        for make in self.make:
            yield from make.programs()

    @property
    def cd(self) -> Optional[Path]:
        return self._cd

    @property
    def env(self) -> Mapping[str, str]:
        return dict(os.environ, **self._env)
