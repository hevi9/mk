from pathlib import Path

from typing import Iterable

import strictyaml
from ruamel.yaml.scanner import ScannerError


class Source:
    def __init__(self):
        pass


def make_sources_from_file_yaml(path_root: Path, path_rel: Path) -> Iterable[Source]:
    path_abs = path_root / path_rel
    try:
        with path_abs.open() as fo:
            text = fo.read()
            data = strictyaml.load(text).data
            pass
    except ScannerError as ex:
        # add path to scanner exception
        ex.context_mark.name = str(path_abs)
        ex.problem_mark.name = str(path_abs)
        raise ex
    except Exception as ex:
        raise ex
