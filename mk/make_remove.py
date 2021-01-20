from typing import Iterable, List
from pathlib import Path
from shutil import rmtree
import os

from .index import Index
from .types import Runnable
from .ui import ui


class Remove(Runnable):

    paths: List[Path]

    def __init__(self, file_names: Iterable[str]):
        self.paths = [Path(file_name) for file_name in file_names]

    def run(self, context: dict) -> None:
        for path in self.paths:
            # "safety" guard
            if len(str(path)) < 3:
                raise ValueError(f"don't remove path {path}")
            ui.talk(f"remove {path}", path=path)
            if not path.exists():
                continue
            if path.is_dir():
                rmtree(path)
            else:
                os.remove(path)
