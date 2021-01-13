from dataclasses import dataclass
from pathlib import Path


@dataclass
class Location:
    path_root: Path
    path_rel: Path

    @property
    def path_abs(self):
        return self.path_root / self.path_rel
