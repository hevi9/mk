from typing import Iterable
from .types import Runnable
from .source import Source
from .run import run
from .index import Index


class Use(Runnable):
    source: Source
    use_source_name: str
    _use_source: Source = None

    def __init__(self, source: Source, use_source_name: str):
        self.source = source
        self.use_source_name = use_source_name

    def update(self, index: Index) -> None:
        self.use_source = index.find_from(self.use_source_name, self.source)

    def run(self) -> None:
        if not self.use_source:
            raise RuntimeError("use_source is not set")
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
