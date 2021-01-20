from typing import Iterable, List
from pathlib import Path
from shutil import move
import os

from .types import Runnable
from .ui import ui
from .context import render


class Move(Runnable):

    params_text: str

    def __init__(self, params_text: str):
        self.params_text = params_text

    def run(self, context: dict) -> None:
        text = render(self.params_text, context)
        parts = text.split()
        src = parts[0]
        dst = parts[1]
        ui.talk(f"Move {src} to {dst}")
        move(src, dst)
