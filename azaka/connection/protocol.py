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
    ThrottledError,
)
from ..tools import ResponseType

if t.TYPE_CHECKING:
    from .connector import Connector

__all__ = ("Protocol",)
logger = logging.getLogger(__name__)


class Protocol(asyncio.Protocol):
    """
    This is the [asyncio.Protocol][] that azaka implements
    to communicate with the server.

    Warning:
        This class is not meant to be used directly in any way.
    """

    __slots__ = ("_command", "_errors", "connector")

    def __init__(self, connector: Connector) -> None:
        """
        Protocol constructor.

        Args:
            connector: The connector that is used to communicate with the server.
        """
        self.connector = connector
        self._errors = {
            "filter": CommandFilterError,
            "missing": MissingFieldError,
            "badarg": BadFieldError,
            "auth": AuthorizationError,
            "gettype": UnknownGetTypeError,
            "getinfo": UnknownGetFlagError,
            "parse": CommandSyntaxError,
            "needlogin": AuthorizationError,
            "throttled": ThrottledError,
        }
        self._command: t.Optional[bytes] = None
        self.connector.push_back.set()

    @property
    def command(self) -> t.Optional[bytes]:
        """
        A property to get the first command to be sent to the server.
        This is called only once in the lifetime by the protocol and
        carries the necessary details to establish the connection.

        Returns:
            The first command to be sent to the server.
        """
        return self._command

    @command.setter
    def command(self, value: bytes) -> None:
        self._command = value

    def connection_made(self, transport: transports.Transport) -> None:  # type: ignore
        """
        The [asyncio.BaseProtocol.connection_made][] override which
        writes the first command to the transport.

        Args:
            transport: The transport that is used to communicate with the server.
        """
        transport.write(self.command)
        logger.info(f"DISPATCHED TRANSPORTER WITH {repr(self.command)}")

    def pause_writing(self) -> None:
        """
        The [asyncio.BaseProtocol.pause_writing][] override which is called when the buffer reaches
        the high watermark. This method calls [asyncio.Event.clear][] to apply backpressure
        to the server.
        """
        logger.warning("TRANSPORT IS PAUSING DUE TO BUFFER OVERFLOW.")
        self.connector.push_back.clear()

    def resume_writing(self) -> None:
        """
        The [asyncio.BaseProtocol.resume_writing][] override which is called when the buffer
        is empty enough to resume writing. This method calls [asyncio.Event.set][] to
        release backpressure from the server.
        """
        self.connector.push_back.set()
        logger.info("TRANSPORT RESUMED.")

    def data_received(self, data: bytes) -> None:
        """
        The [asyncio.Protocol.data_received][] override which is called when data is received.

        Args:
            data: The data received from the server.
        """
        logger.info("PAYLOAD RECEIVED.")
        self._direct(data)

    def connection_lost(self, _: t.Optional[Exception]) -> None:
        """
        The [asyncio.BaseProtocol.connection_lost][] override which is called
        when the connection is lost or explicitly closed.

        Args:
            _: The exception that caused the connection to be lost.
        """
        logger.info("CONNECTION CLOSED.")
        self.connector.on_disconnect.set()

    def _direct(self, data: bytes) -> None:
        """
        A method to manage the data received from the server.

        Args:
            data: The data received from the server.
        """
        response = Response(data)

        if response.type in {ResponseType.OK, ResponseType.SESSION}:
            if not self.connector.on_connect.is_set():
                self.connector.sessiontoken.set_result(response.body)
                self.connector.on_connect.set()
            else:
                self.connector.listener(payload=ResponseType.OK)

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
