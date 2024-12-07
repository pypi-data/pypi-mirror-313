import importlib.metadata
from unittest import mock

import pydantic
import pytest

from neos_common.socket import server, util
from tests.conftest import AsyncMock

RAW_MESSAGE = b'{"hello": "world"}'
MESSAGE_HEADER = b"\x00\x00\x00\x12"

PYDANTIC_VERSION = ".".join(importlib.metadata.version("pydantic").split(".")[:2])


class RequestData(pydantic.BaseModel):
    name: str


class DummyTCPHandler(server.TCPHandler):
    def setup(self):
        self.request_mapping = {
            "test": RequestData,
        }


class TestTCPHandler:
    def test_handle_invalid_request(self):
        request = mock.Mock()
        request.recv.side_effect = [
            MESSAGE_HEADER,
            b'{"hello": "world"}',
        ]

        DummyTCPHandler(request, None, None)

        assert request.sendall.call_args == mock.call(
            b"\x00\x00\x01\xb7"
            + bytes(
                f'{{"ok": false, "status": "unprocessible-entity", "reason": "ValidationError", "message": "Unable to parse message.", "debug": null, "details": [{{"type": "missing", "loc": ["request_type"], "msg": "Field required", "input": {{"hello": "world"}}, "url": "https://errors.pydantic.dev/{PYDANTIC_VERSION}/v/missing"}}, {{"type": "missing", "loc": ["data"], "msg": "Field required", "input": {{"hello": "world"}}, "url": "https://errors.pydantic.dev/{PYDANTIC_VERSION}/v/missing"}}]}}',
                "utf-8",
            ),
        )

    def test_handle_invalid_request_data(self):
        request = mock.Mock()
        request.recv.side_effect = [
            MESSAGE_HEADER,
            b'{"request_type": "test", "data": {}}',
        ]

        DummyTCPHandler(request, None, None)

        assert request.sendall.call_args == mock.call(
            b"\x00\x00\x01\x0f"
            + bytes(
                f'{{"ok": false, "status": "unprocessible-entity", "reason": "ValidationError", "message": "Unable to parse message.", "debug": null, "details": [{{"type": "missing", "loc": ["name"], "msg": "Field required", "input": {{}}, "url": "https://errors.pydantic.dev/{PYDANTIC_VERSION}/v/missing"}}]}}',
                "utf-8",
            ),
        )

    def test_handle_receive_exception(self):
        request = mock.Mock()
        request.recv.side_effect = Exception

        DummyTCPHandler(request, None, None)

        assert request.sendall.call_args == mock.call(
            b'\x00\x00\x00j{"ok": false, "status": "unhandled", "reason": "Unhandled", "message": "", "debug": null, "details": null}',
        )

    def test_handle_process_exception(self, monkeypatch):
        request = mock.Mock()
        request.recv.side_effect = [
            MESSAGE_HEADER,
            b'{"request_type": "test", "data": {}}',
        ]
        monkeypatch.setattr(DummyTCPHandler, "request_mapping", None)
        monkeypatch.setattr(DummyTCPHandler, "setup", mock.Mock())

        DummyTCPHandler(request, None, None)

        assert request.sendall.call_args == mock.call(
            b'\x00\x00\x00\x92{"ok": false, "status": "unhandled", "reason": "Unhandled", "message": "\'NoneType\' object has no attribute \'get\'", "debug": null, "details": null}',
        )

    def test_request_handled(self, monkeypatch):
        request = mock.Mock()
        request.recv.side_effect = [
            MESSAGE_HEADER,
            b'{"request_type": "test", "data": {"name": "testdata"}}',
        ]

        mock_handle = mock.Mock()
        monkeypatch.setattr(DummyTCPHandler, "_handle", mock_handle)

        DummyTCPHandler(request, None, None)

        assert mock_handle.call_args == mock.call(request, "test", RequestData(name="testdata"))


@pytest.fixture
def handler():
    return server.AsyncTCPHandler()


class TestAsyncHandler:
    async def test_non_json_read(self, handler):
        reader, writer = AsyncMock(), mock.Mock()
        reader.read.side_effect = [
            MESSAGE_HEADER,
            b'("hello", "world")',
        ]

        await handler(reader, writer)

        assert writer.write.call_args == mock.call(
            b'\x00\x00\x00\xa0{"ok": false, "status": "unprocessible-entity", "reason": "DecodeError", "message": "Expecting value: line 1 column 1 (char 0)", "debug": null, "details": null}',
        )

    async def test_exception_read(self, handler):
        reader, writer = AsyncMock(), mock.Mock()
        reader.read.side_effect = Exception("exception")

        await handler(reader, writer)

        assert writer.write.call_args == mock.call(
            b'\x00\x00\x00s{"ok": false, "status": "unhandled", "reason": "Unhandled", "message": "exception", "debug": null, "details": null}',
        )

    async def test_data_validation_error(self, handler):
        reader, writer = AsyncMock(), mock.Mock()
        reader.read.side_effect = [
            MESSAGE_HEADER,
            b'{"hello": "world"}',
        ]

        await handler(reader, writer)

        assert writer.write.call_args == mock.call(
            b"\x00\x00\x01\xb7"
            + bytes(
                f'{{"ok": false, "status": "unprocessible-entity", "reason": "ValidationError", "message": "Unable to parse message.", "debug": null, "details": [{{"type": "missing", "loc": ["request_type"], "msg": "Field required", "input": {{"hello": "world"}}, "url": "https://errors.pydantic.dev/{PYDANTIC_VERSION}/v/missing"}}, {{"type": "missing", "loc": ["data"], "msg": "Field required", "input": {{"hello": "world"}}, "url": "https://errors.pydantic.dev/{PYDANTIC_VERSION}/v/missing"}}]}}',
                "utf-8",
            ),
        )

    async def test_processing_exception(self, handler):
        reader, writer = AsyncMock(), mock.Mock()
        reader.read.side_effect = [
            MESSAGE_HEADER,
            b'{"request_type": "test", "data": {"hello": "world"}}',
        ]
        handler.request_mapping = {"test": list}

        await handler(reader, writer)

        assert writer.write.call_args == mock.call(
            b'\x00\x00\x00\x8b{"ok": false, "status": "unhandled", "reason": "Unhandled", "message": "list() takes no keyword arguments", "debug": null, "details": null}',
        )

    async def test_valid_request_handled(self, handler, monkeypatch):
        reader, writer = AsyncMock(), mock.Mock()
        asocket = util.AsyncSocket(reader, writer)
        monkeypatch.setattr(util, "AsyncSocket", mock.Mock(return_value=asocket))
        reader.read.side_effect = [
            MESSAGE_HEADER,
            b'{"request_type": "test", "data": {"hello": "world"}}',
        ]
        monkeypatch.setattr(handler, "_handle", AsyncMock(return_value=None))
        handler.request_mapping = {}

        await handler(reader, writer)

        assert handler._handle.call_args == mock.call(asocket, "test", {"hello": "world"})
