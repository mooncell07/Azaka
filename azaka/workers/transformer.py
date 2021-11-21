import json
import typing as t

__all__ = ("Transformer",)


class Transformer:

    __slots__ = ("data", "terminator")

    def __init__(self, *, data: t.Union[t.Mapping[t.Any, t.Any], str, bytes]) -> None:
        self.data = data
        self.terminator = b"\x04"

    def to_bytes(self) -> bytes:
        if isinstance(self.data, dict):
            self.data = json.dumps(self.data)
        return self.data.encode()  # type: ignore

    def to_dict(self) -> t.Optional[t.Mapping[t.Any, t.Any]]:
        if isinstance(self.data, str) or isinstance(self.data, bytes):
            return json.loads(self.data)
        return None

    def command_formation(self, command: str, **arguments: t.Any) -> bytes:
        if arguments:
            self.data = arguments
        fmt = command.encode() + self.to_bytes() + self.terminator
        return fmt
