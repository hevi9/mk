from typing import Iterable, Mapping

import strictyaml

from mk.location import Location
from .source import Source
from .shell import Shell
from .use import Use


def _make_shell(_: Source, make_item: dict):
    return Shell(make_item["shell"])


def _make_use(source: Source, make_item: dict):
    return Use(source, make_item["use"], make_item.get("vars", {}))


MAKE_ITEM_MAP = {
    "shell": _make_shell,
    "use": _make_use,
}


def make_source_from_dict(item: dict, location: Location) -> Source:
    """ """
    source = Source(
        source=item["source"],
        location=location,
    )
    make_list = item["make"]
    for make_item in make_list:
        if type(make_item) is str:
            make_item = {"shell": make_item}
        elif isinstance(make_item, Mapping):
            pass
        else:
            raise TypeError(f"Invalid make item type {type(make_item)}")
        make_type = make_item.keys() & MAKE_ITEM_MAP.keys()
        if len(make_type) < 1:
            raise ValueError("Missing make type")
        if len(make_type) > 1:
            raise ValueError(f"Conflicting make types {make_type}")
        make_type = make_type.pop()
        source.make.append(MAKE_ITEM_MAP[make_type](source, make_item))
    return source


def make_sources_from_file_yaml(location: Location) -> Iterable[Source]:
    with location.path_abs.open() as fo:
        text = fo.read()
        data = strictyaml.load(text, label=str(location.path_abs)).data
        if not type(data) is list:
            raise TypeError(f"not a list {data}")
        for item in data:
            yield make_source_from_dict(item, location)
