from unittest import mock

import pytest
from aws4.key_pair import KeyPair

from neos_common import base, config, error
from tests.conftest import AsyncMock

keycloak = pytest.importorskip("keycloak")
util = pytest.importorskip("neos_common.authorization.util")


class Config(config.ApiConfig):
    name: str = "test"

    access_manager_host: str = "https://access-manager-host"


@pytest.fixture
def config_obj():
    return Config(
        keycloak_host="https://keycloak-host",
        keycloak_realm="test",
        keycloak_client_id="client-id",
        keycloak_client_secret="client-secret",
        postgres_host="postgres-host",
        postgres_user="postgres-user",
        postgres_password="postgres-password",
        postgres_database="postgres-database",
        access_key_id="access-key-id",
        secret_access_key="secret-access-key",
    )


class TestCommonConfig:
    def test_api_prefix_prepends_slash_if_missing(self, config_obj, monkeypatch):
        monkeypatch.setattr(config_obj, "raw_api_prefix", "api")

        assert config_obj.api_prefix == "/api"

    def test_api_prefix_handles_existing_slash(self, config_obj, monkeypatch):
        monkeypatch.setattr(config_obj, "raw_api_prefix", "/api")

        assert config_obj.api_prefix == "/api"

    def test_logging_config(self, config_obj):
        assert config_obj.logging_config == {
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": "INFO",
                },
            },
            "loggers": {
                "test": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
                "pogo_migrate": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
                "neos_common": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
            "version": 1,
        }


class TestOpenapiInfo:
    def test_info_creation(self, config_obj):
        info_dict: dict[str, str] = {
            "x-iam-action-0": "core:announce",
            "x-iam-resource-0": "test:core:resource_id",
            "logic-operator": "and",
        }

        def generate_from_config(config, resource_type, resource_id):
            return mock.Mock(urn=f"{config.name}:{resource_type.value}:{resource_id}")

        assert info_dict == util.create_openapi_info(
            config_obj,
            mock.Mock(generate_from_config=generate_from_config),
            (base.Action.core_announce, base.ResourceType.core, "resource_id"),
        )

    def test_info_creation_with_account(self, config_obj):
        info_dict: dict[str, str] = {
            "x-iam-action-0": "core:announce",
            "x-iam-resource-0": "test:ksa:account:core:resource_id",
            "logic-operator": "or",
        }

        def generate_from_config(config, partition, account_id, resource_type, resource_id):
            return mock.Mock(urn=f"{config.name}:{partition}:{account_id}:{resource_type.value}:{resource_id}")

        assert info_dict == util.create_openapi_info(
            config_obj,
            mock.Mock(generate_from_config=generate_from_config),
            (base.Action.core_announce, base.ResourceType.core, "resource_id", "ksa", "account"),
            logic_operator="or",
        )

    def test_info_creation_invalid_call(self, config_obj):
        with pytest.raises(ValueError, match="Invalid number of arguments"):
            util.create_openapi_info(
                config_obj,
                mock.Mock(),
                (base.Action.core_announce, base.ResourceType.core, "resource_id", "ksa", "account", "unexpected"),
            )


class TestDepKeycloakClientFactory:
    async def test_client_returned(self, config_obj, monkeypatch):
        kc = mock.Mock()
        monkeypatch.setattr(util, "KeycloakClient", mock.Mock(return_value=kc))

        DepKeycloakClient = util.DepKeycloakClientFactory.build(mock.Mock())

        client = await DepKeycloakClient()(config_obj)

        assert client == kc
        assert util.KeycloakClient.call_args == mock.call(
            host=config_obj.keycloak_host,
            realm=config_obj.keycloak_realm,
            client_id=config_obj.keycloak_client_id,
            client_secret=config_obj.keycloak_client_secret,
        )


class Resource(base.ResourceBase):
    def generate_from_config(self, *args, **kwargs) -> str:  # noqa: ARG002
        return ""


