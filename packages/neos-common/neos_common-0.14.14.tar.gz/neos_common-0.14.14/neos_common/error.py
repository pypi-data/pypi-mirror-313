import re
import typing as t
from http import HTTPStatus

CONVERT_RE = re.compile(r"(?<!^)(?=[A-Z])")

if t.TYPE_CHECKING:  # pragma: no cover
    Loc = tuple[int | str, ...]

    class _ErrorDictRequired(t.TypedDict):
        loc: Loc
        msg: str
        type: str

    class ErrorDict(_ErrorDictRequired, total=False):
        """Type hint for pydantic.error_wrappers.ErrorDict.

        Stolen from type hints in pydantic.error_wrappers
        """

        ctx: dict[str, t.Any]


class NeosException(Exception):  # noqa: N818
    """Base class for all neos exceptions."""

    status_ = "unhandled"
    reason_ = None
    message_ = ""

    def __init__(
        self,
        debug: str | None = None,
        reason: str | None = None,
        message: str | None = None,
        status: int | str | None = None,
        details: list["ErrorDict"] | None = None,
    ) -> None:
        """Socket exception initiator.

        Args:
        ----
        debug: Additional context for specific error instance
        reason: error reason i.e. "neos-exception"
        status: error status i.e. "not-found"
        message: error message
        details: optional list of pydantic validation errors
        """
        reason_ = self.__class__.__name__.replace("Error", "")
        reason_ = CONVERT_RE.sub("-", reason_).lower()

        if isinstance(status, int):
            status = HTTPStatus(status).phrase.replace(" ", "-").lower()

        self.reason = reason or self.reason_ or reason_
        self.message = message or self.message_
        self.status = status or self.status_
        self.debug = debug
        self.details = details

    def __iter__(self) -> t.Iterator[tuple[str, bool | str | list["ErrorDict"] | None]]:
        """Return an iterator to support `dict(self)`."""
        return iter(
            [
                ("ok", False),
                ("status", self.status),
                ("reason", self.reason),
                ("message", self.message),
                ("debug", self.debug),
                ("details", self.details),
            ],
        )


class UnauthorisedError(NeosException):
    status_ = "unauthorised"


class ForbiddenError(NeosException):
    status_ = "forbidden"


class NotFoundError(NeosException):
    status_ = "not-found"


class ConflictError(NeosException):
    status_ = "conflict"


class BadRequestError(NeosException):
    status_ = "bad-request"


class ServerError(NeosException):
    status_ = "server-error"


class UnhandledServiceApiError(NeosException):
    pass


class ServiceApiError(NeosException):
    pass


class AuthorizationRequiredError(UnauthorisedError):
    message_ = "Authorization token required."


class InvalidAuthorizationError(UnauthorisedError):
    message_ = "Authorization token invalid."


class InsufficientPermissionsError(ForbiddenError):
    message_ = "Insufficient permissions."


class InvalidResourceFormatError(BadRequestError):
    message_ = "Resource has invalid format."


class IdentityAccessManagerError(NeosException):
    reason_ = "identity-access-manager-error"
    message_ = "Problem with Identity Access Manager."


class ServiceConnectionError(NeosException):
    reason_ = "service-connection-error"

    def __init__(self, message: str, debug: str | None = None) -> None:
        super().__init__(message=message, debug=debug)


class ServiceTimeoutError(NeosException):
    reason_ = "service-timeout-error"

    def __init__(self, message: str, debug: str | None = None) -> None:
        super().__init__(message=message, debug=debug)


class SignatureError(UnauthorisedError):
    reason_ = "signature-error"
    message_ = "Signature invalid."
