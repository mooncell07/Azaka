import asyncio
import queue
import typing as t

__all__ = ("QueueControlMixin",)


class QueueControlMixin:
    """
    A mixin that manages internal queues and events for [Connector](../connection/connector.md).

    Warning:
        pls don't play with it
    """

    __slots__ = ("future_queue", "on_error", "on_connect", "on_disconnect", "push_back")

    def __init__(self) -> None:
        """
        QueueControlMixin Constructor.

        Attributes:
            future_queue: A [queue.Queue][] holding [asyncio.Future][] objects which are waiting for a response.
            on_error: A [queue.Queue][] holding function that will be called when an error occurs in [Protocol[].
            on_connect: An [asyncio.Event][] that will be set when the connection is established.
            on_disconnect: An [asyncio.Event][] that will be set when the connection is closed.
        """
        self.future_queue: queue.Queue = queue.Queue()

        self.on_error: queue.Queue = queue.Queue(maxsize=1)
        self.on_connect: asyncio.Event = asyncio.Event()
        self.on_disconnect: asyncio.Event = asyncio.Event()

        self.push_back: asyncio.Event = asyncio.Event()

    def listener(
        self,
        *,
        payload: t.Optional[t.Union[t.Mapping[t.Any, t.Any], t.Any]] = None,
        exc: t.Optional[Exception] = None,
    ) -> None:
        """
        A listener that is called by the [Protocol](../connection/protocol.md) when a response is received.
        This method gets the [asyncio.Future][] from the `future_queue` and sets a result/exception to it.

        Args:
            payload: The payload received from the API.
            exc: The exception that occurred.
        """
        future = self.future_queue.get_nowait()
        if exc is not None:
            future.set_exception(exc)
        else:
            future.set_result(payload)

    def error_listener(self, func: t.Callable) -> None:
        """
        A method that puts the error handler in the `on_error` queue.

        Args:
            func: The function to be called when an error occurs.
        """
        self.on_error.put_nowait(func)

    async def drain(self) -> None:
        """
        A coroutine that waits for the `push_back` event to be set.
        """
        await self.push_back.wait()
