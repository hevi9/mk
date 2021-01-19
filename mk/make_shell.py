import shlex
import subprocess

from .index import Index
from .types import Runnable
from .ui import ui
from .context import render


class Shell(Runnable):
    def __init__(self, cmd_text):
        self.cmd_text = cmd_text

    def run(self, context: dict):
        cmd_text = render(self.cmd_text, context)
        ui.run("{cmd}", cmd=cmd_text)
        subprocess.run(cmd_text, shell=True).check_returncode()

    def programs(self):
        parts = shlex.split(self.cmd_text)
        pass

    def update(self, index: Index) -> None:
        pass
