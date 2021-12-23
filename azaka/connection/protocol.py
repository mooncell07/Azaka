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

    __slots__ = ("listener", "sessiontoken", "_command", "on_connect", "on_disconnect")

    def __init__(
        self,
        sessiontoken,
        listener: t.Callable[[t.Mapping[t.Any, t.Any]], None],
        on_connect: asyncio.Event,
        on_disconnect: asyncio.Event,
    ) -> None:
        self.listener = listener
        self.sessiontoken = sessiontoken
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect

        self._command: t.Optional[bytes] = None

    @property
    def command(self) -> t.Optional[bytes]:
        return self._command

    @command.setter
    def command(self, value: bytes) -> None:
        self._command = value

    def connection_made(self, transport: transports.Transport) -> None:  # type: ignore
        transport.write(self.command)
        logger.info(f"DISPATCHED TRANSPORTER WITH {repr(self.command)}")

    def data_received(self, data: bytes) -> None:
        logger.info("PAYLOAD RECEIVED.")
        response = parse_response(data)

        if response.type == "ok" or response.type == "session":
            logger.info("LOGGED IN.")
            self.sessiontoken.set_result(response.data)
            self.on_connect.set()

        elif (response.type == "results") or (response.type == "dbstats"):
            self.listener(response.data)
        elif response.type == "error":
            raise ValueError(response.type, response.data)
        else:
            self.on_disconnect.set()
            raise InvalidResponseTypeError(
                response.type, "Couldn't recognize the type of response."
            ) from None

    def connection_lost(self, exc: t.Optional[Exception]) -> None:
        logger.info("CONNECTION CLOSED.")
        self.on_disconnect.set()
