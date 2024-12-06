from abc import ABC, abstractmethod
from pprint import pformat
from pathlib import Path
import logging
import copy
from eo4eu_base_utils.typing import Self, Iterator, Callable, Any

from ..drivers import Driver


class DataPath:
    def __init__(
        self,
        driver: Driver,
        cwdir: Path,
        path: Path,
        name: Path,
        attrs: dict[str,Any]|None = None
    ):
        if attrs is None:
            attrs = {}

        self._driver = driver
        self._cwdir = cwdir
        self._path = path
        self._name = name
        self._attrs = attrs

    def driver(self) -> Path:
        return self._driver

    def cwdir(self) -> Path:
        return self._cwdir

    def path(self) -> Path:
        return self._path

    def name(self) -> Path:
        return self._name

    def attr(self, name: str, default: Any = None) -> Any:
        if name == "":
            return None
        if name[0] == "_":
            return self.__getattribute__(name)
        return self._attrs.get(name, default)

    def setattr(self, name: str, val: Any = None) -> Self:
        if name == "":
            return self
        elif name[0] == "_":
            self.__setattr__(name, val)
        else:
            self._attrs[name] = val
        return self

    def copy(self) -> Self:
        return DataPath(
            driver = self._driver,
            cwdir = copy.deepcopy(self._cwdir),
            path = copy.deepcopy(self._path),
            name = copy.deepcopy(self._name),
            attrs = {name: attr for name, attr in self._attrs.items()}
        )

    def but(self, **kwargs) -> Self:
        result = self.copy()
        for key, val in kwargs.items():
            result.setattr(key, val)
        return result

    def get(self) -> bytes:
        return self._driver.get(self.path())

    def put(self, data: bytes) -> Self:
        out_path = self._driver.put(self.path(), data)
        return self.but(_path = out_path)

    def __repr__(self) -> str:
        name = str(self.name())
        start = str(self.path())[::-1][len(name):][::-1]
        return f"{start}({name})"


class Data:
    def __init__(self, paths: list[DataPath], colls: dict[str,list[DataPath]]):
        self._paths = paths
        self._colls = colls

    @classmethod
    def empty(cls) -> Self:
        return Data(paths = [], colls = {})

    @classmethod
    def ref(cls, paths: list[DataPath]) -> Self:
        return Data(paths = paths, colls = {})

    @classmethod
    def new(cls, paths: list[DataPath]) -> Self:
        return Data.ref([path.copy() for path in paths])

    @classmethod
    def homogenous(cls, driver: Driver, cwdir: Path, rel_paths: Path) -> Self:
        return Data.ref([
            DataPath(
                driver = driver,
                cwdir = cwdir,
                path = cwdir.joinpath(rel_path),
                name = rel_path
            )
            for rel_path in rel_paths
        ])

    @classmethod
    def join(cls, data: list[Self]) -> Self:
        result = Data.empty()
        for entry in data:
            result.merge_inplace(entry)
        return result

    def len(self) -> int:
        return len(self._paths)

    def is_empty(self) -> bool:
        return self.len() == 0

    def get(self, name: str = "") -> list[DataPath]:
        if name == "":
            return [data_path for data_path in self._paths]
        try:
            return [
                data_path
                for data_path in self._colls[name]
            ]
        except Exception:
            return []

    def __iter__(self) -> Iterator[DataPath]:
        for path in self._paths:
            yield path

    def copy(self) -> Self:
        return Data(
            paths = [path.copy() for path in self._paths],
            colls = {
                key: [path.copy() for path in paths]
                for key, paths in self._colls.items()
            },
        )

    def with_paths(self, paths: list[DataPath]) -> Self:
        return Data(
            paths = paths,
            colls = {
                key: [path.copy() for path in paths]
                for key, paths in self._colls.items()
            },
        )

    def split(self, *predicates: Callable[[DataPath],bool]) -> list[Self]:
        result = [[] for _ in predicates]
        for path in self._paths:
            for i, predicate in enumerate(predicates):
                if predicate(path):
                    result[i].append(path)
                    break

        return [self.with_paths(paths) for paths in result]

    def ifelse(self, predicate: Callable[[DataPath],bool]) -> tuple[Self,Self]:
        succ, fail = [], []
        for path in self._paths:
            if predicate(path):
                succ.append(path)
            else:
                fail.append(path)

        return (self.with_paths(succ), self.with_paths(fail))

    def append_inplace(self, paths: list[DataPath]) -> Self:
        self._paths.append(paths)
        return self

    def append(self, paths: list[DataPath]) -> Self:
        return self.copy().append_inplace(paths)

    def extend_inplace(self, paths: list[DataPath]) -> Self:
        self._paths.extend(paths)
        return self

    def extend(self, paths: list[DataPath]) -> Self:
        return self.copy().extend_inplace(paths)

    def merge_inplace(self, other: Self) -> Self:
        self._paths.extend(other._paths)
        self._colls.update(other._colls)
        return self

    def merge(self, other: Self) -> Self:
        return self.copy().merge_inplace(other)

    def apply(self, func: Callable[[list[DataPath]],list[DataPath]]) -> Self:
        return self.with_paths(func(self._paths))

    def map(self, func: Callable[[DataPath],DataPath|None]) -> Self:
        result = []
        for path in self:
            new_path = func(path)
            if new_path is not None:
                result.append(new_path)
        return self.with_paths(result)

    def attach(self, attrs: dict[str,Callable[[DataPath],Any]]) -> Self:
        return self.map(lambda path: path.but(**{
            name: func(path)
            for name, func in attrs.items()
        }))

    def filter(self, predicate: Callable[[DataPath],bool]) -> Self:
        return self.with_paths([path for path in self if predicate(path)])

    def register_coll(self, coll_name: str, paths: list[DataPath]) -> Self:
        self._colls[coll_name] = paths
        return self

    def collect_inplace(self, name: str) -> Self:
        return self.register_coll(name, self._paths)

    def consume_inplace(self, name: str) -> Self:
        self.collect_inplace(name)
        self._paths = []
        return self

    def collect(self, name: str) -> Self:
        return self.copy().collect_inplace(name)

    def consume(self, name: str) -> Self:
        return self.copy().consume_inplace(name)

    def __repr__(self) -> str:
        return "\n".join([pformat(self._paths), pformat(self._colls)])


class ActionContext:
    def __init__(
        self,
        logger: logging.Logger,
        summary: logging.Logger,
        selector: Callable[[Path],Any]|None = None
    ):
        self.logger = logger
        self.summary = summary
        self.selector = selector

    @classmethod
    def dummy(cls) -> Self:
        return ActionContext(None, None, None)


class Action(ABC):
    @abstractmethod
    def execute(self, input: Data, context: ActionContext) -> Data:
        pass
