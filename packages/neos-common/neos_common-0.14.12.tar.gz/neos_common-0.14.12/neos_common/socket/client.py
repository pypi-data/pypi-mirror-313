import asyncio
import json
import logging
import socket
import time

from neos_common import error
from neos_common.socket import util

logger = logging.getLogger(__name__)


class AsyncTCPClient:
    """Base implementation for asyncio stream socket service client."""

    def __init__(
        self,
        host: str,
        port: int,
        encoder: type[json.JSONEncoder] | None = None,
    ) -> None:
        """TCPClient instantiator.

        Args:
        ----
        host: socket service host name
        port: socket service port
        encoder: json encoder for request messages
        """
        self.addr = (host, port)
        self.encoder = encoder

    async def send_request(self, request: dict) -> dict:
        """Send a request to socket service.

        Handle socket connection errors, and response timeouts.
        """
        try:
            reader, writer = await asyncio.open_connection(*self.addr)
            async_socket = util.AsyncSocket(reader, writer)
        except OSError as e:
            raise error.ServiceConnectionError(
                message="Unable to connect to service.",
                debug=f"{self.addr}: {e!s}",
            ) from e

        try:
            async_socket.write(util.encode(request, encoder=self.encoder))
            response = await async_socket.read()
        finally:
            async_socket.close()

        return response


class TCPClient:
    """Base implementation for socket service client."""

    def __init__(
        self,
        host: str,
        port: int,
        timeout: int = 10,
        wait: int = 10,
        encoder: type[json.JSONEncoder] | None = None,
    ) -> None:
        """TCPClient instantiator.

        Args:
        ----
        host: socket service host name
        port: socket service port
        timeout: number of seconds to wait for a connection
        wait: number of seconds to wait for a response from service
        encoder: json encoder for request messages
        """
        self.addr = (host, port)
        self.timeout = timeout
        self.wait = wait
        self.encoder = encoder

    def send_request(self, request: dict) -> dict:
        """Send a request to socket service.

        Handle socket connection errors, and response timeouts.
        """
        t0 = time.time()
        try:
            sock = socket.create_connection(
                self.addr,
                timeout=self.timeout,
            )
        except socket.gaierror as e:
            raise error.ServiceConnectionError(
                message="Unable to connect to service.",
                debug=f"{self.addr}: {e!s}",
            ) from e

        try:
            util.send_msg(sock, util.encode(request, encoder=self.encoder))
            t0 = time.time()
            response = None
            while not response:
                try:
                    response = util.decode(util.recv_msg(sock))
                except Exception as e:
                    raise error.ServiceConnectionError(
                        message="Unable to process request to service.",
                        debug=f"{self.addr}: {e.__class__.__name__}({e!s})",
                    ) from e
                if time.time() - t0 > self.wait:
                    msg = "Timed out waiting for resp."
                    raise TimeoutError(msg)
        finally:
            sock.close()
        return response
