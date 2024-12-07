import importlib.metadata
from unittest import mock

import pydantic
import pytest

from neos_common import error
from neos_common.socket import client
from tests.conftest import AsyncMock

RAW_MESSAGE = b'{"hello": "world"}'
MESSAGE_HEADER = b"\x00\x00\x00\x12"

PYDANTIC_VERSION = ".".join(importlib.metadata.version("pydantic").split(".")[:2])


class RequestData(pydantic.BaseModel):
    name: str


class TestTCPClient:
    def test_init(self):
        c = client.TCPClient("host", "port", "timeout", "wait")

        assert c.addr == ("host", "port")
        assert c.timeout == "timeout"
        assert c.wait == "wait"

    def test_send_request_creates_connection(self, monkeypatch):
        sock = mock.Mock()
        monkeypatch.setattr(client.socket, "create_connection", mock.Mock(return_value=sock))
        monkeypatch.setattr(sock, "recv", mock.Mock(side_effect=[MESSAGE_HEADER, RAW_MESSAGE]))

        c = client.TCPClient("host", "port", 10, 1)

        c.send_request("request")

        assert client.socket.create_connection.call_args == mock.call(("host", "port"), timeout=10)

    def test_send_request_handles_connection_error(self, monkeypatch):
        monkeypatch.setattr(
            client.socket,
            "create_connection",
            mock.Mock(side_effect=client.socket.gaierror("[Err 2]: fail")),
        )

        c = client.TCPClient("host", "port", 10, 1)

        with pytest.raises(error.ServiceConnectionError) as e:
            c.send_request("request")

        assert e.value.debug == "('host', 'port'): [Err 2]: fail"
        assert e.value.message == "Unable to connect to service."

    def test_send_request_sends_message(self, monkeypatch):
        sock = mock.Mock()
        monkeypatch.setattr(client.socket, "create_connection", mock.Mock(return_value=sock))
        monkeypatch.setattr(sock, "recv", mock.Mock(side_effect=[MESSAGE_HEADER, RAW_MESSAGE]))

        c = client.TCPClient("host", "port", 10, 1)

        c.send_request("request")

        assert sock.sendall.call_args == mock.call(b'\x00\x00\x00\t"request"')

    def test_send_request_returns_response(self, monkeypatch):
        sock = mock.Mock()
        monkeypatch.setattr(client.socket, "create_connection", mock.Mock(return_value=sock))
        monkeypatch.setattr(sock, "recv", mock.Mock(side_effect=[MESSAGE_HEADER, RAW_MESSAGE]))

        c = client.TCPClient("host", "port", 10, 1)

        r = c.send_request("request")

        assert r == {"hello": "world"}

    def test_send_request_timeout(self, monkeypatch):
        sock = mock.Mock()
        monkeypatch.setattr(client.socket, "create_connection", mock.Mock(return_value=sock))
        monkeypatch.setattr(sock, "recv", mock.Mock(return_value=None))

        c = client.TCPClient("host", "port", 10, 0)

        with pytest.raises(TimeoutError):
            c.send_request("request")


class TestAsyncTCPClient:
    def test_init(self):
        c = client.AsyncTCPClient("host", "port", "encoder")

        assert c.addr == ("host", "port")
        assert c.encoder == "encoder"

    async def test_send_request_connection_error(self, monkeypatch):
        monkeypatch.setattr(client.asyncio, "open_connection", AsyncMock(side_effect=OSError("connection issue")))
        c = client.AsyncTCPClient("host", "port")

        with pytest.raises(error.ServiceConnectionError) as e:
            await c.send_request({"hello": "world"})

        assert e.value.debug == "('host', 'port'): connection issue"
        assert e.value.message == "Unable to connect to service."

        assert client.asyncio.open_connection.call_args == mock.call("host", "port")

    async def test_request_sent(self, monkeypatch):
        reader, writer = AsyncMock(), mock.Mock()
        monkeypatch.setattr(client.asyncio, "open_connection", AsyncMock(return_value=(reader, writer)))
        reader.read.side_effect = [
            MESSAGE_HEADER,
            b'{"world": "hello"}',
        ]

        c = client.AsyncTCPClient("host", "port")

        await c.send_request({"hello": "world"})

        assert writer.write.call_args == mock.call(
            b'\x00\x00\x00\x12{"hello": "world"}',
        )

    async def test_response_received(self, monkeypatch):
        reader, writer = AsyncMock(), mock.Mock()
        monkeypatch.setattr(client.asyncio, "open_connection", AsyncMock(return_value=(reader, writer)))
        reader.read.side_effect = [
            MESSAGE_HEADER,
            b'{"world": "hello"}',
        ]

        c = client.AsyncTCPClient("host", "port")

        r = await c.send_request({"hello": "world"})

        assert r == {"world": "hello"}

    async def test_response_received_multipart(self, monkeypatch):
        reader, writer = AsyncMock(), mock.Mock()
        monkeypatch.setattr(client.asyncio, "open_connection", AsyncMock(return_value=(reader, writer)))
        reader.read.side_effect = [
            MESSAGE_HEADER,
            b'{"worl',  # pragma: no-spell-check
            b'd": "hello"}',
        ]

        c = client.AsyncTCPClient("host", "port")

        r = await c.send_request({"hello": "world"})

        assert r == {"world": "hello"}
