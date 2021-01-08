import pytest
from pathlib import Path

from typing import Dict, Union

SOURCE_PRIMARY = """
- source: primary_file
  make:
    - echo primary_file
- source: other_source
  make:
    - echo other source
""".strip()

SOURCE_ERROR_1 = """
- FI
- SE
NO
""".strip()

SOURCE_ERROR_2 = """
- FI
al dkaswdkas - SE
- NO
""".strip()


def have(path_root: Path, path_rel: Union[Path, str], text: str) -> (Path, Path):
    path_rel = Path(path_rel)
    path_abs = path_root / path_rel
    with open(path_abs, "w") as fo:
        fo.write(text)
    return path_root, path_rel


@pytest.fixture(scope="session")
def mkroots(tmp_path_factory) -> Dict:
    root_base = tmp_path_factory.mktemp("base")
    root_other = tmp_path_factory.mktemp("other")
    root_errors = tmp_path_factory.mktemp("errors")
    return {
        "base": {"primary.yaml": have(root_base, "primary.yaml", SOURCE_PRIMARY)},
        "other": {},
        "errors": {
            "error1.yaml": have(root_errors, "error1.yaml", SOURCE_ERROR_1),
            "error2.yaml": have(root_errors, "error2.yaml", SOURCE_ERROR_2),
        },
    }


@pytest.fixture(scope="session")
def mkprimary(mkroots) -> (Path, Path):
    return mkroots["base"]["primary.yaml"]


@pytest.fixture(scope="session")
def mkerror(mkroots) -> (Path, Path):
    return mkroots["errors"]["error1.yaml"]
