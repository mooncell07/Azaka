from __future__ import annotations

import inspect
import json
import typing as t

from collections import namedtuple

__all__ = ("TERMINATOR", "make_command", "make_repr", "parse_response")
TERMINATOR = "\x04"


def make_command(name: str, **args: t.Any) -> bytes:
    if args:
        newargs = json.dumps(args["args"])
        cmd = name + newargs + TERMINATOR
    else:
        cmd = name + TERMINATOR
    return cmd.encode()


def make_repr(obj: t.Any) -> str:
    attrs = [
        attr
        for attr in inspect.getmembers(obj)
        if not inspect.ismethod(attr[1])
        if not attr[0].startswith("_")
    ]
    fmt = ", ".join(f"{attr}={repr(value)}" for attr, value in attrs)
    return f"{obj.__class__.__name__}({fmt})"


def parse_response(data: bytes):
    decoded = data.decode().rstrip(TERMINATOR)
    mapping = decoded.split(maxsplit=1)
    response = namedtuple("response", ["type", "data"])
    response.type = mapping[0]

    if len(mapping) > 1:
        response.type = mapping[0]
        try:
            response.data = json.loads(mapping[1])
        except ValueError:
            response.data = mapping[1]

    return response
