from __future__ import annotations

import typing as t

from .commands import _condition_selector
from .tools import Flags, Type

if t.TYPE_CHECKING:
    from .commands import BoolOProxy


__all__ = ("Interface",)


class Interface:

    __slots__ = ("_condition", "_type", "_flags", "condition", "_options")

    def __init__(self, type: Type, flags: t.Optional[t.Iterable[Flags]] = None) -> None:
        self.condition = _condition_selector(type)

        self._type: Type = type
        self._condition: t.Optional[BoolOProxy] = None
        self._flags: t.Optional[t.Iterable[Flags]] = flags
        self._options: t.Optional[t.Mapping[str, t.Any]] = None

    def __enter__(self) -> Interface:
        return self

    def __exit__(self, *ex) -> None:
        ...

    def set_condition(self, item: BoolOProxy) -> None:
        if not self._condition:
            self._condition = item
        else:
            raise ValueError(
                "This interface only supports single filter (condition) expression."
            )

    def add_option(self, **kwargs: t.Any) -> None:
        self._options = kwargs

    @property
    def set_flags(self) -> t.Optional[t.Iterable[Flags]]:
        return self._flags

    @set_flags.setter
    def set_flags(self, item: t.Iterable[Flags]) -> None:
        if not self._flags:
            self._flags = item
        else:
            raise ValueError("This interface already has a flag set.")
