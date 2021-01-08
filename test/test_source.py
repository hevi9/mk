from ruamel.yaml.scanner import ScannerError

import pytest
import mk.source
from mk.location import Location

# noinspection PyUnresolvedReferences
from .fixtures import mkprimary, mkerror, mkroots


def test_primary_source(mkroots):
    path_root, path_rel = mkroots["base"]["primary.mk.yaml"]
    for source in mk.source.make_sources_from_file_yaml(
        Location(path_root=path_root, path_rel=path_rel)
    ):
        assert source.source in ("primary_file", "other_source")
        assert str(source.location.path_abs).endswith("primary.mk.yaml")
        assert type(source.make) is list


def test_error_1(mkroots):
    path_root, path_rel = mkroots["errors"]["error1.mk.yaml"]
    with pytest.raises(ScannerError) as ex:
        for _ in mk.source.make_sources_from_file_yaml(
            Location(path_root=path_root, path_rel=path_rel)
        ):
            pass
    msg = str(ex.value)
    assert "error1.mk.yaml" in msg
