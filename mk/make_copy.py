from typing import Iterable, List, Any
from pathlib import Path
from shutil import copy2, copytree
import os
import shlex

from .types import Runnable, Source
from .ui import ui
from .context import render


class Copy(Runnable):

    path_from: str
    path_to: str

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        params = make_item["copy"]
        if type(params) is str:
            self.path_from, self.path_to = shlex.split(params)
        elif type(params) is dict:
            self.path_from = params["from"]
            self.path_to = params["to"]
        else:
            raise ValueError(
                f"Invalid type {type(params)} for field 'copy' in {source.location}"
            )

    def run(self, context: dict) -> None:
        path_from = Path(render(self.path_from, context))
        path_to = Path(render(self.path_to, context))
        copytree(
            path_from,
            path_to,
            symlinks=False,
            ignore=None,
            ignore_dangling_symlinks=False,
            dirs_exist_ok=False,
        )
