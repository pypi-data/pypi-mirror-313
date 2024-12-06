from abc import ABC, abstractmethod
from .result import Result


class Source(ABC):
    @abstractmethod
    def get(self, args) -> Result:
        return Result.err("")


class Filler(ABC):
    @abstractmethod
    def fill(self, source: Source, val: Result) -> Result:
        return None
