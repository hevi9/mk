from ruamel.yaml.scanner import ScannerError
import pytest
import mk.source
from mk.index import Index
from mk.location import Location
from mk.run import run
from mk.find import update_index_from_roots


# noinspection PyUnresolvedReferences
from .fixtures import mkprimary, mkerror, mkroots, mkroot


def test_primary_source(mkroots):
    path_root, path_rel = mkroots["base"]["primary.mk.yaml"]
    for source in mk.source.make_sources_from_file_yaml(
        Location(path_root=path_root, path_rel=path_rel)
    ):
        assert source.source in ("primary_file", "other_source", "combined")
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


def test_source_run(mkroot, capfd):
    mkroot.have(
        "sample/.mk.yaml",
        """            
        -   source: echo_test
            make:
                - echo testing1
                - echo testing2
                - shell: echo testing3
        """,
    )
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("sample/echo_test")
    run(source)
    out, err = capfd.readouterr()
    lines = out.split()
    assert lines == ["testing1", "testing2", "testing3"]


def _test_source_make_use(mkroot):
    path_root, path_rel = mkroot.have(
        "test/source/make_use.mk.yaml",
        """                    
        -   source: super-source
            make:
                - use: sub-source-1
                - use: sub-source-2
                - echo super-source
        -   source: sub-source-1
            make:
                - echo sub-source-1
        -   source: sub-source-2
            make:
                - echo sub-source-2
        """,
    )
    location = Location(path_root, path_rel)


def _test_source_run_with_use(mkroot, capfd):
    """
    TODO:
    """
    mkroot.have(
        "sample/sub-source-use.mk.yaml",
        """                    
        -   source: super-source
            make:
                - use: sub-source-1
                - use: sub-source-2
                - echo super-source
        -   source: sub-source-1
            make:
                - echo sub-source-1
        -   source: sub-source-2
            make:
                - echo sub-source-2
        """,
    )
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("sample/super-source")
    run(source)
    out, err = capfd.readouterr()
    lines = out.split()
    assert lines == ["sub-source-1", "sub-source-2", "super-source"]
