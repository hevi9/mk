import os
import stat
from pathlib import Path
from shutil import rmtree
from typing import Any, Iterable, List

from .context import render
from .index import Index
from .types import Runnable
from .ui import ui
from .source import Source


def _remove_readonly(func, path, _):
    """ Clear the readonly bit and reattempt the removal. """
    os.chmod(path, stat.S_IWRITE)
    func(path)


class Remove(Runnable):

    paths: List[str]

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        params = make_item["remove"]
        if isinstance(params, str):
            self.paths = params.split()
        elif isinstance(params, list):
            self.paths = params
        else:
            raise ValueError(
                f"Invalid type {type(params)} for field 'remove' in {source.location}"
            )

    def run(self, context: dict) -> None:
        # eval
        paths = [Path(render(path, context)) for path in self.paths]
        # run
        for path in paths:
            # "safety" guard
            if len(str(path)) < 3:
                raise ValueError(f"don't remove path {path}")
            if not path.exists():
                ui.talk("{path} does not exists, no op", path=path)
                continue
            if path.is_dir():
                ui.talk("remove tree {path}", path=path)
                rmtree(path, onerror=_remove_readonly)
            else:
                ui.talk("remove file {path}", path=path)
                os.remove(path)

    def update(self, index: Index) -> None:
        pass
