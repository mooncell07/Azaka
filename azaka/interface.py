from __future__ import annotations

import typing as t

from .commands.condition import VNCondition
from .tools import TERMINATOR, Flags, Type

if t.TYPE_CHECKING:
    from .commands import BoolOProxy


__all__ = ("Interface",)


class Interface:
    __slots__ = ("condition", "_condition", "_type", "_flags")

    def __init__(self, type: Type, flags: t.Optional[t.Iterable[Flags]] = None) -> None:
        if type.name == "VN":
            self.condition = VNCondition

        self._type: Type = type
        self._condition: t.Optional[BoolOProxy] = None

        self._flags: t.Optional[t.Iterable[Flags]] = flags

    def __enter__(self) -> Interface:
        return self

    def __exit__(self, *ex) -> None:
        ...

    def _to_command(self) -> bytes:

        if self._flags and self._condition:
            flags = ",".join(i.value for i in self._flags)
            formation = f"get {self._type.value} {flags} {self._condition.expression}{TERMINATOR}"
            return formation.encode()
        else:
            raise NotImplementedError

    def set_condition(self, item: BoolOProxy) -> None:
        if not self._condition:
            self._condition = item
        else:
            raise ValueError(
                "This interface only supports single filter (condition) expression."
            )

    @property
    def set_flags(self) -> t.Optional[t.Iterable[Flags]]:
        return self._flags

    @set_flags.setter
    def set_flags(self, item: t.Iterable[Flags]) -> None:
        if not self._flags:
            self._flags = item
        else:
            raise ValueError("This interface already has a flag set.")
