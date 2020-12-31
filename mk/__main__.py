import click
import sys
from . import make


@click.command()
def cli():
    # sources = find_sources()
    # source = get_name_from_sources(name, sources)
    make()


if __name__ == '__main__':
    cli(prog_name="{} -m {}".format(sys.executable, __package__))
