from mk.source import Source


def run(source: Source):
    for runnable in source.make:
        runnable.run()
