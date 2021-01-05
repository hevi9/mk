import mk.source

from .fixtures import mkprimary, mkerror, mkroots


def test_primary_source(mkprimary):
    mk.source.make_sources_from_file_yaml(*mkprimary)


def test_error_1(mkroots):
    try:
        mk.source.make_sources_from_file_yaml(*mkroots["errors"]["error1.yaml"])
    except Exception as ex:
        pass


def test_error_2(mkroots):
    try:
        mk.source.make_sources_from_file_yaml(*mkroots["errors"]["error2.yaml"])
    except Exception as ex:
        pass
