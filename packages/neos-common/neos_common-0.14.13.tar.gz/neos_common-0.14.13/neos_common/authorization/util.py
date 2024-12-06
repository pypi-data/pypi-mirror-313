import logging
import typing

import fastapi
import keycloak
from aws4.key_pair import KeyPair
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.base import SecurityBase

from neos_common import base, error
from neos_common.authorization import token, validator
from neos_common.authorization.base import (
    AccessValidator,
    AccessValidatorDependency,
    ActionResource,
    ActionResourceList,
    AuthorizationDependency,
    ConfigDependency,
    HubClientDependency,
    KeycloakClientDependency,
    SignatureValidator,
    SignatureValidatorDependency,
)
from neos_common.client.hub_client import HubClient
from neos_common.client.keycloak_client import KeycloakClient
from neos_common.config import ApiConfig, Config

logger = logging.getLogger(__name__)


PermissionArgs = typing.Union[  # noqa: UP007
    # action, resource_type, resource_id
    tuple[base.Action, base.ResourceType, str | None],
    # action, resource_type, resource_id, partition, account_id
    tuple[base.Action, base.ResourceType, str | None, str | None, str | None],
]


def create_openapi_info(
    config: Config,
    resource_class: type,
    *args: PermissionArgs,
    logic_operator: str = "and",
) -> dict[str, str]:
    """Generate openapi info for use in FastAPI routes."""
    docs = {}
    for i, a in enumerate(args):
        if len(a) == 3:
            action, resource_type, resource_id = a
            resource_urn = resource_class.generate_from_config(
                config=config,
                resource_type=resource_type,
                resource_id=resource_id,
            ).urn
        elif len(a) == 5:
            action, resource_type, resource_id, partition, account = a
            resource_urn = resource_class.generate_from_config(
                config=config,
                partition=partition,
                account_id=account,
                resource_type=resource_type,
                resource_id=resource_id,
            ).urn
        else:
            msg = "Invalid number of arguments"
            raise ValueError(msg)

        docs[f"x-iam-action-{i}"] = action.value
        docs[f"x-iam-resource-{i}"] = resource_urn
    docs["logic-operator"] = logic_operator

    return docs


class DepKeycloakClientFactory:
    """Keycloak client dependency.

    Pull the config from the app.state, instantiate a keycloak client.

    Returns:
    -------
        KeycloakClient using configured keycloak parameters.
    """

    @classmethod
    def build(cls, config_dep: type[ConfigDependency]) -> type[KeycloakClientDependency]:
        """Build a KeycloakClientDependency.

        Generate a fastapi dependency that creates a KeycloakClient.
        """

        class DepKeycloakClient:
            async def __call__(self, config: ApiConfig = fastapi.Depends(config_dep())) -> KeycloakClient:
                return KeycloakClient(
                    host=config.keycloak_host,
                    realm=config.keycloak_realm,
                    client_id=config.keycloak_client_id,
                    client_secret=config.keycloak_client_secret,
                )

        return DepKeycloakClient


