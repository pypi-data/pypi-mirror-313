import json
import logging
from pprint import pformat
from pathlib import Path
from eo4eu_base_utils.typing import Self, Iterator, Any

from .utils import _get_nested, _get_all_keys
from .model import Filler, Source
from .source import (
    EnvSource,
    DictSource,
    FileSource,
    CompoundSource,
)
from .logs import cfg_logger
from .result import Result


class ConfigError(Exception):
    pass


class Config:
    def __init__(self, attrs: dict|None = None):
        if attrs is None:
            attrs = {}

        self._attrs = {
            key: (Config(**val) if isinstance(val, dict) else val)
            for key, val in attrs.items()
            if key[0] != "_"
        }

    def to_dict(self):
        return {
            key: val.to_dict() if isinstance(val, self.__class__) else val
            for key, val in self.items()
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __getattr__(self, key: str):
        if key[0] == "_":
            return super().__getattr__(key)
        return self._attrs[key]

    def __setattr__(self, key: str, val):
        if key[0] == "_":
            return super().__setattr__(key, val)
        self._attrs[key] = val

    def __getitem__(self, key: str):
        return self._attrs[key]

    def __setitem__(self, key: str, val):
        self._attrs[key] = val

    def __repr__(self) -> str:
        return pformat(self.to_dict())

    def items(self) -> Iterator[tuple[str,Any]]:
        return self._attrs.items()

    def get(self, value: str, default: Any = None) -> Any:
        try:
            return self._attrs[value]
        except Exception:
            return default


class ConfigBuilder(Filler, Source):
    def __init__(self, **kwargs):
        self._logger = kwargs.get("_logger", cfg_logger)
        self._root = kwargs.get("_root", self)
        self._sources = []
        self._source = None
        self._attrs = {
            key: ConfigBuilder(
                **val,
                _logger = self._logger,
                _root = self._root
            ) if isinstance(val, dict) else val
            for key, val in kwargs.items()
            if key[0] != "_"
        }

    @classmethod
    def from_dict(cls, items: dict) -> Self:
        return Config(**items)

    @classmethod
    def from_json(cls, items: str) -> Self:
        return cls.from_dict(json.loads(items))

    def __getitem__(self, key: str):
        return self._attrs[key]

    def __setitem__(self, key: str, val):
        self._attrs[key] = val

    def items(self) -> Iterator[tuple[str,Any]]:
        return self._attrs.items()

    def __repr__(self) -> str:
        return pformat(self.to_dict())

    def _fmt_all_keys(self) -> str:
        return pformat(_get_all_keys(self._root))

    def items(self) -> Iterator[tuple[str,Any]]:
        return self._attrs.items()

    def inherit(self, root: Self, logger: logging.Logger) -> Self:
        self._root = root
        self._logger = logger
        return self

    def set_source(self, source: Source) -> Self:
        self._source = source

    def use_source(self, source: Source) -> Self:
        self._sources.append(source)
        self._source = CompoundSource(self._sources)
        return self

    def use_files(self, root: str|Path = "/") -> Self:
        return self.use_source(FileSource(root))

    def use_env(self) -> Self:
        return self.use_source(EnvSource())

    def use_dict(self, source: dict, **kwargs) -> Self:
        return self.use_source(DictSource(source, **kwargs))

    def use_json(self, source: str, **kwargs) -> Self:
        return self.use_dict(json.loads(source), **kwargs)

    def get(self, args: list[str]) -> Result:
        if len(args) == 0:
            return Result.err(f"No keys provided")

        head, tail = args[0], args[1:]
        if head != "__parent":
            return self._source.get(args)
        try:
            result = _get_nested(self._root, tail)
            if isinstance(result, Filler):
                return result.fill(self._root, Result.none())
            else:
                return Result.ok(result)
        except Exception as e:
            return Result.err(
                f"Could not find config key \"{'/'.join(tail)}\" in {self._fmt_all_keys()}: {e}"
            )

    def fill(self, source: Source, val: Result) -> Result:
        previous_keys = val.get_or([])
        result = Config()
        for key, val in self.items():
            keys = previous_keys + [key]
            filled_val = Result.ok(val)
            if isinstance(val, self.__class__):
                val.set_source(self._source)
                filled_val = val.fill(self, Result.ok(keys))
            elif isinstance(val, Filler):
                filled_val = val.fill(self, Result.none())

            if filled_val.is_ok():
                result[key] = filled_val.get()
            else:
                return filled_val.then_err(f"Failed to fill config key \"{'/'.join(keys)}\"")

        return Result.ok(result)

    def build(self, clear_sources: bool = True) -> Config:
        if self._source is None:
            raise ConfigError(f"Failed to build configuration: No sources set")

        result = self.fill(self, Result.none())
        if clear_sources:
            self._sources = []
            self._source = None

        if result.is_err():
            result.log(self._logger)
            raise ConfigError(f"Failed to build configuration")

        return result.get()
