import shlex
import subprocess  # nosec

from .context import render
from .index import Index
from .types import Runnable
from .ui import ui
from .types import Source


class Shell(Runnable):
    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        self.cmd_text = make_item["shell"]

    def run(self, context: dict):
        cmd_text = render(self.cmd_text, context)
        ui.run("{cmd}", cmd=cmd_text)
        subprocess.run(cmd_text, shell=True).check_returncode()  # nosec

    def programs(self):
        # parts = shlex.split(self.cmd_text)
        ...

    def update(self, index: Index) -> None:
        ...
