import os
import shlex
from pathlib import Path
from shutil import move
from typing import Iterable, List

from .context import render
from .index import Index
from .make_base import MakeBase
from .source import Source
from .types import Runnable
from .ui import ui


class Move(MakeBase):

    from_path: str
    to_path: str

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        params = make_item["move"]
        if isinstance(params, str):
            self.from_path, self.to_path = shlex.split(params)
        elif isinstance(params, dict):
            self.from_path = params["from"]
            self.to_path = params["to"]
        else:
            raise ValueError(
                f"Invalid type {type(params)} for 'move' in {source.location}"
            )

    def run(self, context: dict) -> None:
        from_path = Path(render(self.from_path, context))
        to_path = Path(render(self.to_path, context))
        if to_path.exists():
            raise RuntimeError(f"{to_path} exists on 'move'")
        ui.talk(f"Move {from_path} to {to_path}")
        with self._run_context():
            move(str(from_path), to_path)  # str for mypy

    def update(self, index: Index) -> None:
        pass
