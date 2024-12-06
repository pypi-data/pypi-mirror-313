import json
import typing
from unittest import mock

import aws4.key_pair
import httpcore
import httpx
import pytest

from neos_common import error
from neos_common.client import base
from tests.conftest import AsyncMock


class DummyClient(base.NeosClient):
    known_errors: typing.ClassVar[set] = {"E000"}
    service_name = "dummy"

    def __init__(self, token, key_pair, partition) -> None:
        assert token is not None or key_pair is not None

        self._token = token
        self._key_pair = key_pair
        self._partition = partition

    @property
    def token(self):
        return self._token

    @property
    def key_pair(self):
        return self._key_pair

    @property
    def partition(self):
        return self._partition


@pytest.fixture
def client():
    return DummyClient(token="token", key_pair=None, partition="ksa")


@pytest.fixture
def signature_client():
    return DummyClient(token="token", key_pair=aws4.key_pair.KeyPair("access-key", "access-secret"), partition="ksa")


class TestNeosClient:
    @pytest.mark.parametrize(
        ("method", "params", "json_payload", "headers"),
        [
            (base.Method.GET, None, None, None),
            (base.Method.GET, None, None, {"auth": "token"}),
            (base.Method.GET, {"a": "b", "c": "d"}, None, {"auth": "token"}),
            (base.Method.POST, None, None, None),
            (base.Method.POST, None, None, {"auth": "token"}),
            (base.Method.POST, None, {"a": "b", "c": "d"}, {"auth": "token"}),
            (base.Method.PUT, None, None, None),
            (base.Method.PUT, None, None, {"auth": "token"}),
            (base.Method.PUT, None, {"a": "b", "c": "d"}, {"auth": "token"}),
            (base.Method.DELETE, None, None, None),
            (base.Method.DELETE, None, None, {"auth": "token"}),
            (base.Method.DELETE, None, {"a": "b", "c": "d"}, {"auth": "token"}),
        ],
    )
    async def test_request(self, client, httpx_mock, method, params, json_payload, headers):
        url = "http://host"
        query = "?{}".format("&".join([f"{k}={v}" for k, v in params.items()])) if params else ""
        body = f"{json.dumps(json_payload)}".encode() if json_payload else None
        httpx_mock.add_response(
            url=f"{url}{query}",
            match_content=body,
            json={"hello": "world"},
            headers=headers,
        )

        r = await client._request(
            url=url,
            method=method,
            params=params,
            headers=headers,
            json=json_payload,
        )

        assert r.json() == {"hello": "world"}

    @pytest.mark.parametrize(
        ("method", "params", "json_payload", "headers"),
        [
            (base.Method.GET, None, None, None),
            (base.Method.GET, None, None, {"auth": "token"}),
            (base.Method.GET, {"a": "b", "c": "d"}, None, {"auth": "token"}),
            (base.Method.POST, None, None, None),
            (base.Method.POST, None, None, {"auth": "token"}),
            (base.Method.POST, None, {"a": "b", "c": "d"}, {"auth": "token"}),
            (base.Method.PUT, None, None, None),
            (base.Method.PUT, None, None, {"auth": "token"}),
            (base.Method.PUT, None, {"a": "b", "c": "d"}, {"auth": "token"}),
            (base.Method.DELETE, None, None, None),
            (base.Method.DELETE, None, None, {"auth": "token"}),
            (base.Method.DELETE, None, {"a": "b", "c": "d"}, {"auth": "token"}),
        ],
    )
    async def test_signed_request(self, signature_client, httpx_mock, method, params, json_payload, headers):
        url = "http://host"
        query = "?{}".format("&".join([f"{k}={v}" for k, v in params.items()])) if params else ""
        body = f"{json.dumps(json_payload)}".encode() if json_payload else None
        httpx_mock.add_response(
            url=f"{url}{query}",
            match_content=body,
            json={"hello": "world"},
            headers=headers,
        )

        r = await signature_client._request(url, method, params, headers, json_payload)

        assert r.json() == {"hello": "world"}

    async def test_token_request_generates_bearer_auth(self, client, monkeypatch):
        httpx_client = mock.MagicMock()
        mock_client = AsyncMock()
        httpx_client.__aenter__.return_value = mock_client
        monkeypatch.setattr(base.httpx, "AsyncClient", mock.MagicMock(return_value=httpx_client))

        await client._request("url", base.Method.GET)

        assert mock_client.request.call_args == mock.call(
            url="url",
            method="GET",
            params=None,
            json=None,
            headers=None,
            auth=base.NeosBearerClientAuth("token"),
        )

    async def test_empty_token_request_excludes_auth(self, monkeypatch):
        client = DummyClient(token="", key_pair=None, partition="ksa")
        httpx_client = mock.MagicMock()
        mock_client = AsyncMock()
        httpx_client.__aenter__.return_value = mock_client
        monkeypatch.setattr(base.httpx, "AsyncClient", mock.MagicMock(return_value=httpx_client))

        await client._request("url", base.Method.GET)

        assert mock_client.request.call_args == mock.call(
            url="url",
            method="GET",
            params=None,
            json=None,
            headers=None,
            auth=None,
        )

    async def test_signed_request_generates_signature_auth(self, signature_client, monkeypatch):
        httpx_client = mock.MagicMock()
        mock_client = AsyncMock()
        httpx_client.__aenter__.return_value = mock_client
        monkeypatch.setattr(base.httpx, "AsyncClient", mock.MagicMock(return_value=httpx_client))

        await signature_client._request("url", base.Method.GET)

        assert mock_client.request.call_args == mock.call(
            url="url",
            method="GET",
            params=None,
            json=None,
            headers=None,
            auth=base.HttpxAWS4Auth(
                aws4.key_pair.KeyPair("access-key", "access-secret"),
                "service",
                "ksa",
                aws4.AuthSchema("NEOS4-HMAC-SHA256", "x-neos"),
            ),
        )

    async def test_request_handles_timeout(self, client, httpx_mock):
        httpx_mock.add_exception(httpcore.ReadTimeout("Timed out"))
        with pytest.raises(error.ServiceTimeoutError):
            await client._request("url", method=base.Method.GET)

    async def test_request_handles_connect_error(self, client, httpx_mock):
        httpx_mock.add_exception(httpx.ConnectError("Unable to connect"))
        with pytest.raises(error.ServiceConnectionError):
            await client._request("url", method=base.Method.GET)

    async def test_get(self, client, monkeypatch):
        monkeypatch.setattr(client, "_request", AsyncMock(return_value="response"))

        r = await client._get("url", "params", "headers")

        assert r == "response"
        assert client._request.call_args == mock.call(
            url="url",
            method=base.Method.GET,
            params="params",
            headers="headers",
        )

    async def test_post(self, client, monkeypatch):
        monkeypatch.setattr(client, "_request", AsyncMock(return_value="response"))

        r = await client._post("url", "json", "headers")

        assert r == "response"
        assert client._request.call_args == mock.call(
            url="url",
            method=base.Method.POST,
            json="json",
            headers="headers",
        )

    async def test_put(self, client, monkeypatch):
        monkeypatch.setattr(client, "_request", AsyncMock(return_value="response"))

        r = await client._put("url", "json", "headers")

        assert r == "response"
        assert client._request.call_args == mock.call(
            url="url",
            method=base.Method.PUT,
            json="json",
            headers="headers",
        )

    async def test_delete(self, client, monkeypatch):
        monkeypatch.setattr(client, "_request", AsyncMock(return_value="response"))

        r = await client._delete("url", "json", "headers")

        assert r == "response"
        assert client._request.call_args == mock.call(
            url="url",
            method=base.Method.DELETE,
            json="json",
            headers="headers",
        )

    def test_process_unexpected_response(self, client):
        json = {"kong": "error"}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=400)

        with pytest.raises(error.UnhandledServiceApiError) as e:
            client.process_response(response)

        assert e.value.reason == "unhandled-service-api"
        assert e.value.message == "Unhandled dummy api response."
        assert e.value.debug is None
        assert e.value.status == "bad-request"

    def test_process_invalid_json(self, client):
        response = mock.Mock(json=mock.Mock(side_effect=json.JSONDecodeError("Ups", "doc", 1)), status_code=400)

        with pytest.raises(error.UnhandledServiceApiError) as e:
            client.process_response(response)

        assert e.value.reason == "unhandled-service-api"
        assert e.value.message == "Invalid dummy api JSON format response."
        assert e.value.debug == "Ups: 1"
        assert e.value.status == "bad-request"

    def test_process_rate_limit_timeout(self, client):
        json = {"kong": "error"}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=429)

        with pytest.raises(error.UnhandledServiceApiError) as e:
            client.process_response(response)

        assert e.value.reason == "unhandled-service-api"
        assert e.value.message == "dummy api rate limit error."
        assert e.value.debug is None
        assert e.value.status == "too-many-requests"

    def test_process_response_unknown_error(self, client):
        json = {"type": "1", "title": "message", "details": "debug_message"}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=400)

        with pytest.raises(error.UnhandledServiceApiError) as e:
            client.process_response(response)

        assert e.value.reason == "1"
        assert e.value.message == "Unhandled dummy api error response."
        assert e.value.debug == "debug_message"
        assert e.value.status == "bad-request"

    def test_process_response_validation_error(self, client):
        json = {"type": "1", "title": "message", "errors": {"validation": "error"}}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=422)

        with pytest.raises(error.ServiceApiError) as e:
            client.process_response(response)

        assert e.value.reason == "1"
        assert e.value.message == "dummy request validation error."
        assert e.value.details == {"validation": "error"}
        assert e.value.status == "unprocessable-entity"

    @pytest.mark.parametrize(
        ("code", "expected"),
        [
            ("E000", error.ServiceApiError),
        ],
    )
    def test_process_response_known_error(self, code, expected, client):
        json = {"type": code, "title": "message", "details": "debug_message"}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=400)

        with pytest.raises(expected) as e:
            client.process_response(response)

        assert e.value.debug == "debug_message"
