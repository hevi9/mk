from pathlib import Path
from dataclasses import dataclass

from typing import Iterable

# noinspection Mypy
import strictyaml

from mk.location import Location


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


def make_sources_from_file_yaml(location: Location) -> Iterable[Source]:
    with location.path_abs.open() as fo:
        text = fo.read()
        data = strictyaml.load(text, label=str(location.path_abs)).data
        for source in make_sources_from_data(data, location):
            yield source
