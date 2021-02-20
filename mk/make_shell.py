import subprocess  # nosec

from .context import render
from .make_base import RunCtx
from .source import Source
from .ui import ui


class Shell(RunCtx):
    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        self.cmd_text = make_item["shell"]

    def run(self, context: dict):
        cmd_text = render(self.cmd_text, context)
        ui.run("{cmd}", cmd=cmd_text)
        subprocess.run(
            cmd_text,
            shell=True,  # nosec
            cwd=render(self.cd, context) if self.cd else None,
            env=self.env,
        ).check_returncode()  # nosec

    def programs(self):
        # TODO: implement programs
        # parts = shlex.split(self.cmd_text)
        ...
