#  type: ignore

import functools
import json
import typing as t
from .enums import VN
from ..exceptions import OperationNotSupportedError

__all__ = ("ConditionProxy",)


class BoolOProxy:
    def __init__(self, expression) -> None:
        self.expression = f"({expression})"

    def __and__(self, value):
        self.expression = f"({self.expression} and {value.expression})"
        return self

    def __or__(self, value):
        self.expression = f"({self.expression} or {value.expression})"
        return self


class ConditionProxy:
    def __init__(self, attr: VN) -> None:
        self.attr = attr
        self.name = attr.name

        self.clean_name = attr.name.replace("_array", "")

    def analyze(arg):
        def wrapper(func):
            @functools.wraps(func)
            def inner(self, func_arg):
                if arg in self.attr.value.symbols:
                    return func(self, json.dumps(func_arg))
                else:
                    raise OperationNotSupportedError(
                        f"{self.name} doesn't support {func.__name__} operation."
                    )

            return inner

        return wrapper

    @analyze("=")
    def __eq__(self, value):
        return BoolOProxy(f"{self.clean_name} = {value}")

    @analyze("!=")
    def __ne__(self, value):
        return BoolOProxy(f"{self.clean_name} != {value}")

    @analyze("<")
    def __lt__(self, value):
        return BoolOProxy(f"{self.clean_name} < {value}")

    @analyze("<=")
    def __le__(self, value):
        return BoolOProxy(f"{self.clean_name} <= {value}")

    @analyze(">")
    def __gt__(self, value):
        return BoolOProxy(f"{self.clean_name} > {value}")

    @analyze(">=")
    def __ge__(self, value):
        return BoolOProxy(f"{self.clean_name} >= {value}")

    @analyze("~")
    def __mod__(self, value):
        return BoolOProxy(f"{self.clean_name} ~ {value}")
