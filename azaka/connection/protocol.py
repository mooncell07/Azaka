import asyncio
import logging
import typing as t
from asyncio import transports

from ..workers import parse_response

__all__ = ("Protocol",)


class Protocol(asyncio.Protocol):

    __slots__ = ("_subscriber", "command", "logger", "on_connect", "on_disconnect")

    def __init__(self, command: bytes, *event: asyncio.Event) -> None:
        self.command = command
        self.on_connect, self.on_disconnect = event
        self.logger: logging.Logger = logging.getLogger(__name__)
        self._subscriber: t.Optional[t.Callable[[str], t.NoReturn]] = None

    @property
    def subscriber(self):
        return self._subscriber

    @subscriber.setter
    def subscriber(self, value: t.Callable[[str], t.NoReturn]):
        self._subscriber = value
        return self._subscriber

    def connection_made(self, transport: transports.Transport) -> None:  # type: ignore
        self.logger.info(
            f"ESTABLISHING CONNECTION WITH {repr(transport.get_extra_info('socket'))}"
        )
        transport.write(self.command)
        self.logger.info(f"DISPATCHED TRANSPORTER WITH {repr(self.command)}")

    def data_received(self, data: bytes) -> None:
        self.logger.info("PAYLOAD RECEIVED.")
        msg = parse_response(data)
        if msg == "ok":
            self.logger.info("LOGGED IN.")
            self.on_connect.set()
        else:
            self.subscriber(msg)

    def connection_lost(self, exc: t.Optional[Exception]) -> None:
        if exc is None:
            self.logger.info("CONNECTION CLOSED.")
        else:
            self.logger.exception(
                f"CONNECTION WAS CLOSED BY THE SERVER WITH EXCEPTION -> {exc}"
            )
        self.on_disconnect.set()
