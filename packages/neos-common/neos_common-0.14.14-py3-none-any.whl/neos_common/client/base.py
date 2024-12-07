import json
import logging
import typing
from enum import Enum

import aws4
import aws4.key_pair
import httpcore
import httpx
from aws4.client import HttpxAWS4Auth

from neos_common import error

logger = logging.getLogger(__name__)


BAD_REQUEST_CODE = 400
NOT_FOUND_CODE = 400
REQUEST_VALIDATION_CODE = 422
RATE_LIMIT_CODE = 429


class Method(Enum):
    """HTTP request methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


async def log_request(request: httpx.Request) -> None:
    """Event hook for httpx events to log requests."""
    logger.info(
        f"[Request] {request.method.upper()} {request.url}",
    )


class NeosBearerClientAuth:
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, request: httpx.Request) -> httpx.Request:
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, NeosBearerClientAuth) and other.token == self.token


class NeosClient(typing.Protocol):
    """Base class for HTTP client implementations for NEOS rest services."""

    unhandled_error_class = error.UnhandledServiceApiError
    handled_error_class = error.ServiceApiError

    @property
    def token(self) -> str | None: ...

    @property
    def key_pair(self) -> aws4.key_pair.KeyPair | None: ...

    @property
    def known_errors(self) -> set[str]: ...  # pragma: no cover

    @property
    def service_name(self) -> str: ...  # pragma: no cover

    @property
    def partition(self) -> str: ...  # pragma: no cover

    async def _request(
        self,
        url: str,
        method: Method,
        params: dict | None = None,
        headers: dict | None = None,
        json: dict | None = None,
        *,
        verify: bool = True,
        **kwargs,
    ) -> httpx.Response:
        if self.key_pair is not None:
            auth = HttpxAWS4Auth(
                self.key_pair,
                self.service_name,
                self.partition,
                aws4.AuthSchema("NEOS4-HMAC-SHA256", "x-neos"),
            )
        elif self.token:
            auth = NeosBearerClientAuth(self.token)
        else:
            auth = None

        async with httpx.AsyncClient(event_hooks={"request": [log_request]}, verify=verify) as client:
            try:
                r = await client.request(
                    url=url,
                    method=method.value,
                    params=params,
                    json=json,
                    headers=headers,
                    auth=auth,
                    **kwargs,
                )
            except httpcore.ReadTimeout as e:
                raise error.ServiceTimeoutError(
                    message=f"Timeout connecting to {self.service_name} service.",
                    debug=str(e),
                ) from e
            except httpx.ConnectError as e:
                raise error.ServiceConnectionError(
                    message=f"Error connecting to {self.service_name} service.",
                    debug=str(e),
                ) from e

        return r

    async def _get(
        self,
        url: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        return await self._request(
            url=url,
            method=Method.GET,
            params=params,
            headers=headers,
        )

    async def _post(
        self,
        url: str,
        json: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        return await self._request(
            url=url,
            method=Method.POST,
            json=json,
            headers=headers,
        )

    async def _put(
        self,
        url: str,
        json: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        return await self._request(
            url=url,
            method=Method.PUT,
            json=json,
            headers=headers,
        )

    async def _delete(
        self,
        url: str,
        json: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        return await self._request(
            url=url,
            method=Method.DELETE,
            json=json,
            headers=headers,
        )

    def process_response(self, response: httpx.Response) -> dict:
        try:
            data = response.json()
        except json.JSONDecodeError as exc:
            logger.error(response.content)  # noqa: TRY400
            raise self.unhandled_error_class(
                message=f"Invalid {self.service_name} api JSON format response.",
                status=response.status_code,
                debug=f"{exc.msg}: {exc.pos}",
            ) from exc
        if response.status_code >= BAD_REQUEST_CODE:
            logger.info(data)
            try:
                details = None
                if data["type"] is not None:
                    details = data.get("details", data["title"])

                exc = self.unhandled_error_class(
                    message=f"Unhandled {self.service_name} api error response.",
                    status=response.status_code,
                    reason=data["type"],
                    debug=details,
                )
            except KeyError as e:
                exc = self.unhandled_error_class(
                    message=f"Unhandled {self.service_name} api response.",
                    status=response.status_code,
                )
                if response.status_code == RATE_LIMIT_CODE:
                    exc = self.unhandled_error_class(
                        message=f"{self.service_name} api rate limit error.",
                        status=response.status_code,
                    )

                raise exc from e

            if response.status_code == REQUEST_VALIDATION_CODE:
                exc = self.handled_error_class(
                    message=f"{self.service_name} request validation error.",
                    details=data.get("errors"),
                    reason=data["type"],
                    status=response.status_code,
                )
            elif data["type"] in self.known_errors:
                exc = self.handled_error_class(
                    message=data["title"],
                    debug=data.get("details"),
                    reason=data["type"],
                    status=response.status_code,
                )

            raise exc

        return data
