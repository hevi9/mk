from ruamel.yaml.scanner import ScannerError

import pytest
import mk.source

# noinspection PyUnresolvedReferences
from .fixtures import mkprimary, mkerror, mkroots


def test_primary_source(mkprimary):
    for source in mk.source.make_sources_from_file_yaml(*mkprimary):
        assert source.source in ("primary_file", "other_source")
        assert str(source.location.path_abs).endswith("primary.yaml")
        assert type(source.make) is list


def test_error_1(mkroots):
    with pytest.raises(ScannerError) as ex:
        for _ in mk.source.make_sources_from_file_yaml(
            *mkroots["errors"]["error1.yaml"]
        ):
            pass
    msg = str(ex.value)
    assert "error1.yaml" in msg
