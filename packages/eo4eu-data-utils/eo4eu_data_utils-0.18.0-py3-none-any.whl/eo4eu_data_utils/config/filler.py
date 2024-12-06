import logging
from pathlib import Path
from eo4eu_base_utils.typing import Any, Callable, Self, Iterator

from .model import Filler, Source
from .result import Result
from .utils import _to_bool, _to_list


logger = logging.getLogger("eo4eu_data_utils.config")


class DependencyFiller(Filler):
    def __init__(self, value: Filler|Any):
        self._value = value

    def fill(self, source: Source, val: Result) -> Result:
        if isinstance(self._value, Filler):
            return self._value.fill(source, val)
        return Result.ok(self._value)


class DefaultFiller(Filler):
    def __init__(self, default: Any):
        self._filler = DependencyFiller(default)

    def fill(self, source: Source, val: Result) -> Result:
        if val.is_err():
            return val.then(self._filler.fill(source, val))
        else:
            return val


class WarnFiller(Filler):
    def __init__(
        self,
        level: int = logging.WARNING,
        logger: logging.Logger|None = None,
        warn_always: bool = False
    ):
        if logger is None:
            logger = logging.getLogger("eo4eu_data_utils.config")

        self._level = level
        self._logger = logger
        self._warn_always = warn_always

    def fill(self, source: Source, val: Result) -> Result:
        if self._warn_always or val.is_err():
            val.log(self._logger, level = self._level)
        return val


class SourceFiller(Filler):
    def __init__(self, args, override = False):
        self._args = [DependencyFiller(arg) for arg in args]
        self._override = override

    def _iter_fill_args(self, source: Source, val: Result) -> Iterator[Result]:
        for arg in self._args:
            yield arg.fill(source, val)

    def fill(self, source: Source, val: Result) -> Result:
        args = Result.merge_until_err(self._iter_fill_args(source, val))
        if args.is_err():
            return args

        result = source.get(args.get())
        if val.is_err():
            return val.then(result)
        if self._override:
            return val.then_try(result)
        else:
            return val


class ValidateFiller(Filler):
    def __init__(
        self,
        func: Callable[[Any],bool],
        name: str|None = None,
        args: tuple|None = None,
        kwargs: dict|None = None,
    ):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        if name is None:
            try:
                name = func.__name__
            except Exception:
                name = "unknown"

        self._func = func
        self._name = name
        self._args = args
        self._kwargs = kwargs

    def _err_message(self, value: Result, extra = ""):
        return f"Validator \"{self._name}\" rejected \"{value}\"{extra}"

    def fill(self, source: Source, val: Result) -> Result:
        if val.is_err():
            return val.then_err(self._err_message(val))

        try:
            if self._func(val.get(), *self._args, **self._kwargs):
                return val
            return val.then_err(self._err_message(val.get()))
        except Exception as e:
            return val.then_err(self._err_message(val.get(), f": {e}"))


class ApplyFiller(Filler):
    def __init__(
        self,
        func: Callable[[Any],Any],
        name: str|None = None,
        args: tuple|None = None,
        kwargs: dict|None = None,
        must_apply: bool = True,
        print_traceback: bool = False,
    ):
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}
        if name is None:
            try:
                name = func.__name__
            except Exception:
                name = "unknown"

        self._func = func
        self._name = name
        self._args = args
        self._kwargs = kwargs
        self._must_apply = must_apply
        self._print_traceback = print_traceback

    def _err_message(self, value: Result, extra = ""):
        return f"Cannot apply function \"{self._name}\" to \"{value}\"{extra}"

    def _exc_message(self, value: Result, exception: Exception):
        exc_str = f": {exception}"
        if self._print_traceback:
            exc_str = f":\n{traceback.format_exc()}"

        return self._err_message(value, extra = exc_str)

    def fill(self, source: Source, val: Result) -> Result:
        if val.is_err():
            return val.then_err(self._err_message(val))

        try:
            return val.then_ok(self._func(val.get(), *self._args, **self._kwargs))
        except Exception as e:
            msg = self._exc_message(val, e)
            if self._must_apply:
                return val.then_err(msg)
            else:
                return val.then_benign_err(msg)