class TestDepAuthorizationFactory:
    def test_init_single_action_resource(self):
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization(util.ActionResource("action", "resource_type", "resource"))

        assert dep.action_resources == util.ActionResourceList(
            [util.ActionResource("action", "resource_type", "resource")],
            "and",
        )

    def test_init_action_resources(self):
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization([util.ActionResource("action", "resource_type", "resource")])

        assert dep.action_resources == util.ActionResourceList(
            [util.ActionResource("action", "resource_type", "resource")],
            "and",
        )

    def test_init_action_resource_list(self):
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization(
            util.ActionResourceList([util.ActionResource("action", "resource_type", "resource")], "or"),
        )

        assert dep.action_resources == util.ActionResourceList(
            [util.ActionResource("action", "resource_type", "resource")],
            "or",
        )

    async def test_no_token_enforced(self, config_obj):
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization(util.ActionResourceList([], "or"))
        request = mock.Mock(headers={})

        with pytest.raises(error.AuthorizationRequiredError):
            await dep(request, mock.Mock(), config_obj, mock.Mock(), mock.Mock())

    async def test_keycloak_error_handled(self, config_obj):
        mock_keycloak = mock.Mock(
            introspect_token=mock.Mock(side_effect=keycloak.KeycloakError("an error")),
        )
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization(
            util.ActionResourceList([util.ActionResource("action", base.ResourceType.core, Resource)], "and"),
        )
        request = mock.Mock(headers={"Authorization": "Bearer token"})

        with pytest.raises(error.IdentityAccessManagerError):
            await dep(request, mock_keycloak, config_obj, mock.Mock(), mock.Mock())

    async def test_inactive_token(self, config_obj):
        mock_keycloak = mock.Mock(
            introspect_token=mock.Mock(
                return_value={"active": False},
            ),
        )
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization([])
        request = mock.Mock(headers={"Authorization": "Bearer token"})

        with pytest.raises(error.InvalidAuthorizationError):
            await dep(request, mock_keycloak, config_obj, mock.Mock(), mock.Mock())

    async def test_malformed_token(self, config_obj):
        mock_keycloak = mock.Mock(
            introspect_token=mock.Mock(
                return_value={"active": True},
            ),
        )
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization([])
        request = mock.Mock(headers={"Authorization": "Bearer token"})

        with pytest.raises(error.InvalidAuthorizationError) as e:
            await dep(request, mock_keycloak, config_obj, mock.Mock(), mock.Mock())

        assert e.value.debug == "Invalid token format, 'sub'"

    async def test_valid_token(self, config_obj):
        mock_keycloak = mock.Mock(
            introspect_token=mock.Mock(
                return_value={
                    "active": True,
                    "sub": "user-id",
                },
            ),
        )
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization([])
        request = mock.Mock(headers={"Authorization": "Bearer token"})

        token = await dep(request, mock_keycloak, config_obj, mock.Mock(), mock.Mock())

        assert token.user_id == "user-id"

    async def test_valid_signature(self, config_obj):
        mock_keycloak = mock.Mock()
        mock_signature = mock.Mock(validate=AsyncMock(return_value=("user-id", [])))
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization([])
        request = mock.Mock(headers={"Authorization": "NEOS4-HMAC-SHA256 ..."})

        token = await dep(request, mock_keycloak, config_obj, mock_signature, mock.Mock())

        assert token.user_id == "user-id"
        assert token.resources == []

    async def test_unsupported_auth(self, config_obj):
        mock_keycloak = mock.Mock()
        DepAuthorization = util.DepAuthorizationFactory.build(mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock())
        dep = DepAuthorization([])
        request = mock.Mock(headers={"Authorization": "Basic token"})

        with pytest.raises(error.InvalidAuthorizationError):
            await dep(request, mock_keycloak, config_obj, mock.Mock(), mock.Mock())


class TestDepAccessValidatorFactory:
    async def test_validator_returned(self, monkeypatch):
        hub_client = mock.Mock()
        av = mock.Mock()
        monkeypatch.setattr(util.validator, "AccessValidator", mock.Mock(return_value=av))
        DepAccessValidator = util.DepAccessValidatorFactory.build(mock.Mock())
        access_validator = await DepAccessValidator()(hub_client)

        assert access_validator == av

    async def test_default_client_generated(self):
        hub_client = mock.Mock()
        DepAccessValidator = util.DepAccessValidatorFactory.build(mock.Mock())
        access_validator = await DepAccessValidator()(hub_client)

        assert access_validator._hub_client == hub_client

    async def test_validator_generates_client(self):
        hub_client = mock.Mock()

        DepAccessValidator = util.DepAccessValidatorFactory.build(mock.Mock())
        access_validator = await DepAccessValidator()(hub_client)

        assert access_validator._hub_client == hub_client


class TestDepHubClientFactory:
    async def test_hub_client_returned(self, monkeypatch):
        config = mock.Mock(
            hub_host="host",
            access_key_id="access-key",
            secret_access_key="secret-key",
            partition="ksa",
            account="root",
        )
        hub_client_mock = mock.Mock()
        HubClientMock = mock.Mock(return_value=hub_client_mock)
        monkeypatch.setattr(util, "HubClient", HubClientMock)
        DepHubClient = util.DepHubClientFactory.build(mock.Mock())
        hub_client = await DepHubClient()(config)

        assert HubClientMock.call_args == mock.call(
            host="host",
            token=None,
            key_pair=KeyPair(
                access_key_id="access-key",
                secret_access_key="secret-key",
            ),
            account="root",
            partition="ksa",
        )
        assert hub_client == hub_client_mock
