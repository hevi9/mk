from typing import Iterable, List

from .types import Runnable
from dataclasses import dataclass, field
from .source import Source
from .run import run


@dataclass
class Use(Runnable):
    source: Source
    use_source: Source = None
    _use_source: Source = field(init=False, repr=False)

    def run(self) -> None:
        run(self.use_source)

    def programs(self) -> Iterable[str]:
        return [
            program
            for runnable in self.use_source.make
            for program in runnable.programs()
        ]

    @property
    def use_source(self) -> Source:
        return self._use_source

    @use_source.setter
    def use_source(self, value: Source):
        if value is self.source:  # TODO add recursively circular check
            raise ValueError(f"Cannot use circular dependency for {self.source}")
        self._use_source = value