class CreateFiller(Filler):
    def __init__(
        self,
        func: Callable[[Any],Any],
        name: str = "",
        args: tuple|None = None,
        kwargs: dict|None = None,
    ):
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        self._func = func
        self._name = name
        self._args = [DependencyFiller(arg) for arg in args]
        self._kwargs = [(key, DependencyFiller(arg)) for key, arg in kwargs.items()]

    def fill(self, source: Source, val: Result) -> Result:
        filled_args = []
        for arg in self._args:
            filled_arg = arg.fill(source, val)
            if filled_arg.is_err():
                return filled_arg
            filled_args.append(filled_arg.get())

        filled_kwargs = {}
        for key, arg in self._kwargs:
            filled_arg = arg.fill(source, val)
            if filled_arg.is_err():
                return filled_arg
            filled_kwargs[key] = filled_arg.get()

        try:
            return val.then_ok(self._func(*filled_args, **filled_kwargs))
        except Exception as e:
            return val.then_err(f"Cannot create \"{self._name}\": {e}")


class IfElseFiller(Filler):
    def __init__(self, if_true: Any|Filler, if_false: Any|Filler):
        self._if_true = DependencyFiller(if_true)
        self._if_false = DependencyFiller(if_false)

    def fill(self, source: Source, val: Result) -> Result:
        if val.is_err():
            return val

        if val.get():
            return self._if_true.fill(source, Result.none())
        else:
            return self._if_false.fill(source, Result.none())


class Try(Filler):
    def __init__(self, fillers: list[Filler], **kwargs):
        self._fillers = fillers

    def fill(self, source: Source, val: Result) -> Result:
        for filler in self._fillers:
            val = filler.fill(source, val)
        return val

    def then(self, filler: Filler) -> Self:
        self._fillers.append(filler)
        return self

    @classmethod
    def option(cls, *args, prefix = None, **kwargs) -> Self:
        if prefix is None:
            args = list(args)
        else:
            args = [prefix] + list(args)

        return Try([SourceFiller(args)], **kwargs)

    @classmethod
    def cfgmap(cls, *paths: str|Path) -> Self:
        return cls.option(*paths, prefix = "configmaps")

    @classmethod
    def secret(cls, *paths: str|Path) -> Self:
        return cls.option(*paths, prefix = "secrets")

    @classmethod
    def parent(cls, *paths: str|Path, prefix = None) -> Self:
        return cls.option(*paths, prefix = "__parent")

    @classmethod
    def create(cls, func: Callable[[Any],Any], *args, name: str = "", **kwargs):
        return Try([CreateFiller(func, name = name, args = args, kwargs = kwargs)])

    def or_option(self, *args, prefix = None) -> Self:
        return self.then(Try.option(*args, prefix = prefix))

    def or_cfgmap(self, *paths: str|Path) -> Self:
        return self.then(Try.cfgmap(*paths))

    def or_secret(self, *paths: str|Path) -> Self:
        return self.then(Try.secret(*paths))

    def or_parent(self, *paths: str|Path) -> Self:
        return self.then(Try.parent(*paths))

    def into_option(self, *args, prefix = None) -> Self:
        return Try.option(*args, self, prefix = prefix)

    def into_cfgmap(self, *paths: str|Path) -> Self:
        return Try.cfgmap(*paths, self)

    def into_secret(self, *paths: str|Path) -> Self:
        return Try.secret(*paths, self)

    def into_parent(self, *paths: str|Path) -> Self:
        return Try.parent(*paths, self)

    def default(self, default: Any) -> Self:
        return self.then(DefaultFiller(default))

    def warn(self, **kwargs) -> Self:
        return self.then(WarnFiller(**kwargs))

    def ifelse(self, if_true: Filler|Any, if_false: Filler|Any) -> Self:
        return self.then(IfElseFiller(if_true, if_false))

    def validate(self, func: Callable[[Any],Any], *args, **kwargs) -> Self:
        return self.then(ValidateFiller(func, *args, **kwargs))

    def apply(self, func: Callable[[Any],Any], *args, **kwargs) -> Self:
        return self.then(ApplyFiller(func, *args, **kwargs))

    def format(self, fmt_string: str, **kwargs) -> Self:
        return self.apply(
            func = lambda s: fmt_string.format(s),
            name = f"\"{fmt_string}\".format()",
            **kwargs
        )

    def to_int(self, **kwargs) -> Self:
        return self.apply(
            func = int,
            name = "convert to int",
            **kwargs
        )

    def to_path(self, **kwargs) -> Self:
        return self.apply(
            func = Path,
            name = "convert to pathlib.Path",
            **kwargs
        )

    def to_bool(self, **kwargs) -> Self:
        return self.apply(
            func = _to_bool,
            name = "convert to bool",
            **kwargs
        )

    def to_list(self, **kwargs) -> Self:
        return self.apply(
            func = _to_list,
            name = "convert to list",
            **kwargs
        )
