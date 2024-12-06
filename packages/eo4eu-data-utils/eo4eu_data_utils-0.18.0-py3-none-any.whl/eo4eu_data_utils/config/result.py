import logging
from pprint import pformat

from eo4eu_base_utils.typing import Self, Any, Iterator, Callable


class Result:
    def __init__(self, is_ok: bool, value: Any, stack: list[str]):
        self._is_ok = is_ok
        self._value = value
        self._stack = stack

    @classmethod
    def none(cls) -> Self:
        return Result(is_ok = False, value = None, stack = [])

    @classmethod
    def ok(cls, value: Any) -> Self:
        return Result(is_ok = True, value = value, stack = [])

    @classmethod
    def err(cls, *errors: str) -> Self:
        return Result(is_ok = False, value = None, stack = list(errors))

    @classmethod
    def merge_until_err(cls, input_iter: Iterator[Self]) -> Self:
        result = []
        for input in input_iter:
            if input.is_err():
                return input
            result.append(input.get())
        return Result.ok(result)

    def then(self, other: Self) -> Self:
        return Result(
            is_ok = other.is_ok(),
            value = other.get(),
            stack = self._stack + other._stack
        )

    def then_ok(self, value: Any) -> Self:
        return self.then(Result.ok(value))

    def then_err(self, *errors: str) -> Self:
        return self.then(Result.err(*errors))

    def then_try(self, other: Self) -> Self:
        if other.is_ok():
            return self.then(other)
        else:
            return self

    def then_benign_err(self, error: str) -> Self:
        return Result(
            is_ok = self.is_ok(),
            value = self.get(),
            stack = self._stack + [error]
        )

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self._is_ok

    def stack(self) -> list[str]:
        return self._stack

    def log(self, logger: logging.Logger, level: int = logging.WARNING) -> Self:
        for msg in self._stack:
            logger.log(level, msg)
        return self

    def get(self) -> Any:
        return self._value

    def get_or(self, default: Any) -> Any:
        if not self.is_ok():
            return default
        return self.get()

    def unwrap(self) -> Any:
        if not self.is_ok():
            raise ValueError("\n".join(self._stack))
        return self.get()

    def apply_if_ok(self, func: Callable[[Any],Any]) -> Self:
        if self.is_err():
            return self
        try:
            return self.then_ok(func(self.get()))
        except Exception as e:
            return self.then_err(str(e))

    def __repr__(self) -> str:
        if self.is_ok():
            return f"Result.ok({pformat(self.get())})"
        else:
            return "Result.err"
