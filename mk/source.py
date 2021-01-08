from pathlib import Path
from dataclasses import dataclass

from typing import Iterable

import strictyaml


@dataclass
class Location:
    path_root: Path
    path_rel: Path

    @property
    def path_abs(self):
        return self.path_root / self.path_rel


@dataclass
class Source:
    source: str
    make: Iterable[str]
    location: Location


def make_source_from_item(item: dict, location: Location) -> Source:
    return Source(source=item["source"], make=item["make"], location=location)


def make_sources_from_data(data: Iterable, location: Location) -> Iterable[Source]:
    for item in data:
        yield make_source_from_item(item, location)


def make_sources_from_file_yaml(path_root: Path, path_rel: Path) -> Iterable[Source]:
    location = Location(path_root=path_root, path_rel=path_rel)
    with location.path_abs.open() as fo:
        text = fo.read()
        data = strictyaml.load(text, label=str(location.path_abs)).data
        for source in make_sources_from_data(data, location):
            yield source
