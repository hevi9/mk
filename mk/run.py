from mk.source import Source


def run(source: Source, context: dict):
    for runnable in source.make:
        runnable.run(context)
