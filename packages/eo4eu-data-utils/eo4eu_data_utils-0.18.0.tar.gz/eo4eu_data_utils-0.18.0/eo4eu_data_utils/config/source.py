import os
import copy
from pathlib import Path
from pprint import pformat
from abc import ABC, abstractmethod
from eo4eu_base_utils.typing import Any

from .result import Result
from .model import Source
from .utils import _get_all_keys


class FileSource(Source):
    def __init__(self, root: str|Path = "/"):
        self.root = Path(root)
        self._cache = {}

    def get(self, args: list[str|Path]) -> Result:
        if len(args) == 0:
            return Result.err("No file path provided.")

        path = self.root.joinpath(*args)
        path_str = str(path)
        try:
            if path_str not in self._cache:
                self._cache[path_str] = path.read_text()

            return Result.ok(self._cache[path_str])
        except Exception as e:
            return Result.err(f"Could not read from \"{path_str}\": {e}")


class DictSource(Source):
    def __init__(self, content: dict, arg_kind = "dict key"):
        self.content = content
        self.arg_kind = arg_kind

    def get(self, args: list[str]) -> Result:
        if len(args) == 0:
            return Result.err(f"No {self.arg_kind}(s) provided.")

        try:
            result = copy.deepcopy(self.content)
            for arg in args:
                result = result[arg]

            return Result.ok(result)
        except Exception as e:
            key_str = "/".join(args)
            return Result.err(
                f"Could not find {self.arg_kind} \"{key_str}\" in {pformat(_get_all_keys(self.content))}"
            )


class EnvSource(Source):
    def __init__(self):
        pass

    def get(self, args: list[str]) -> Result:
        key = "_".join([arg.replace("-", "_").upper() for arg in args])
        try:
            return Result.ok(os.environ[key])
        except Exception as e:
            return Result.err(f"Could not find environment variable: {key}")


class CompoundSource(Source):
    def __init__(self, sources: list[Source]):
        self.sources = sources

    def get(self, args) -> Result:
        result = Result.none()
        for source in self.sources:
            result = result.then(source.get(args))
            if result.is_ok():
                return result
        return result
