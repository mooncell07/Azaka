import asyncio
import queue
import typing as t

__all__ = ("QueueControlMixin",)


class QueueControlMixin:
    __slots__ = ("future_queue", "on_error", "on_connect", "on_disconnect")

    def __init__(self) -> None:
        self.future_queue: queue.Queue = queue.Queue()

        self.on_error: queue.Queue = queue.Queue(maxsize=1)
        self.on_connect: asyncio.Event = asyncio.Event()
        self.on_disconnect: asyncio.Event = asyncio.Event()

    def listener(
        self,
        *,
        payload: t.Optional[t.Union[t.Mapping[t.Any, t.Any], t.Any]] = None,
        exc: t.Optional[Exception] = None,
    ) -> None:
        future = self.future_queue.get_nowait()
        if exc is not None:
            future.set_exception(exc)
        else:
            future.set_result(payload)

    def error_listener(self, func: t.Callable) -> None:
        self.on_error.put_nowait(func)
