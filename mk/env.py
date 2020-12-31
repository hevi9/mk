from decouple import config
from pathlib import Path

MKPATH = config("MKPATH", default=str(Path("~").expanduser() / ".mkroot")).split(":")
