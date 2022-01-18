from __future__ import annotations

import typing as t

from .commands import _condition_selector, BaseCondition, BoolOProxy
from .tools import Flags, Labels
from .exceptions import InterfaceError


__all__ = ("Interface", "SETInterface")


class Interface:
    """
    A helper class to make it easier to create GET commands.

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
            one of the objects from
            [Objects](../public/objects/baseobject.md) yourself but not in any case the object
            should be constructed.

        Attributes:
            condition: The [Condition](../condition) type for this interface. (Automatically set based on type).
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
            predicate can be a callable which
            takes a
            [BaseCondition](../public/condition.md#azaka.commands.condition.BaseCondition) arg or a
            [BoolOProxy](../internals/commands/proxy.md#azaka.commands.proxy.BoolOProxy) object.

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


class SETInterface:
    """
    A helper class to make it easier to create SET commands.
    """

    def __init__(self, id: int, *, vote: t.Optional[int] = None) -> None:
        """
        SETInterface constructor.

        Args:
            id: The id of the item to modify.
            vote: The vote to set for the item. (Must be between 10 and 100)
        """
        self.id = id
        self._kwargs: t.MutableMapping[str, t.Any] = {"vote": vote} if vote else {}

    def __enter__(self) -> SETInterface:
        return self

    def __exit__(self, *ex) -> None:
        ...

    def write_notes(self, notes: str) -> None:
        """
        Writes notes for the item in ulist.

        Args:
            notes: The notes to write.
        """
        self._kwargs["notes"] = notes

    def started_on(self, date: str) -> None:
        """
        Sets the start date for the item.

        Args:
            date: The date to set.
        """
        self._kwargs["started"] = date

    def finished_on(self, date: str) -> None:
        """
        Sets the finish date for the item.

        Args:
            date: The date to set.
        """
        self._kwargs["finished"] = date

    def set_labels(self, *labels: Labels) -> None:
        """
        Sets the [Labels](./enums.md#azaka.tools.enums.Labels) for the item.

        Args:
            *labels: The labels to set.
        """
        self._kwargs["labels"] = labels
