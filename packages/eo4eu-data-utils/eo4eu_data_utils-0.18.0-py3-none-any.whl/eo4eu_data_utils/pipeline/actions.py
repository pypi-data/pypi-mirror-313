from logging import Logger
from pathlib import Path
import functools
import re
from eo4eu_base_utils.typing import Callable, Any

from ..drivers import Driver
from ..metainfo import DSMetainfo
from .interface import DataPath, Data, ActionContext, Action


class Do(Action):
    def __init__(self, func: Callable[[],None]):
        self._func = func

    def execute(self, input: Data, context: ActionContext) -> Data:
        self._func()
        return input


class Log(Action):
    def __init__(
        self,
        log_func: Callable[[Logger,Data],None],
        summary: bool = False
    ):
        self._log_func = log_func
        self._summary = summary

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            logger = context.summary if self._summary else context.logger
            self._log_func(logger, input)
        except Exception as e:
            context.logger.error(f"Failed to log message: {e}")
        return input


class Join(Action):
    def __init__(self, actions: list[Action]):
        self._actions = actions

    def execute(self, input: Data, context: ActionContext) -> Data:
        return Data.join([
            action.execute(input, context)
            for action in self._actions
        ])


class Apply(Action):
    def __init__(self, func: Callable[[Data],Data]):
        self._func = func

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            return self._func(input)
        except Exception as e:
            context.logger.error(f"Unexpected error: {e}")


class Attach(Action):
    def __init__(self, attrs: dict[str,Any]):
        self._attrs = attrs

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            return input.attach(self._attrs)
        except Exception as e:
            context.logger.error(f"Unexpected error: {e}")


class Source(Action):
    def __init__(self, driver: Driver, cwdir: Path, metainfo: DSMetainfo|None = None):
        self._driver = driver
        self._cwdir = cwdir
        self._metainfo = metainfo

    def _get_data(self) -> Data:
        if self._metainfo is None:
            return Data.homogenous(
                driver = self._driver,
                cwdir = self._cwdir,
                rel_paths = self._driver.source(self._cwdir)
            )
        else:
            return Data.ref([
                DataPath(
                    driver = self._driver,
                    cwdir = self._cwdir,
                    path = item["path"],
                    name = item["path"],
                    attrs = {"metainfo": item}
                )
                for item in self._metainfo.products
            ])

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            result = self._get_data()
            if context.selector is not None:
                result = result.attach({
                    "SELECTOR": lambda data_path: context.selector(data_path.path())
                })
            return input.merge(result)
        except Exception as e:
            context.logger.error(f"Failed to list files: {e}")
            return input


class Filter(Action):
    def __init__(self, predicates: list[Any], select_by: str = "SELECTOR"):
        self._predicates = predicates
        self._select_by = select_by

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            return input.filter(_predicate_any(self._predicates, self._select_by))
        except Exception as e:
            context.logger.error(f"Failed to filter files: {e}")
            return Data.empty()


class Switch(Action):
    def __init__(self, cases: list[Any,Action], select_by: str = "SELECTOR"):
        self._cases = cases
        self._select_by = select_by

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            predicates = []
            actions = []
            for predicate, action in self._cases:
                prepared_predicate = _prepare_predicate(predicate, self._select_by)
                if prepared_predicate is not None:
                    predicates.append(prepared_predicate)
                    actions.append(action)

            return Data.join([
                action.execute(data, context)
                for action, data in zip(actions, input.split(*predicates))
            ])
        except Exception as e:
            context.logger.error(f"Unexpected error: {e}")
            return Data.empty()


class Branch(Action):
    def __init__(self, predicate: Any, action: Action, select_by: str = "SELECTOR"):
        self._predicate = predicate
        self._action = action
        self._select_by = select_by

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            prepared_predicate = _prepare_predicate(self._predicate, self._select_by)
            succ, fail = input.ifelse(prepared_predicate)
            result = self._action.execute(succ, context)
            return result.merge(fail)
        except Exception as e:
            context.logger.error(f"Unexpected error: {e}")
            return Data.empty()


class Collect(Action):
    def __init__(self, name: str, consume: bool = False):
        self._name = name
        self._consume = consume

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            if self._consume:
                return input.consume(self._name)
            else:
                return input.collect(self._name)
        except Exception as e:
            context.logger.error(f"Failed to collect files: {e}")
            return input


