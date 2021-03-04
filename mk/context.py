import jinja2

env = jinja2.Environment(  # nosec
    variable_start_string="${",
    variable_end_string="}",
    undefined=jinja2.StrictUndefined,
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
    }
