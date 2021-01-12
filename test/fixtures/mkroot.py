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
- source: combined
  uses:
    - primary_file
    - other_source

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


class Root:
    def __init__(self, path_root: Path):
        self.path_root = path_root

    def have(self, path_rel: Union[Path, str], text: str) -> Tuple[Path, Path]:
        path_rel = Path(path_rel)
        path_abs = self.path_root / path_rel
        path_abs.parent.mkdir(parents=True, exist_ok=True)
        with open(path_abs, "w") as fo:
            fo.write(text)
        return self.path_root, path_rel


@pytest.fixture(scope="session")
def mkroot(tmp_path_factory) -> Root:
    return Root(tmp_path_factory.mktemp("root"))


@pytest.fixture(scope="session")
def mkroots(tmp_path_factory) -> Dict:
    root_base = Root(tmp_path_factory.mktemp("base"))
    root_other = Root(tmp_path_factory.mktemp("other"))
    root_errors = Root(tmp_path_factory.mktemp("errors"))
    return {
        "base": {
            ".": root_base,
            "primary.mk.yaml": root_base.have("primary.mk.yaml", SOURCE_PRIMARY),
            ".mk.yaml": root_base.have(".mk.yaml", SOURCE_PRIMARY),
            "prj": {
                ".mk.yaml": root_base.have("prj/.mk.yaml", SOURCE_PRIMARY),
            },
        },
        "other": {".": root_other},
        "errors": {
            ".": root_errors,
            "error1.mk.yaml": root_errors.have("error1.mk.yaml", SOURCE_ERROR_1),
            "error2.mk.yaml": root_errors.have("error2.mk.yaml", SOURCE_ERROR_2),
        },
    }


@pytest.fixture(scope="session")
def mkprimary(mkroots) -> Tuple[Path, Path]:
    return mkroots["base"]["primary.mk.yaml"]


@pytest.fixture(scope="session")
def mkerror(mkroots) -> Tuple[Path, Path]:
    return mkroots["errors"]["error1.mk.yaml"]
