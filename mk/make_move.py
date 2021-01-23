from typing import Iterable, List
from pathlib import Path
from shutil import move
import os
import shlex

from .types import Runnable
from .ui import ui
from .context import render
from .types import Source


class Move(Runnable):

    from_path: str
    to_path: str

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        params = make_item["move"]
        if type(params) is str:
            self.from_path, self.to_path = shlex.split(params)
        elif type(params) is dict:
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
        move(from_path, to_path)
