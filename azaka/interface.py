from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from .commands import VNCondition, BoolOProxy

__all__ = ("Interface",)


class Interface:
    __slots__ = ("condition", "_conditions")

    def __init__(self, type_: str) -> None:
        if type_ == "VN":
            self.condition = VNCondition

        self._conditions: t.List[BoolOProxy] = []

    def __enter__(self) -> Interface:
        return self

    def __exit__(self, type, value, traceback) -> None:
        ...

    def set_condition(self, item: VNCondition) -> None:
        self._conditions.extend(item._exprs)
