from typing import Iterable

from . import types
from .ex import DuplicateSourceError
from .types import Source


class Index(types.Index):
    def __init__(self):
        self._source_map = {}

    @property
    def source_map(self) -> dict:
        return self._source_map

    def add_source(self, source: Source) -> None:
        if self._source_map.get(source.id):
            raise DuplicateSourceError("already exists", id=source.id, location=source)
        self._source_map[source.id] = source

    def list(self) -> Iterable[Source]:
        return self._source_map.values()

    def find(self, source_id: str) -> Source:
        return self._source_map[source_id]

    def find_from(self, use_source_name: str, from_source: Source) -> Source:
        try:
            return self.find(use_source_name)
        except KeyError:
            pass

        def look(parts):
            try:
                return self.find("/".join(parts + [use_source_name]))
            except KeyError:
                if not parts:
                    return None
                parts.pop()
                return look(parts)

        source = look(from_source.id.split("/"))
        if not source:
            raise KeyError(f"Source {use_source_name} not found")
        return source
