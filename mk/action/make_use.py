from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional

from mk.action.make_base import RunCtx
from mk.context import render
from mk.run import run
from mk.source import Source

if TYPE_CHECKING:
    from mk.index import Index


class Use(RunCtx):
    source: Source
    use_source_name: str
    _use_source: Optional[Source] = None
    use_context: dict

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        self.source = source
        self.use_source_name = make_item["use"]
        self.use_context = make_item.get("vars", {})

    def update(self, index: Index) -> None:
        self.use_source = index.find_from(self.use_source_name, self.source)

    def run(self, context: dict) -> None:
        if not self.use_source:
            raise RuntimeError("use_source is not set")
        use_context = {k: render(v, context) for k, v in self.use_context.items()}
        run(self.use_source, dict(context, **use_context))

    def programs(self) -> Iterable[str]:
        if not self.use_source:
            raise ValueError(".use_source is not updated")
        return [
            program
            for runnable in self.use_source.make
            for program in runnable.programs()
        ]

    @property
    def use_source(self) -> Optional[Source]:
        return self._use_source

    @use_source.setter
    def use_source(self, value: Source):
        if value is self.source:  # TODO add recursively circular check
            raise ValueError(f"Cannot use circular dependency for {self.source}")
        self._use_source = value
