import click
import sys
from loguru import logger
from pathlib import Path


def find_sources(paths):
    pass


@click.command()
@click.option(
    "paths",
    "--path",
    default=[Path("~").expanduser() / ".mkroot"],
    multiple=True,
    envvar="MKPATH",
    type=click.Path(),
    help="Path(s) to find sources",
)
@click.argument("name")
def cli(paths, name):
    sources = find_sources(paths)
    # source = get_name_from_sources(name, sources)
    # make()
    click.echo(f"{paths}")
    pass


if __name__ == "__main__":
    cli(prog_name="{} -m {}".format(sys.executable, __package__))
