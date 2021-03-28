""" Run actions in source. """

from typing import Any, Mapping

from creat.source import Source


def run(source: Source, context: Mapping[str, Any]):
    """ Run source. """
    source.run(context)
