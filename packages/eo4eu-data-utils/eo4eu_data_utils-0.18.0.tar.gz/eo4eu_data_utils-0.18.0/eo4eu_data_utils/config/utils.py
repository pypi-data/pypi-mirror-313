from typing import Any

from .model import Filler, Source
from .result import Result


def _to_list(input: Any) -> list:
    try:
        return list(input)
    except Exception:
        return [input]


def _to_bool(input: Any) -> bool:
    if isinstance(input, bool):
        return input
    if isinstance(input, str):
        input_lower = input.lower()
        if input_lower == "true" or input_lower == "1":
            return True
        else:
            return False
    if isinstance(input, int):
        return False if input == 0 else True
    return False


def _get_nested(dict_like: dict, keys: list[str]) -> Any:
    result = dict_like
    for key in keys:
        result = result[key]
    return result


def _set_nested(dict_like: dict, keys: list[str], value: Any):
    head, tail = keys[:-1], keys[-1]
    result = dict_like
    for key in head:
        result = result[key]
    result[tail] = value


def _get_all_keys(dict_like: dict, root: list[str]|None = None) -> set[str]:
    if root is None:
        root = []
    result = set()
    for key, val in dict_like.items():
        full_key = root + [key]
        try:
            result = result | _get_all_keys(val, root = full_key)
        except Exception:
            result.add("/".join(full_key))
    return result
# 
# 
# def _fill_recursive(source: Source, input: Result) -> Result:
#     if input.is_err():
#         return input
# 
#     input_val = input.get()
#     if not isinstance(input_val, Filler):
#         return input
# 
#     return _fill_recursive(source, input_val.fill(source, input))
