from __future__ import annotations

import asyncio
import logging
import typing as t
from asyncio import transports

from ..exceptions import InvalidResponseTypeError
from ..tools import parse_response

__all__ = ("Protocol",)
logger = logging.getLogger(__name__)


class Protocol(asyncio.Protocol):

    __slots__ = ("_subscriber", "command", "on_connect", "on_disconnect")

    def __init__(
        self, command: bytes, on_connect: asyncio.Event, on_disconnect: asyncio.Event
    ) -> None:
        self._subscriber: t.Optional[t.Callable[[str], t.NoReturn]] = None
        self.command = command
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect

    @property
    def subscriber(self):
        return self._subscriber

    @subscriber.setter
    def subscriber(self, value: t.Callable[[str], t.NoReturn]) -> None:
        self._subscriber = value

    def connection_made(self, transport: transports.Transport) -> None:  # type: ignore
        logger.info(
            f"ESTABLISHING CONNECTION WITH {repr(transport.get_extra_info('socket'))}"
        )
        transport.write(self.command)
        logger.info(f"DISPATCHED TRANSPORTER WITH {repr(self.command)}")

    def data_received(self, data: bytes) -> None:
        logger.info("PAYLOAD RECEIVED.")
        response = parse_response(data)

        if response.type == "ok":
            logger.info("LOGGED IN.")
            self.on_connect.set()

        elif (response.type == "results") or (response.type == "dbstats"):
            self.subscriber(response.data)

        else:
            self.on_disconnect.set()
            raise InvalidResponseTypeError(
                response.type, "Couldn't recognize the type of response."
            ) from None

    def connection_lost(self, exc: t.Optional[Exception]) -> None:
        if exc is None:
            logger.info("CONNECTION CLOSED.")
        else:
            logger.exception(
                f"CONNECTION WAS CLOSED BY THE SERVER WITH EXCEPTION -> {exc}"
            )
        self.on_disconnect.set()
