from mk.ex import DuplicateSourceError
from mk.source import Source

from typing import Iterable


class Index:
    def __init__(self):
        self._source_map = {}

    def add_source(self, source: Source) -> None:
        if self._source_map.get(source.id):
            raise DuplicateSourceError
        self._source_map[source.id] = source

    def list(self) -> Iterable[Source]:
        return self._source_map.values()

    def find(self, source_id: str) -> Source:
        return self._source_map[source_id]
