from __future__ import annotations

import typing as t

from .commands import _condition_selector, BaseCondition, BoolOProxy
from .tools import Flags
from .exceptions import InterfaceError


__all__ = ("Interface",)


class Interface:
    """
    A helper class to make it easier to create commands.

    Example:
    ```python
    @client.register
    async def new(ctx: Context) -> None:
        with Interface(type=ctx.user, flags=(Flags.BASIC,)) as interface:
            interface.set_condition(lambda USER: USER.ID == 34)
        await client.get(interface)
    ```
    """

    __slots__ = (
        "_condition",
        "_flags",
        "_type",
        "_options",
        "condition",
    )

    def __init__(self, type, *, flags: t.Iterable[Flags] = ()) -> None:
        """
        The interface constructor.

        Args:
            type: The type of data to fetch from the API.
            flags: The flags to use when fetching data.

        Note:
            The [Context](./context.md) contains various `type`s that can be used or just pass
            one of the objects from [Objects](./objects) yourself but not in any case the object
            should be constructed.

        Attributes:
            condition: The [Condition]() type for this interface. (Automatically set based on type).
        """
        self.condition: t.Type[BaseCondition] = _condition_selector(type)

        self._type = type
        self._condition: t.Optional[BoolOProxy] = None
        self._flags: t.Iterable[Flags] = flags
        self._options: t.Optional[t.Mapping[str, t.Any]] = None

    def __enter__(self) -> Interface:
        return self

    def __exit__(self, *ex) -> None:
        ...

    def set_condition(
        self,
        predicate: t.Union[t.Callable[[t.Type[BaseCondition]], BoolOProxy], BoolOProxy],
    ) -> None:
        """
        Sets the condition for this interface.

        Args:
            predicate: The condition to set.

        Note:
            predicate can be a callable which takes a [BaseCondition][] arg or a [BoolOProxy]() object.

        Raises:
            InterfaceError: If the condition is already set for the interface in use.
        """
        if not self._condition:
            if isinstance(predicate, BoolOProxy):
                self._condition = predicate
            else:
                self._condition = predicate(self.condition)
        else:
            raise InterfaceError("This interface already has a condition set")

    def add_option(self, **kwargs: t.Any) -> None:
        """
        Adds options to the interface.

        Args:
            **kwargs: The options to add.
        """
        self._options = kwargs

    @property
    def flags(self) -> t.Iterable[Flags]:
        """
        Flags to use when fetching data.

        Returns:
            The flags to use when fetching data. `None` if no flags are set.
        """
        return self._flags

    @flags.setter
    def flags(self, item: t.Iterable[Flags]) -> None:
        if not self._flags:
            self._flags = item
        else:
            raise InterfaceError("This interface already has a flag set.")

    def _verify(self) -> None:
        msg = []
        if not self._condition:
            msg.append("condition")

        if not self._flags:
            msg.append("flags")

        if msg:
            raise InterfaceError(f"The attribute(s): `{', '.join(msg)}` can't be None.")
