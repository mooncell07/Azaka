from __future__ import annotations

import functools
import json
import typing as t

from ..exceptions import OperationNotSupportedError

if t.TYPE_CHECKING:
    from .condition import Operator

__all__ = ("ConditionProxy", "BoolOProxy")


class BoolOProxy:
    """
    Final parser for the expressions.

    This object takes care of parsing bitwise `AND` and the bitwise `OR` operators and also
    generates the final expression which is identical to the original expression.

    Note:
        This class is not meant to be instantiated directly.
        It is generated when any field of any [Condition](../../public/condition.md) is conditioned
        against a value.

        for example:
        ```python
        from azaka.condition import VNCondition

        print(type(VNCondition.TITLE == "fate"))
        #output: <class 'azaka.commands.proxy.BoolOProxy'>
        ```

        You can pass this object directly to `get_x` methods of [Context](../../public/context.md)
        and [Interface.set_condition](../../public/interface.md#azaka.interface.Interface.set_condition).
    """

    __slots__ = ("expression",)

    def __init__(self, expression: str) -> None:
        """
        BoolOProxy constructor.

        args:
            expression: The expression to be parsed.

        attributes:
            expression: The expression in parentheses.
        """
        self.expression: str = f"({expression})"

    def __and__(self, value: BoolOProxy) -> BoolOProxy:
        """
        Does an inplace bitwise `AND` operation and Returns the `BoolOProxy` object.
        The expression will look like `(exprA and exprB)` in string form.
        """
        self.expression = f"({self.expression} and {value.expression})"
        return self

    def __or__(self, value: BoolOProxy) -> BoolOProxy:
        """
        Does an inplace bitwise `OR` operation and Returns the `BoolOProxy` object.
        The expression will look like `(exprA or exprB)` in string form.
        """
        self.expression = f"({self.expression} or {value.expression})"
        return self

    def __repr__(self) -> str:
        """
        Returns the string representation of the expression.
        """
        return self.expression

    def __str__(self) -> str:
        """
        Returns the string representation of the expression.
        """
        return self.expression


class ConditionProxy:
    """
    An object which takes care of parsing binary expressions which consist of
    Relational Operators and the special operator `%` for searching.
    """

    __slots__ = ("name", "operator")

    def __init__(self, attr_name: str, operator: Operator) -> None:
        """
        ConditionProxy constructor.

        args:
            attr_name: The name of the field.
            operator: The [Operator](../../public/condition.md#azaka.commands.condition.Operator)
                      instance to be used.
        """
        self.name = attr_name
        self.operator = operator

    def analyze(arg: str):  # type: ignore
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
        """
        Returns a [BoolOProxy](./#azaka.commands.proxy.BoolOProxy) object with the expression `field = value`.
        """
        return BoolOProxy(f"{self.name} = {value}")

    @analyze("!=")
    def __ne__(self, value: t.Any):
        """
        Returns a [BoolOProxy](./#azaka.commands.proxy.BoolOProxy) object with the expression `field != value`.
        """
        return BoolOProxy(f"{self.name} != {value}")

    @analyze("<")
    def __lt__(self, value: t.Any) -> BoolOProxy:
        """
        Returns a [BoolOProxy](./#azaka.commands.proxy.BoolOProxy) object with the expression `field < value`.
        """
        return BoolOProxy(f"{self.name} < {value}")

    @analyze("<=")
    def __le__(self, value: t.Any) -> BoolOProxy:
        """
        Returns a [BoolOProxy](./#azaka.commands.proxy.BoolOProxy) object with the expression `field <= value`.
        """
        return BoolOProxy(f"{self.name} <= {value}")

    @analyze(">")
    def __gt__(self, value: t.Any) -> BoolOProxy:
        """
        Returns a [BoolOProxy](./#azaka.commands.proxy.BoolOProxy) object with the expression `field > value`.
        """
        return BoolOProxy(f"{self.name} > {value}")

    @analyze(">=")
    def __ge__(self, value: t.Any) -> BoolOProxy:
        """
        Returns a [BoolOProxy](./#azaka.commands.proxy.BoolOProxy) object with the expression `field >= value`.
        """
        return BoolOProxy(f"{self.name} >= {value}")

    @analyze("~")
    def __mod__(self, value: t.Any) -> BoolOProxy:
        """
        Returns a [BoolOProxy](./#azaka.commands.proxy.BoolOProxy) object with the expression `field ~ value`.
        """
        return BoolOProxy(f"{self.name} ~ {value}")
