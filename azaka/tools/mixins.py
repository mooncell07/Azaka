import asyncio
import queue
import typing as t

__all__ = ("QueueControlMixin",)


class QueueControlMixin:
    __slots__ = ("future_queue", "on_connect", "on_disconnect")

    def __init__(self) -> None:
        self.future_queue: queue.Queue = queue.Queue()

        self.on_connect: asyncio.Event = asyncio.Event()
        self.on_disconnect: asyncio.Event = asyncio.Event()

    def listener(self, payload: t.Mapping[t.Any, t.Any]) -> None:
        future = self.future_queue.get_nowait()
        future.set_result(payload)
