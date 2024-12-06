import traceback

from eo4eu_base_utils.typing import Self, Any


class Result:
    PRINT_EXCEPTIONS = False
    NDASH = 25

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
    def err(cls, error: str) -> Self:
        if cls.PRINT_EXCEPTIONS:
            fmt_exc = traceback.format_exc()
            if fmt_exc != "NoneType: None":
                error += "\n".join([
                    f"\n{cls.NDASH*'-'} BEGIN EXCEPTION {cls.NDASH*'-'}",
                    fmt_exc,
                    f"{cls.NDASH*'-'}- END EXCEPTION -{cls.NDASH*'-'}\n",
                ])
        return Result(is_ok = False, value = None, stack = [error])

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

    def merge(self, acc, other: Self) -> Self:
        if self.is_ok() and other.is_ok():
            return Result(
                is_ok = True,
                value = acc(self.get(), other.get()),
                stack = self._stack + other._stack
            )
        else:
            return Result(
                is_ok = self.is_ok() or other.is_ok(),
                value = self.get() if self.is_ok() else other.get(),
                stack = self._stack + other._stack
            )

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self._is_ok

    def stack(self) -> list[str]:
        return self._stack

    def fmt_err(self) -> str:
        return "".join(self._stack)

    def log_warnings(self, logger) -> Self:
        for msg in self._stack:
            logger.warning(msg)
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
