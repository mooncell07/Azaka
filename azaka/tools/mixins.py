import asyncio
import queue
import typing as t
import inspect

__all__ = ("QueueControlMixin", "ReprMixin")


class QueueControlMixin:
    __slots__ = ("future_queue", "on_error", "on_connect", "on_disconnect")

    def __init__(self) -> None:
        self.future_queue: queue.Queue = queue.Queue()

        self.on_error: queue.Queue = queue.Queue()
        self.on_connect: asyncio.Event = asyncio.Event()
        self.on_disconnect: asyncio.Event = asyncio.Event()

    def listener(self, payload: t.Mapping[t.Any, t.Any]) -> None:
        future = self.future_queue.get_nowait()
        future.set_result(payload)

    def error_listener(self, func: t.Callable) -> None:
        self.on_error.put_nowait(func)


class ReprMixin:
    def __init__(self, obj) -> None:
        self.obj = obj

    def __repr__(self) -> str:
        return self._make_repr()

    def _make_repr(self) -> str:
        attrs = [
            attr
            for attr in inspect.getmembers(self)
            if not inspect.ismethod(attr[1])
            if not attr[0].startswith("_")
        ]
        fmt = ", ".join(f"{attr}={repr(value)}" for attr, value in attrs)
        return f"{self.__class__.__name__}({fmt})"
