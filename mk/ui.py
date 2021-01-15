import sys

import click
from rich.console import Console

console = Console()


class _Ui:

    _is_verbose: bool = True

    @property
    def is_verbose(self) -> bool:
        return self._is_verbose

    @is_verbose.setter
    def is_verbose(self, value: bool):
        self._is_verbose = value

    def error(self, format_text: str, **kwargs):
        click.secho(
            "Error: " + format_text.format(**kwargs), err=True, bold=True, fg="red"
        )

    def error_exit(self, format_text: str, **kwargs):
        self.error(format_text, **kwargs)
        sys.exit(1)

    def talk(self, format_text: str, **kwargs):
        if self.is_verbose:
            click.secho(format_text.format(**kwargs), fg="blue")

    def warn(self, format_text: str, **kwargs):
        click.secho(format_text.format(**kwargs), fg="orange")

    def create(self, format_text: str, **kwargs):
        click.secho(format_text.format(**kwargs), fg="green")

    def run(self, format_text: str, **kwargs):
        if self.is_verbose:
            # click.secho(format_text.format(**kwargs), fg="blue")
            console.rule(format_text.format(**kwargs))


ui = _Ui()
