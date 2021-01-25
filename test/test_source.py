# pylint: disable=unused-import

import pytest
from ruamel.yaml.scanner import ScannerError

from mk.context import make_root_context
from mk.find import update_index_from_roots
from mk.index import Index
from mk.location import Location
from mk.run import run
from mk.source_build import make_sources_from_file_yaml
from mk.ui import ui

from .fixtures import mkerror, mkprimary, mkroot, mkroots

# noinspection PyUnresolvedReferences


def test_primary_source(mkroots):
    path_root, path_rel = mkroots["base"]["primary.mk.yaml"]
    for source in make_sources_from_file_yaml(
        Location(path_root=path_root, path_rel=path_rel)
    ):
        assert source.name in ("primary_file", "other_source", "combined")
        assert str(source.location.path_abs).endswith("primary.mk.yaml")
        assert isinstance(source.make, list)


def test_error_1(mkroots):
    path_root, path_rel = mkroots["errors"]["error1.mk.yaml"]
    with pytest.raises(ScannerError) as ex:
        for _ in make_sources_from_file_yaml(
            Location(path_root=path_root, path_rel=path_rel)
        ):
            pass
    msg = str(ex.value)
    assert "error1.mk.yaml" in msg


def test_source_run(mkroot, capfd):
    ui.is_verbose = False
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
    context = {}
    run(source, context)
    out, _ = capfd.readouterr()
    lines = out.split()
    assert lines == ["testing1", "testing2", "testing3"]


def test_source_make_use(mkroot, capfd):
    ui.is_verbose = False
    mkroot.have(
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
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/super-source")
    context = {}
    run(source, context)
    out, _ = capfd.readouterr()
    lines = out.split()
    assert lines == ["sub-source-1", "sub-source-2", "super-source"]


def test_source_make_render(mkroot, capfd):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_render.mk.yaml",
        """
        -   source: super-source
            make:
                -   echo super-source ${target}

                -   use: sub-source-frontend
                    vars:
                        target: ${target}/frontend

                -   use: sub-source-backend
                    vars:
                        target: ${target}/backend

        -   source: sub-source-backend
            make:
                -   echo sub-source-backend ${target}

        -   source: sub-source-frontend
            make:
                -   echo sub-source-frontend ${target}
        """,
    )
    index = Index()
    context = {
        "target": "target-dir",
    }
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/super-source")
    run(source, context)
    out, _ = capfd.readouterr()
    lines = out.split()
    assert lines == [
        "super-source",
        "target-dir",
        "sub-source-frontend",
        "target-dir/frontend",
        "sub-source-backend",
        "target-dir/backend",
    ]


def test_source_make_remove_file(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_remove_file.mk.yaml",
        """
        -   source: make-remove-file
            make:
            -   remove: to-be-removed.txt
        """,
    )
    remove_root, remove_rel = mkroot.have("data/to-be-removed.txt", "DATA")
    remove_file = remove_root / remove_rel
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-remove-file")
    assert remove_file.is_file()
    with mkroot.cd("data"):
        run(source, {})
    assert not remove_file.exists()


def test_source_make_remove_tree(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_remove_tree.mk.yaml",
        """
        -   source: make-remove-tree
            make:
            -   remove: tree-to-be-removed
        """,
    )
    mkroot.have("data/tree-to-be-removed/to-be-removed-1.txt", "DATA")
    remove_root, remove_rel = mkroot.have(
        "data/tree-to-be-removed/to-be-removed-2.txt", "DATA"
    )
    remove_dir = (remove_root / remove_rel).parent
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-remove-tree")
    assert remove_dir.is_dir()
    with mkroot.cd("data"):
        run(source, {})
    assert not remove_dir.exists()


def test_source_make_remove_tree_render(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_remove_tree.mk.yaml",
        """
        -   source: make-remove-tree
            make:
            -   remove: ${target}/tree-to-be-removed
        """,
    )
    mkroot.have("data/target-root/tree-to-be-removed/to-be-removed-1.txt", "DATA")
    remove_root, remove_rel = mkroot.have(
        "data/target-root/tree-to-be-removed/to-be-removed-2.txt", "DATA"
    )
    remove_dir = (remove_root / remove_rel).parent
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-remove-tree")
    context = make_root_context("target-root")
    assert remove_dir.is_dir()
    with mkroot.cd("data"):
        run(source, context)
    assert not remove_dir.exists()


def test_source_make_remove_tree_render_list(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_remove_tree.mk.yaml",
        """
        -   source: make-remove-tree
            make:
            -   remove:
                - ${target}/tree-to-be-removed
        """,
    )
    mkroot.have("data/target-root/tree-to-be-removed/to-be-removed-1.txt", "DATA")
    remove_root, remove_rel = mkroot.have(
        "data/target-root/tree-to-be-removed/to-be-removed-2.txt", "DATA"
    )
    remove_dir = (remove_root / remove_rel).parent
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-remove-tree")
    context = make_root_context("target-root")
    assert remove_dir.is_dir()
    with mkroot.cd("data"):
        run(source, context)
    assert not remove_dir.exists()


def test_source_make_copy_tree(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_copy_tree.mk.yaml",
        """
        -   source: make-copy-tree
            make:
            -   copy: ${source.dir}/source-tree target-tree-1
            -   copy:
                    from: ${source.dir}/source-tree
                    to: target-tree-2
        """,
    )
    mkroot.have("test/source/source-tree/.gitignore", "DATA")
    mkroot.have("test/source/source-tree/README.md", "DATA")
    root_path, target_rel = mkroot.have_dir("test/target-area")
    target_area = root_path / target_rel
    #
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-copy-tree")
    context = make_root_context("target-root")
    with mkroot.cd(target_area):
        run(source, context)
    assert (target_area / "target-tree-1" / ".gitignore").exists()
    assert (target_area / "target-tree-2" / ".gitignore").exists()


@pytest.mark.skip(reason="TODO")
def test_source_make_copy_file(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_copy.mk.yaml",
        """
        -   source: cmd-source
            make:
            -   cmd: copy source-file target-file
            -   cmd: copy source-tree target-tree
            -   cmd: move source-tree target-tree
            -   cmd: remove remove-tree-1
        """,
    )


@pytest.mark.skip(reason="TODO")
def test_source_make_move(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_cmd.mk.yaml",
        """
        -   source: cmd-source
            make:
            -   cmd: copy source-file target-file
            -   cmd: copy source-tree target-tree
            -   cmd: move source-tree target-tree
            -   cmd: remove remove-tree-1
        -   source: cmd-source-2
            make:
            -   copy: source-file target-file
            -   copy: source-tree target-tree
            -   move: source-tree target-tree
            -   remove: remove-tree-1
        """,
    )


@pytest.mark.skip(reason="TODO")
def test_source_make_file_update(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_cmd.mk.yaml",
        """
        -   source: cmd-update
            make:
            -   update: ${target}/tsconfig.json
                value: |
                    {
                        "compilerOptions": {
                            "module": "es6"
                        }
                    }
        -   source: cmd-update-2
            make:
            -   update-json: ${target}/tsconfig.json
                value:
                    compilerOptions:
                        module: es6
        """,
    )
