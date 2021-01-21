import pytest
import mk.find
from pathlib import Path

# noinspection PyUnresolvedReferences
from .fixtures import mkprimary, mkerror, mkroots


def test_find_mk_files(mkroots):
    for location in mk.find.find_mk_files(
        [mkroots["base"]["."].path_root, mkroots["other"]["."].path_root], [".git"]
    ):
        assert location.path_rel in (
            Path("primary.mk.yaml"),
            Path(".mk.yaml"),
            Path("prj/.mk.yaml"),
        )


def test_find_mk_sources_from_roots(mkroots):
    for source in mk.find.find_mk_sources_from_roots(
        [mkroots["base"]["."].path_root, mkroots["other"]["."].path_root], []
    ):
        assert source.name in ("primary_file", "other_source", "combined")
