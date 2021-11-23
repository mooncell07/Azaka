from __future__ import annotations

import json
import typing as t
from json.decoder import JSONDecodeError

__all__ = ("TERMINATOR", "make_command", "parse_response")

TERMINATOR = "\x04"


def parse_response(data: bytes) -> t.Union[t.Mapping[t.Any, t.Any], str]:
    decoded = data.decode().rstrip(TERMINATOR)
    mapping = decoded.split()
    try:
        return json.loads(mapping[1])
    except (JSONDecodeError, IndexError):
        return decoded


def make_command(name: str, **args: t.Any) -> bytes:
    if args:
        newargs = json.dumps(args["args"])
        cmd = name + newargs + TERMINATOR
    else:
        cmd = name + TERMINATOR
    return cmd.encode()
