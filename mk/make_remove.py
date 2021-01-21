from typing import Iterable, List, Any
from pathlib import Path
from shutil import rmtree
import os

from .index import Index
from .types import Runnable, Source
from .ui import ui
from .context import render


class Remove(Runnable):

    paths: List[str]

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        params = make_item["remove"]
        if type(params) is str:
            self.paths = params.split()
        elif type(params) is list:
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
                rmtree(path)
            else:
                ui.talk("remove file {path}", path=path)
                os.remove(path)
