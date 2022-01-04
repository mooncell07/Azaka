from __future__ import annotations

import json
import typing as t

from ..tools.enums import ResponseType

try:
    import orjson

    ORJ = True
except ModuleNotFoundError:
    ORJ = False


__all__ = ("TERMINATOR", "Command", "Response")
TERMINATOR = "\x04"


class Command:
    __slots__ = ("name", "kwargs", "interface")

    def __init__(self, name: str, **kwargs: t.Any) -> None:
        self.name = name
        self.kwargs = kwargs
        self.interface = kwargs.get("interface", False)

    def create(self) -> bytes:
        if self.interface:
            flatten_flags = ",".join(i.value for i in self.interface._flags)
            filter_expressions = self.interface._condition.expression
            dumped_options = (
                json.dumps(self.interface._options) if self.interface._options else ""
            )

            formation = (
                f"{self.name} "
                f"{self.interface._type.value} "
                f"{flatten_flags} "
                f"{filter_expressions}"
                f"{dumped_options}"
                f"{TERMINATOR}"
            )
            return formation.encode()

        elif self.kwargs:

            dumped = json.dumps(self.kwargs)
            formation = f"{self.name} {dumped}{TERMINATOR}"
            return formation.encode()

        formation = f"{self.name}{TERMINATOR}"
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
                if ORJ:
                    self.body = orjson.loads(resp_info[1])
                else:
                    self.body = json.loads(resp_info[1])
            except ValueError:
                self.body = resp_info[1]
            return None
        return None
