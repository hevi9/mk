import sys

import jinja2

env = jinja2.Environment(
    variable_start_string="${",
    variable_end_string="}",
)


def render(text: str, context: dict) -> str:
    globals = env.make_globals({})
    tmpl = jinja2.Template.from_code(
        env, env.compile(text, filename="TODO:FILE"), globals, None
    )
    return tmpl.render(context)


def make_root_context(target_name: str) -> dict:
    """ Make root context. """
    return {
        "name": target_name,
        "target": target_name,
        "cmd": make_platform_cmd(sys.platform),
    }


PLATFORM_CMD = {
    "posix": {
        "rmtree": "rm -rf",
        "cp": "cp -a",
    },
    "win32": {
        "rmtree": "rd /s /q",
        "cp": "xcopy /E /H",
    },
}


def make_platform_cmd(platform: str) -> dict:
    try:
        return PLATFORM_CMD[platform]
    except KeyError:
        return PLATFORM_CMD["posix"]
