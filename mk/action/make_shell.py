import subprocess  # nosec

from mk.action.make_base import RunCtx
from mk.context import render
from mk.source import Source
from mk.ui import ui


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
