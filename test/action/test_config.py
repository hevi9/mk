import pytest

from mk.ui import ui


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
