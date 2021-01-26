import os
from abc import abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Iterable, Mapping, Optional, Tuple

from mk.bases import Item, Runnable
from mk.index import Index
from mk.location import Location
from mk.source import Source


class MakeBase(Item, Runnable):
    """ Base implementation for make items. """

    source: Source
    _cd: Optional[Path]
    _env: dict

    def __init__(self, source: Source, control: dict):
        super().__init__(control, source.location)
        self.source = source
        self._cd = Path(str(control.get("cd"))) if control.get("cd", False) else None
        self._env = control.get("env", {})

    def update(self, index: Index) -> None:
        pass

    def programs(self) -> Iterable[str]:
        return []

    @property
    def cd(self) -> Optional[Path]:
        if self._cd:
            return self._cd
        if self.source.cd:
            return self.source.cd
        return None

    @property
    def env(self) -> Mapping[str, str]:
        return dict(self.source.env, **self._env)

    @contextmanager
    def _run_context(self):
        if self.cd:
            cwd_old = Path.cwd()
            try:
                os.chdir(self.cd)
                yield self.cd, self.env
            finally:
                os.chdir(cwd_old)
        else:
            yield None, self.env

    @abstractmethod
    def run(self, context: dict) -> None:
        pass
