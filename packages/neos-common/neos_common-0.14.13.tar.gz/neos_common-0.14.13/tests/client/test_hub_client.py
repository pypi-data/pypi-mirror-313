import json
from unittest import mock

import pytest
from aws4.key_pair import KeyPair

from neos_common import base, error, schema
from neos_common.authorization import token
from neos_common.client.hub_client import HubClient
from neos_common.schema import Contract, Subscription, Visibility


@pytest.fixture
def client():
    return HubClient(
        "https://hub-host",
        token.TokenData("user-id", "auth_token", []),
        key_pair=None,
        account="root",
        partition="ksa",
    )


@pytest.fixture
def signature_client():
    return HubClient(
        "https://hub-host",
        None,
        key_pair=KeyPair("access_key", "access_secret"),
        account="root",
        partition="ksa",
    )


class TestHubClient:
    def test_init_bearer(self):
        hub_client = HubClient("host", "token", None, "account", "partition")
        assert hub_client._host == "host"
        assert hub_client._token == "token"
        assert hub_client._key_pair is None
        assert hub_client._account == "account"
        assert hub_client._partition == "partition"

    def test_init_sign(self):
        hub_client = HubClient("host", None, "key_pair", "account", "partition")
        assert hub_client._host == "host"
        assert hub_client._token is None
        assert hub_client._key_pair == "key_pair"
        assert hub_client._account == "account"
        assert hub_client._partition == "partition"

    def test_validate_token_url(self, client):
        assert client.validate_token_url == "https://hub-host/iam/validate/token"

    def test_validate_signature_url(self, client):
        assert client.validate_signature_url == "https://hub-host/iam/validate/signature"

    @pytest.mark.parametrize(
        ("code", "expected_error"),
        [
            ("authorization-required", error.AuthorizationRequiredError),
            ("invalid-authorization", error.InvalidAuthorizationError),
            ("insufficient-permissions", error.InsufficientPermissionsError),
            ("invalid-resource-format", error.InvalidResourceFormatError),
            ("identity-access-manager-error", error.IdentityAccessManagerError),
            ("server-error", error.ServiceApiError),
        ],
    )
    def test_process_response_mapping_error(self, client, code, expected_error):
        json = {"type": code, "title": "message", "details": "debug message"}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=422)

        with pytest.raises(expected_error):
            client.process_response_with_mapping(response)

    def test_process_response_unknown_error(self, client):
        json = {"type": "1", "title": "message", "details": "debug_message"}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=400)

        with pytest.raises(error.UnhandledServiceApiError) as e:
            client.process_response(response)

        assert e.value.reason == "1"
        assert e.value.message == "Unhandled Hub api error response."
        assert e.value.debug == "debug_message"
        assert e.value.status == "bad-request"

    def test_process_response_validation_error(self, client):
        json = {"type": "1", "title": "message", "errors": {"validation": "error"}}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=422)

        with pytest.raises(error.ServiceApiError) as e:
            client.process_response(response)

        assert e.value.reason == "1"
        assert e.value.message == "Hub request validation error."
        assert e.value.details == {"validation": "error"}
        assert e.value.status == "unprocessable-entity"

    @pytest.mark.parametrize(
        ("code", "expected"),
        [
            ("policy-not-found", error.ServiceApiError),
            ("core-already-registered", error.ServiceApiError),
        ],
    )
    def test_process_response_known_error(self, code, expected, client):
        json = {"type": code, "title": "message", "details": "debug_message"}
        response = mock.Mock(json=mock.Mock(return_value=json), status_code=400)

        with pytest.raises(expected) as e:
            client.process_response(response)

        assert e.value.debug == "debug_message"

    async def test_validate_token_with_return_resource(self, httpx_mock, client):
        resources_payload = {
            "principal_id": "user_id",
            "resources": ["nrn:ksa:core:sc:root:product:my-product"],
        }
        httpx_mock.add_response(
            url="https://hub-host/iam/validate/token?principal_id=user_id&action=core:announce&resource=nrn%3Aksa%3Acore%3Asc%3Aroot%3Aproduct%3Amy-product&return_allowed_resources=true&logic_operator=and",
            json=resources_payload,
        )

        user_id, resources = await client.validate_token(
            principal="user_id",
            actions=[base.Action.core_announce],
            resources=["nrn:ksa:core:sc:root:product:my-product"],
            logic_operator="and",
            return_allowed_resources=True,
        )
        assert resources == resources_payload["resources"]
        assert user_id == "user_id"

    async def test_validate_token_without_return_resource(self, httpx_mock, client):
        resources_payload = {
            "principal_id": "user_id",
            "resources": [],
        }
        httpx_mock.add_response(
            url="https://hub-host/iam/validate/token?principal_id=user_id&action=core:announce&resource=nrn%3Aksa%3Acore%3Asc%3Aroot%3Aproduct%3Amy-product&return_allowed_resources=false&logic_operator=or",
            json=resources_payload,
        )

        user_id, resources = await client.validate_token(
            principal="user_id",
            actions=[base.Action.core_announce],
            resources=["nrn:ksa:core:sc:root:product:my-product"],
            logic_operator="or",
            return_allowed_resources=False,
        )
        assert resources == resources_payload["resources"]
        assert user_id == "user_id"

    async def test_validate_signature(self, httpx_mock, client):
        resources_payload = {
            "principal_id": "user_id",
            "resources": ["nrn:ksa:core:sc:root:product:my-product"],
        }
        httpx_mock.add_response(
            url="https://hub-host/iam/validate/signature?access_key_id=access-key-id&auth_schema=NEOS4&scope=scope&challenge=challenge&signed_challenge=signed-challenge&action=core:announce&resource=nrn%3Aksa%3Acore%3Asc%3Aroot%3Aproduct%3Amy-product&return_allowed_resources=true&logic_operator=and",
            json=resources_payload,
        )

        user_id, resources = await client.validate_signature(
            access_key="access-key-id",
            auth_schema="NEOS4",
            scope="scope",
            challenge="challenge",
            signed_challenge="signed-challenge",
            actions=[base.Action.core_announce],
            resources=["nrn:ksa:core:sc:root:product:my-product"],
            logic_operator="and",
            return_allowed_resources=True,
        )
        assert resources == resources_payload["resources"]
        assert user_id == "user_id"

    async def test_get_allowed_resources(self, httpx_mock, client):
        httpx_mock.add_response(
            url="https://hub-host/iam/principal/user-id/resource?action=product:consume",
            json={
                "resources": ["a", "b"],
                "principal_id": "user-id",
            },
        )

        resources = await client.get_allowed_resources("user-id", base.Action.product_consume)
        assert resources == ["a", "b"]

    async def test_announce_core(self, httpx_mock, client):
        httpx_mock.add_response(
            method="POST",
            url="https://hub-host/registry/core/identifier/announce",
            headers={"X-Access-Key": "core-access-key"},
            match_content=b'{"host": "host", "version": "v1.2.3"}',
            json={},
        )

        await client.announce_core("host", version="v1.2.3", core_identifier="identifier")

    async def test_register_data_product_approval_false(self, httpx_mock, client):
        # Set up expected contract with approval set to False
        expected_contract = Contract(visibility=Visibility.PUBLIC, subscription=Subscription(approval=False))

        # Mock the response to simulate the API's response when approval is False
        httpx_mock.add_response(
            method="POST",
            url="https://hub-host/registry/core/core-identifier/data_product",
            headers={"X-Access-Key": "core-access-key"},
            json={
                "urn": "urn",
                "name": "name",
                "metadata": {"hello": "world"},
                "description": "description",
                "label": "ABC",
                "sanitized_name": "sanitized_name",
                "data_product_type": "data_product_type",
                "engine": "engine",
                "table": "table",
                "identifier": "identifier",
                "contract": {"visibility": "public", "subscription": {"approval": False}},
            },
        )

        # Execute the method with approval set to False
        await client.register_data_product(
            "urn",
            "name",
            metadata={"hello": "world"},
            description="description",
            label="ABC",
            sanitized_name="sanitized_name",
            data_product_type="data_product_type",
            engine="engine",
            table="table",
            identifier="identifier",
            core_identifier="core-identifier",
            contract=expected_contract,
        )

        request = httpx_mock.get_request()
        request_data = json.loads(request.content)

        # Assert that approval is set to False in the contract
        assert request_data["contract"]["subscription"]["approval"] is False

    async def test_register_data_product(self, httpx_mock, client):
        httpx_mock.add_response(
            method="POST",
            url="https://hub-host/registry/core/core-identifier/data_product",
            headers={"X-Access-Key": "core-access-key"},
            match_content=bytes(
                json.dumps({
                    "urn": "urn",
                    "name": "name",
                    "metadata": {"hello": "world"},
                    "description": "description",
                    "label": "ABC",
                    "sanitized_name": "sanitized_name",
                    "data_product_type": "data_product_type",
                    "engine": "engine",
                    "table": "table",
                    "identifier": "identifier",
                    "contract": {"visibility": "public", "subscription": {"approval": True}},
                }),
                "utf-8",
            ),
            json={},
        )

        await client.register_data_product(
            "urn",
            "name",
            metadata={"hello": "world"},
            description="description",
            label="ABC",
            sanitized_name="sanitized_name",
            data_product_type="data_product_type",
            engine="engine",
            table="table",
            identifier="identifier",
            core_identifier="core-identifier",
            contract=schema.Contract(visibility="public", subscription=schema.Subscription(approval=True)),
        )

    async def test_register_private_data_product(self, httpx_mock, client):
        httpx_mock.add_response(
            method="POST",
            url="https://hub-host/registry/core/core-identifier/data_product",
            headers={"X-Access-Key": "core-access-key"},
            match_content=bytes(
                json.dumps({
                    "urn": "urn",
                    "name": "name",
                    "metadata": {"hello": "world"},
                    "description": "description",
                    "label": "ABC",
                    "sanitized_name": "sanitized_name",
                    "data_product_type": "data_product_type",
                    "engine": "engine",
                    "table": "table",
                    "identifier": "identifier",
                    "contract": {"visibility": "private", "subscription": {"approval": True}},
                }),
                "utf-8",
            ),
            json={},
        )

        await client.register_data_product(
            "urn",
            "name",
            metadata={"hello": "world"},
            description="description",
            label="ABC",
            sanitized_name="sanitized_name",
            data_product_type="data_product_type",
            engine="engine",
            table="table",
            identifier="identifier",
            core_identifier="core-identifier",
            contract=schema.Contract(visibility="private", subscription=schema.Subscription(approval=True)),
        )

    async def test_update_data_product_metadata(self, httpx_mock, client):
        httpx_mock.add_response(
            method="POST",
            url="https://hub-host/registry/core/core-identifier/data_product/metadata",
            headers={"X-Access-Key": "core-access-key"},
            match_content=b'{"urn": "urn", "metadata": {"hello": "world"}, "description": "desc"}',
            json={},
        )

        await client.update_data_product_metadata(
            "urn",
            metadata={"hello": "world"},
            description="desc",
            core_identifier="core-identifier",
        )

    async def test_deregister_data_product(self, httpx_mock, client):
        httpx_mock.add_response(
            method="DELETE",
            url="https://hub-host/registry/core/core-identifier/data_product",
            headers={"X-Access-Key": "core-access-key"},
            match_content=b'{"urn": "urn"}',
            json={},
        )

        await client.deregister_data_product("urn", core_identifier="core-identifier")
