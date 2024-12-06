import asyncio
import json
import logging
import socketserver
import typing

import pydantic
import pydantic.error_wrappers

from neos_common.error import NeosException
from neos_common.socket import util

if typing.TYPE_CHECKING:
    Loc = tuple[int | str, ...]

    class _ErrorDictRequired(typing.TypedDict):
        loc: Loc
        msg: str
        type: str

    class ErrorDict(_ErrorDictRequired, total=False):
        """Type hint for pydantic.error_wrappers.ErrorDict.

        Stolen from type hints in pydantic.error_wrappers
        """

        ctx: dict[str, typing.Any]


logger = logging.getLogger(__name__)


class ValidationError(NeosException):
    status_ = "unprocessible-entity"


class AsyncTCPHandler:
    Request = util.SocketRequest

    async def setup(self) -> None: ...

    async def teardown(self) -> None: ...

    async def __call__(self, reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter) -> None:
        async_socket = util.AsyncSocket(reader, writer)
        await self.setup()
        try:
            data = await async_socket.read()
        except json.decoder.JSONDecodeError as e:
            logger.exception("Decode error processing request.")
            exc = ValidationError(
                reason="DecodeError",
                message=str(e),
                details=None,
            )
            async_socket.write(util.encode(dict(exc)))
        except Exception as e:
            logger.exception("Exception processing request.")
            exc = NeosException(
                reason="Unhandled",
                message=str(e),
            )
            async_socket.write(util.encode(dict(exc)))
        else:
            if data is None:
                await self.teardown()
                async_socket.close()
                return

            try:
                request = self.Request(**data)
                request_type = request.request_type

                RequestDataCls = self.request_mapping.get(request_type, dict)  # noqa: N806
                request_data = RequestDataCls(**request.data)
            except pydantic.ValidationError as e:
                logger.exception("Validation error processing request data.")
                exc = ValidationError(
                    reason="ValidationError",
                    message="Unable to parse message.",
                    details=e.errors(),
                )
                async_socket.write(util.encode(dict(exc)))
            except Exception as e:
                logger.exception("Exception processing request data.")
                exc = NeosException(
                    reason="Unhandled",
                    message=str(e),
                )
                async_socket.write(util.encode(dict(exc)))
            else:
                await self._handle(async_socket, request_type, request_data)

        await self.teardown()
        async_socket.close()

    async def _handle(
        self,
        sock: util.AsyncSocket,
        request_type: str,
        request_data: pydantic.BaseModel | dict,
    ) -> None: ...


class TCPHandler(socketserver.BaseRequestHandler):
    """Base handler for TCP socket server.

    When a message is received:
        * decode it
        * format it into an instance of `cls.Request`
        * pass it to the handler defined for `request.request_type` in `cls.request_mapping`

    Define the mapping between Request.request_type and handlers in `cls.request_mapping`.
    Override the default SocketRequest schema via `cls.Request`
    """

    request_mapping: typing.ClassVar[dict] = {}
    Request = util.SocketRequest

    def handle(self) -> None:
        """Handle an incoming request.

        Handle issues decoding, processing and validating request messages, on
        error response to the client, with error details.

        On success pass the validated request message to the appropriate
        handler.
        """
        try:
            data = util.decode(util.recv_msg(self.request))
        except json.decoder.JSONDecodeError as e:
            logger.exception("Decode error processing request.")
            exc = ValidationError(
                reason="DecodeError",
                message=str(e),
                details=None,
            )
            util.send_msg(self.request, util.encode(dict(exc)))
        except Exception as e:
            logger.exception("Exception processing request.")
            exc = NeosException(
                reason="Unhandled",
                message=str(e),
            )
            util.send_msg(self.request, util.encode(dict(exc)))
        else:
            if data is None:
                return

            try:
                request = self.Request(**data)
                request_type = request.request_type

                RequestDataCls = self.request_mapping.get(request_type, dict)  # noqa: N806
                request_data = RequestDataCls(**request.data)
            except pydantic.ValidationError as e:
                logger.exception("Validation error processing request data.")
                exc = ValidationError(
                    reason="ValidationError",
                    message="Unable to parse message.",
                    details=e.errors(),
                )
                util.send_msg(self.request, util.encode(dict(exc)))
            except Exception as e:
                logger.exception("Exception processing request data.")
                exc = NeosException(
                    reason="Unhandled",
                    message=str(e),
                )
                util.send_msg(self.request, util.encode(dict(exc)))
            else:
                self._handle(self.request, request_type, request_data)

    def _handle(
        self,
        sock: util.Socket,
        request_type: str,
        request_data: pydantic.BaseModel | dict,
    ) -> None: ...
