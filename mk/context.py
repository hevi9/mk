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
