from mk.source import Source


def run(source: Source):
    for shell in source.make:
        shell.run()
