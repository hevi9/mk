import shlex
import subprocess
from .types import Runnable


class Shell(Runnable):
    def __init__(self, cmd_text):
        self.cmd_text = cmd_text

    def run(self):
        subprocess.run(self.cmd_text, shell=True).check_returncode()

    def programs(self):
        parts = shlex.split(self.cmd_text)
        pass
