import click
import sys
from . import make


@click.command()
def cli():
    make()


if __name__ == '__main__':
    cli(prog_name="{} -m {}".format(sys.executable, __package__))
