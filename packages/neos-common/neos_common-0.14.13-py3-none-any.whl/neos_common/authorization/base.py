import typing
import uuid
from dataclasses import dataclass

from neos_common.authorization.token import TokenData
from neos_common.base import Action, ResourceLike, ResourceType
from neos_common.config import ApiConfig, Config

if typing.TYPE_CHECKING:
    import fastapi

    from neos_common.client.hub_client import HubClient
    from neos_common.client.keycloak_client import KeycloakClient


class SignatureValidator(typing.Protocol):
    """Define the base requirements for an object that can validate signed requests."""

    async def validate(
        self,
        request: "fastapi.Request",
        action: list[Action | str],
        resource: list[ResourceLike],
        logic_operator: str,
        *,
        return_allowed_resources: bool,
    ) -> tuple[uuid.UUID, list[str]]:
        """Validate a request and return the associated user_id and resources."""
        ...  # pragma: no cover


class AccessValidator:
    async def validate(
        self,
        user_id: uuid.UUID,
        actions: list[Action | str],
        resources: list[ResourceLike],
        logic_operator: str,
        *,
        return_allowed_resources: bool = True,
    ) -> tuple[uuid.UUID, list[str]]: ...  # pragma: no cover


class ConfigDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns Config."""

    async def __call__(self, request: "fastapi.Request") -> Config: ...  # pragma: no cover


class SignatureValidatorDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns a SignatureValidator."""

    async def __call__(self) -> SignatureValidator: ...  # pragma: no cover


class HubClientDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns an HubClient."""

    async def __call__(self, config: Config) -> "HubClient": ...  # pragma: no cover


class AccessValidatorDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns an AccessValidator."""

    async def __call__(self, hub_client: "HubClient", token: TokenData) -> AccessValidator: ...  # pragma: no cover


class KeycloakClientDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns a KeycloakClient."""

    async def __call__(self, config: ApiConfig) -> "KeycloakClient": ...  # pragma: no cover


@dataclass
class ActionResource:
    action: Action
    resource_type: ResourceType
    resource: ResourceLike
    resource_extractor: "typing.Callable[[fastapi.Request], dict[str, str]] | None" = None


@dataclass
class ActionResourceList:
    action_resources: list[ActionResource]
    logic_operator: typing.Literal["and", "or"] = "and"


class AuthorizationDependency(typing.Protocol):
    """Define the base requirements for a dependency that validates authorization."""

    def __init__(
        self,
        action_resources: ActionResourceList | list[ActionResource] | ActionResource,
        *,
        return_allowed_resources: bool = False,
    ) -> None: ...  # pragma: no cover

    async def __call__(
        self,
        request: "fastapi.Request",
        keycloak_client: "KeycloakClient",
        config: Config,
        signature_validator: SignatureValidator,
        access_validator: AccessValidator,
    ) -> TokenData: ...  # pragma: no cover