class DepAuthorizationFactory:
    """Authorization dependency.

    Pull the config from the app.state and parse the token from the request.

    Returns:
    -------
        TokenData with information about current user.
    """

    @classmethod
    def build(  # noqa: C901
        cls,
        config_dep: type[ConfigDependency],
        keycloak_dep: type[KeycloakClientDependency],
        signature_dep: type[SignatureValidatorDependency],
        access_validator: type[AccessValidatorDependency],
    ) -> type[AuthorizationDependency]:
        """Build an AuthorizationDependency.

        Generate a fastapi dependency that validates incoming authorization
        headers and creates TokenData.
        """

        class DepAuthorization(SecurityBase):
            def __init__(
                self,
                action_resources: ActionResourceList | list[ActionResource] | ActionResource,
                *,
                return_allowed_resources: bool = False,
            ) -> None:
                self.model = HTTPBearerModel()
                self.scheme_name = "bearer"

                if isinstance(action_resources, ActionResource):
                    action_resources = [action_resources]

                if isinstance(action_resources, list):
                    action_resources = ActionResourceList(action_resources=action_resources)

                self.action_resources: ActionResourceList = action_resources
                self.return_allowed_resources = return_allowed_resources

            def extract_action_resources(
                self,
                request: fastapi.Request,
                config: Config,
            ) -> tuple[list[base.Action | str], list[base.ResourceLike]]:
                actions: list[base.Action | str] = []
                resources: list[base.ResourceLike] = []

                for ar in self.action_resources.action_resources:
                    resource_kwargs = ar.resource_extractor(request) if ar.resource_extractor else {"resource_id": None}
                    resources.append(
                        ar.resource.generate_from_config(
                            config,
                            ar.resource_type,
                            **resource_kwargs,
                        ),
                    )
                    actions.append(ar.action)

                return actions, resources

            async def __call__(
                self,
                request: fastapi.Request,
                keycloak_client: KeycloakClient = fastapi.Depends(keycloak_dep()),
                config: Config = fastapi.Depends(config_dep()),
                signature_validator: SignatureValidator = fastapi.Depends(signature_dep()),
                access_validator: AccessValidator = fastapi.Depends(access_validator()),
            ) -> token.TokenData:
                authorization = request.headers.get("Authorization", "")
                auth_type, _, credentials = authorization.partition(" ")
                if auth_type == "":
                    msg = "Missing Authorization header."
                    raise error.AuthorizationRequiredError(msg)

                actions_, resources_ = self.extract_action_resources(request, config)

                if auth_type.lower() == "bearer":
                    access_token = credentials

                    logger.info(access_token)
                    try:
                        introspected_token = keycloak_client.introspect_token(access_token)
                    except keycloak.KeycloakError as e:
                        message = keycloak_client.parse_error(e)
                        logger.warning(message)
                        raise error.IdentityAccessManagerError(message) from e

                    if not introspected_token["active"]:
                        raise error.InvalidAuthorizationError

                    try:
                        user_id = introspected_token["sub"]
                    except KeyError as e:
                        msg = f"Invalid token format, {e!s}"
                        raise error.InvalidAuthorizationError(msg) from e

                    user_id, resources = (
                        await access_validator.validate(
                            user_id,
                            actions_,
                            resources_,
                            logic_operator=self.action_resources.logic_operator,
                            return_allowed_resources=self.return_allowed_resources,
                        )
                        if resources_ != []
                        else (user_id, [])
                    )

                    return token.TokenData(user_id, access_token, resources)

                if auth_type.lower() in ("neos4-hmac-sha256", "aws4-hmac-sha256"):
                    user_id, resources = await signature_validator.validate(
                        request,
                        actions_,
                        resources_,
                        logic_operator=self.action_resources.logic_operator,
                        return_allowed_resources=self.return_allowed_resources,
                    )
                    return token.TokenData(user_id=str(user_id), auth_token="none", resources=resources)  # noqa: S106

                msg = "Unsupported authorization header."
                raise error.InvalidAuthorizationError(msg)

        return DepAuthorization


class DepAccessValidatorFactory:
    """Access validator dependency."""

    @classmethod
    def build(
        cls,
        hub_client_dep: type[HubClientDependency],
    ) -> type[AccessValidatorDependency]:
        """Build an AccessValidatorDependency.

        Generate a fastapi dependency that creates an AccessValidator.
        """

        class DepAccessValidator(AccessValidatorDependency):
            async def __call__(
                self,
                hub_client: HubClient = fastapi.Depends(hub_client_dep()),
            ) -> validator.AccessValidator:
                return validator.AccessValidator(
                    hub_client=hub_client,
                )

        return DepAccessValidator


class DepHubClientFactory:
    @classmethod
    def build(
        cls,
        config_dep: type[ConfigDependency],
    ) -> type[HubClientDependency]:
        """Build an HubClientDependency.

        Generate a fastapi dependency that creates an HubClient.
        """

        class DepHubClient:
            async def __call__(
                self,
                config: Config = fastapi.Depends(config_dep()),
            ) -> HubClient:
                return HubClient(
                    host=config.hub_host,  # type: ignore[reportGeneralTypeIssues]
                    token=None,
                    key_pair=KeyPair(
                        config.access_key_id,  # type: ignore[reportGeneralTypeIssues]
                        config.secret_access_key,  # type: ignore[reportGeneralTypeIssues]
                    ),
                    account=config.account,  # type: ignore[reportGeneralTypeIssues]
                    partition=config.partition,  # type: ignore[reportGeneralTypeIssues]
                )

        return DepHubClient