class FileOp(Action):
    def __init__(self,
        driver: Driver,
        outdir: Path,
        names: tuple[str,str,str],
        dst_func: Callable[[DataPath],Path],
        put_func: Callable[[Driver,DataPath,DataPath],list[DataPath]],
        reselect: bool = False,
        attach: dict[str,Callable[[DataPath],DataPath]]|None = None,
        cd: bool = False,
    ):
        if attach is None:
            attach = {}

        self._driver = driver
        self._outdir = outdir
        self._noun, self._verb, self._past = names
        self._dst_func = dst_func
        self._put_func = put_func
        self._reselect = reselect
        self._attach = attach
        self._cd = cd

    def execute(self, input: Data, context: ActionContext) -> Data:
        result = Data.empty()
        failures = 0
        for src in input:
            dst = None
            try:
                dst = src.but(
                    _driver = self._driver if self._driver is not None else src.driver(),
                    _cwdir = self._outdir if self._cd else src.cwdir(),
                    _path = self._outdir.joinpath(self._dst_func(src)),
                    _name = src.name()
                )
            except Exception as e:
                context.logger.error(f"Unexpected error: {e}")
                continue
            try:
                context.logger.info(f"{self._verb} {src}")
                dst_paths = self._put_func(src, dst)
                if len(dst_paths) == 0:
                    dst_paths = [dst]

                head, tail = dst_paths[0], dst_paths[1:]
                context.logger.info(f"{' ' * (len(self._verb) - 3)} to {head}")
                for path in tail:
                    context.logger.info(f"{' ' * len(self._verb)} {path}")

                _attach = {
                    field: functools.partial(func, src)
                    for field, val in self._attach.items()
                }
                if self._reselect and context.selector is not None:
                    _attach["SELECTOR"] = lambda dst: context.selector(dst.path())

                if len(_attach) > 0:
                    result.merge_inplace(Data.ref(dst_paths).attach(_attach))
                else:
                    result.extend_inplace(dst_paths)
            except Exception as e:
                context.logger.warning(f"Failed to {self._noun} {src.path()}")
                context.logger.warning(f"{' ' * (len(self._noun) + 7)} to {dst}")
                context.logger.warning(str(e))
                failures += 1

        if failures > 0:
            context.summary.error(f"Failed to {self._noun} {failures}/{input.len()} files.")
        return input.with_paths(result.get())


class StatefulAction(Action):
    def __init__(self, action: Action, context: ActionContext):
        self._action = action
        self._context = context

    def execute(self, input: Data, context: ActionContext) -> Data:
        if self._context is None:
            return self._action(input, context)
        else:
            return self._action(input, self._context)


def basic_dst_func(path: DataPath) -> Path:
    return path.name()


def basic_put_func(src: DataPath, dst: DataPath) -> list[DataPath]:
    data = src.get()
    return [dst.put(data)]


def move_put_func(src: DataPath, dst: DataPath) -> list[DataPath]:
    src.driver().move(src.path(), dst.path())
    return [dst]


def unpack_put_func(src: DataPath, dst: DataPath) -> list[DataPath]:
    paths = None
    try:
        paths = src.driver().unpack(src.path(), dst.path())
    except Exception:
        paths = move_put_func(src, dst)
    return [
        src.but(
            _path = path,
            _name = path.relative_to(dst.path().parent)
        )
        for path in paths
    ]


def _prepare_predicate(
    predicate: Any,
    attr: str = "_path",
) -> Callable[[DataPath],bool]|None:
    try:
        if callable(predicate):
            return functools.partial(
                lambda data_path, attr: predicate(data_path.attr(attr)),
                attr = attr
            )
        if isinstance(predicate, str):
            invert = False
            if predicate != "" and predicate[0] == "!":
                invert = True
                predicate = predicate[1:]
            return functools.partial(
                lambda path, regex, attr: invert ^ (
                    regex.fullmatch(str(path.attr(attr))) is not None
                ),
                regex = re.compile(predicate.replace(".", "\\.").replace("*", ".*")),
                attr = attr
            )
        return functools.partial(
            lambda path, predicate, attr: path.attr(attr) == predicate,
            predicate = predicate,
            attr = attr
        )
    except Exception:
        return None


def _predicate_any(
    predicates: list[Any],
    attr: str = "_path",
) -> Callable[[DataPath],bool]:
    prepared_predicates = []
    for predicate in predicates:
        prepared_predicate = _prepare_predicate(predicate, attr)
        if prepared_predicate is not None:
            prepared_predicates.append(prepared_predicate)

    return functools.partial(
        lambda path, ps: any([predicate(path) for predicate in ps]),
        ps = prepared_predicates
    )
