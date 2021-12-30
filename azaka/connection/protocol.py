from __future__ import annotations

import asyncio
import logging
import contextlib
import queue
import typing as t
from asyncio import transports

from ..commands import Response
from ..exceptions import (
    AuthorizationError,
    BadFieldError,
    CommandFilterError,
    CommandSyntaxError,
    InvalidResponseTypeError,
    MissingFieldError,
    UnknownGetFlagError,
    UnknownGetTypeError,
)
from ..tools import ResponseType

if t.TYPE_CHECKING:
    from .connector import Connector

__all__ = ("Protocol",)
logger = logging.getLogger(__name__)


class Protocol(asyncio.Protocol):

    __slots__ = ("_command", "_errors", "connector")

    def __init__(self, connector: Connector) -> None:
        self.connector = connector
        self._errors = {
            "filter": CommandFilterError,
            "missing": MissingFieldError,
            "badarg": BadFieldError,
            "auth": AuthorizationError,
            "gettype": UnknownGetTypeError,
            "getinfo": UnknownGetFlagError,
            "parse": CommandSyntaxError,
        }
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
        self._direct(data)

    def _direct(self, data: bytes) -> None:
        response = Response(data)

        if response.type in {ResponseType.OK, ResponseType.SESSION}:
            self.connector.sessiontoken.set_result(response.body)
            self.connector.on_connect.set()

        elif response.type in {ResponseType.RESULTS, ResponseType.DBSTATS}:
            if isinstance(response.body, dict):
                self.connector.listener(payload=response.body)

        elif response.type == ResponseType.ERROR:
            if isinstance(response.body, dict):
                error = self._errors[response.body["id"]](**response.body)
                self.connector.listener(exc=error)

                with contextlib.suppress(queue.Empty):
                    self.connector.on_error.get_nowait()(error)

        else:
            raise InvalidResponseTypeError(
                response.type, "Couldn't recognize the type of response."
            ) from None

    def connection_lost(self, exc: t.Optional[Exception]) -> None:
        logger.info("CONNECTION CLOSED.")
        self.connector.on_disconnect.set()
