from __future__ import annotations

import json
import typing as t

from ..tools.enums import ResponseType
from ..objects import UlistLabels


try:
    import orjson  # type: ignore

    ORJ = True
except ModuleNotFoundError:
    ORJ = False


if t.TYPE_CHECKING:
    from ..interface import Interface


__all__ = ("TERMINATOR", "Command", "Response")
TERMINATOR = "\x04"


class Command:
    __slots__ = ("name", "kwargs", "interface")

    def __init__(self, name: str, **kwargs: t.Any) -> None:
        self.name = name
        self.kwargs = kwargs
        self.interface: t.Optional[Interface] = kwargs.get("interface")

    def create(self) -> bytes:
        if self.interface:
            return self._from_interface()

        elif self.kwargs:
            dumped = json.dumps(self.kwargs)
            formation = f"{self.name} {dumped}{TERMINATOR}"
            return formation.encode()

        formation = f"{self.name}{TERMINATOR}"
        return formation.encode()

    @t.no_type_check
    def _from_interface(self) -> bytes:
        self.interface._verify()
        filter_expressions = self.interface._condition.expression
        flatten_flags = ",".join(i.value for i in self.interface._flags)
        dumped_options = (
            json.dumps(self.interface._options) if self.interface._options else ""
        )

        resolved_type = (
            self.interface._type.__name__.lower()
            if self.interface._type != UlistLabels
            else "ulist-labels"
        )
        formation = (
            f"{self.name} "
            f"{resolved_type} "
            f"{flatten_flags} "
            f"{filter_expressions}"
            f"{dumped_options}"
            f"{TERMINATOR}"
        )
        return formation.encode()


class Response:

    __slots__ = ("_data", "type", "body")

    def __init__(self, data: bytes) -> None:
        self._data: str = data.decode()
        self.type: t.Optional[ResponseType] = None
        self.body: t.Optional[t.Union[t.Mapping[t.Any, t.Any], str]] = None

        self.parse()

    def parse(self) -> None:
        cleaned = self._data.rstrip(TERMINATOR)
        resp_info = cleaned.split(maxsplit=1)

        self.type = ResponseType(resp_info[0])

        if len(resp_info) > 1:
            try:
                self.body = (
                    orjson.loads(resp_info[1]) if ORJ else json.loads(resp_info[1])
                )
            except ValueError:
                self.body = resp_info[1]
        return None
