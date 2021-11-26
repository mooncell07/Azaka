import asyncio
import queue
import typing as t

__all__ = ("QueueControlMixin",)


class QueueControlMixin:
    __slots__ = ("condition_queue", "response_queue", "on_connect", "on_disconnect")

    def __init__(self) -> None:
        self.condition_queue: queue.Queue = queue.Queue()
        self.response_queue: queue.Queue = queue.Queue()

        self.on_connect: asyncio.Event = asyncio.Event()
        self.on_disconnect: asyncio.Event = asyncio.Event()

    def listener(self, payload: t.Mapping[t.Any, t.Any]) -> None:
        self.response_queue.put(payload)
        condition = self.condition_queue.get_nowait()
        condition.release()
