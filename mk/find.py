from pathlib import Path

from typing import Iterable

from .location import Location

MK_GLOB = ("*.mk.yaml", "*.mk.yml")


def find_mk_files(mkpath: Iterable[Path], ignore: Iterable[str]) -> Iterable[Location]:
    def traverse(path_rel):
        path_abs = root / path_rel
        if path_abs.is_dir():
            for entry in path_abs.glob("*"):
                for ignore_glob in ignore:
                    if entry.match("**/" + ignore_glob):
                        continue
                yield from traverse(path_rel / entry.name)
        elif path_abs.is_file():
            for glob in MK_GLOB:
                if path_abs.match("**/" + glob):
                    yield Location(path_root=root, path_rel=path_rel)

    for root in mkpath:
        yield from traverse(Path("."))
