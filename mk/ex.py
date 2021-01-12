from dataclasses import dataclass


# from pathlib import Path


# @dataclass
# class FileScannerError(Exception):
#     problem: str
#     context: str
#     text: str
#     line: int
#     column: int
#     path_root: Path
#     path_rel: Path
from mk.location import Location


class DuplicateSourceError(Exception):
    location: Location
    id: str

    def __init__(self, msg, id: str, location: Location):
        super().__init__(f"Duplicate {id} in {location}: {msg}")
        self.location = location
        self.id = id
