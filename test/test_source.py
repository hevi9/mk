from ruamel.yaml.scanner import ScannerError

import pytest
import mk.source
from .fixtures import mkprimary, mkerror, mkroots


def test_primary_source(mkprimary):
    mk.source.make_sources_from_file_yaml(*mkprimary)


def test_error_1(mkroots):
    with pytest.raises(ScannerError) as ex:
        mk.source.make_sources_from_file_yaml(*mkroots["errors"]["error1.yaml"])


def test_error_2(mkroots):
    with pytest.raises(ScannerError) as ex:
        mk.source.make_sources_from_file_yaml(*mkroots["errors"]["error2.yaml"])
