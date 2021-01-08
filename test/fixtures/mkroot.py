import pytest
from pathlib import Path

from typing import Dict, Union, Tuple

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


def have(path_root: Path, path_rel: Union[Path, str], text: str) -> Tuple[Path, Path]:
    path_rel = Path(path_rel)
    path_abs = path_root / path_rel
    path_abs.parent.mkdir(parents=True, exist_ok=True)
    with open(path_abs, "w") as fo:
        fo.write(text)
    return path_root, path_rel


@pytest.fixture(scope="session")
def mkroots(tmp_path_factory) -> Dict:
    root_base = tmp_path_factory.mktemp("base")
    root_other = tmp_path_factory.mktemp("other")
    root_errors = tmp_path_factory.mktemp("errors")
    return {
        "base": {
            ".": root_base,
            "primary.mk.yaml": have(root_base, "primary.mk.yaml", SOURCE_PRIMARY),
            ".mk.yaml": have(root_base, ".mk.yaml", SOURCE_PRIMARY),
            "prj": {
                ".mk.yaml": have(root_base, "prj/.mk.yaml", SOURCE_PRIMARY),
            },
        },
        "other": {".": root_other},
        "errors": {
            ".": root_errors,
            "error1.mk.yaml": have(root_errors, "error1.mk.yaml", SOURCE_ERROR_1),
            "error2.mk.yaml": have(root_errors, "error2.mk.yaml", SOURCE_ERROR_2),
        },
    }


@pytest.fixture(scope="session")
def mkprimary(mkroots) -> Tuple[Path, Path]:
    return mkroots["base"]["primary.mk.yaml"]


@pytest.fixture(scope="session")
def mkerror(mkroots) -> Tuple[Path, Path]:
    return mkroots["errors"]["error1.mk.yaml"]
