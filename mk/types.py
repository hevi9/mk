from abc import ABC, abstractmethod
from typing import Iterable


class Runnable(ABC):
    @abstractmethod
    def run(self) -> None:
        """ """

    @abstractmethod
    def programs(self) -> Iterable[str]:
        """ """
