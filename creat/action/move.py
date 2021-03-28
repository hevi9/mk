""" Move operation. """

import shlex
from pathlib import Path
from shutil import move
from typing import Any, Mapping

from creat import get_console
from creat.action.bases import Action
from creat.context import render
from creat.source import Source

_console = get_console()


class Move(Action):
    """ Move file or tree action. """

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
            raise ValueError(f"Invalid type {type(params)} for 'move' in {source._location}")

    def run(self, context: Mapping[str, Any]) -> None:
        from_path = Path(render(self.from_path, context))
        to_path = Path(render(self.to_path, context))
        if to_path.exists():
            raise RuntimeError(f"{to_path} exists on 'move'")
        _console.print(f"Move {from_path} to {to_path}")
        with self._run_context():
            move(str(from_path), to_path)  # str for mypy
