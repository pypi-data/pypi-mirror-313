import shutil
from pathlib import Path

from .interface import Driver


class LocalDriver(Driver):
    def __init__(self, cwdir: Path):
        self._cwdir = cwdir
        self._cache = {}

    def _full_path(self, path: Path) -> Path:
        return self._cwdir.joinpath(path)

    def source(self, path: Path) -> list[Path]:
        full_path = self._full_path(path)
        key = str(full_path)
        if key not in self._cache:
            self._cache[key] = [
                subpath.relative_to(self._cwdir)
                for subpath in full_path.rglob("*")
            ]
        return self._cache[key]

    def move(self, src: Path, dst: Path) -> Path:
        full_src, full_dst = self._full_path(src), self._full_path(dst)
        full_dst.parent.mkdir(parents = True, exist_ok = True)
        full_src.rename(full_dst)
        return dst

    def get(self, path: Path) -> bytes:
        return path.read_bytes()

    def put(self, path: Path, data: bytes) -> Path:
        full_path = self._full_path(path)
        full_path.parent.mkdir(parents = True, exist_ok = True)
        full_path.write_bytes(data)
        return path

    def unpack(self, src: Path, dst: Path) -> list[Path]:
        shutil.unpack_archive(src, dst)
        return [
            subpath
            for subpath in dst.rglob("*")
            if subpath.is_file()
        ]
