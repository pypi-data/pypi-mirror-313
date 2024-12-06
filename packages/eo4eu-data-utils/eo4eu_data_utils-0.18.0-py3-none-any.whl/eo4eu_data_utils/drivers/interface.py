from pathlib import Path
from abc import ABC, abstractmethod


# Some classes may implement this interface only partially
class Driver(ABC):
    @abstractmethod
    def source(self, path: Path) -> list[Path]:
        pass

    @abstractmethod
    def get(self, path: Path) -> bytes:
        pass

    @abstractmethod
    def put(self, path: Path, data: bytes) -> Path:
        pass

    def move(self, src: Path, dst: Path) -> Path:
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement the move method"
        )

    def unpack(self, src: Path, dst: Path) -> list[Path]:
        raise NotImplementedError(
            f"{self.__class__.__name__} does not implement the unpack method"
        )
