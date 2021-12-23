# type: ignore

from functools import wraps
from .tools import VN
from .exceptions import OperationNotSupportedError

__all__ = ("VNCondition",)


class ConditionProxy:
    def __init__(self, attr: VN) -> None:
        self.attr = attr
        self.name = attr.name

    def analyze(arg):
        def wrapper(func):
            @wraps(func)
            def inner(self, func_arg):
                if arg in self.attr.value:
                    return func(self, func_arg)
                else:
                    raise OperationNotSupportedError(
                        f"{self.attr.name} doesn't support {func.__name__} operation."
                    )

            return inner

        return wrapper

    @analyze("==")
    def __eq__(self, value):
        return f"{self.name} = {value}"

    @analyze("!=")
    def __ne__(self, value):
        return f"{self.name} != {value}"

    @analyze("<")
    def __lt__(self, value):
        return f"{self.name} < {value}"

    @analyze("<=")
    def __le__(self, value):
        return f"{self.name} <= {value}"

    @analyze(">")
    def __gt__(self, value):
        return f"{self.name} > {value}"

    @analyze(">=")
    def __ge__(self, value):
        return f"{self.name} >= {value}"


class VNCondition:
    def __init__(self) -> None:
        self.id = ConditionProxy(VN.id)

    @property
    def AND(self):
        return "AND"

    @property
    def OR(self):
        return "OR"

    def __getitem__(self, items):
        expr_list = []
        for i, v in enumerate(items):

            if v == "AND":
                expr_list.append("and")

            elif v == "OR":
                expr_list.append("or")

            else:
                expr_list.append(v)

        return " ".join(expr_list)
