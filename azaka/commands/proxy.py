from __future__ import annotations

import functools
import json
import typing as t
from ..exceptions import OperationNotSupportedError

if t.TYPE_CHECKING:
    from .condition import Operator

__all__ = ("ConditionProxy", "BoolOProxy")


class BoolOProxy:

    __slots__ = ("expression",)

    def __init__(self, expression: str) -> None:
        self.expression = f"({expression})"

    def __and__(self, value: BoolOProxy):
        self.expression = f"({self.expression} and {value.expression})"
        return self

    def __or__(self, value: BoolOProxy):
        self.expression = f"({self.expression} or {value.expression})"
        return self


class ConditionProxy:
    def __init__(self, attr_name: str, operator: Operator) -> None:
        self.name = attr_name
        self.operator = operator

    def analyze(arg: str):
        def wrapper(func: t.Callable[[ConditionProxy, t.Any], BoolOProxy]):
            @functools.wraps(func)
            def inner(self, func_arg: t.Any) -> BoolOProxy:
                if arg in self.operator.symbols:
                    return func(self, json.dumps(func_arg))
                else:
                    raise OperationNotSupportedError(
                        f"{self.name} doesn't support {func.__name__} operation."
                    )

            return inner

        return wrapper

    @analyze("=")
    def __eq__(self, value: t.Any) -> BoolOProxy:
        return BoolOProxy(f"{self.name} = {value}")

    @analyze("!=")
    def __ne__(self, value: t.Any):
        return BoolOProxy(f"{self.name} != {value}")

    @analyze("<")
    def __lt__(self, value: t.Any) -> BoolOProxy:
        return BoolOProxy(f"{self.name} < {value}")

    @analyze("<=")
    def __le__(self, value: t.Any) -> BoolOProxy:
        return BoolOProxy(f"{self.name} <= {value}")

    @analyze(">")
    def __gt__(self, value: t.Any) -> BoolOProxy:
        return BoolOProxy(f"{self.name} > {value}")

    @analyze(">=")
    def __ge__(self, value: t.Any) -> BoolOProxy:
        return BoolOProxy(f"{self.name} >= {value}")

    @analyze("~")
    def __mod__(self, value: t.Any) -> BoolOProxy:
        return BoolOProxy(f"{self.name} ~ {value}")
