from unittest import mock

import fastapi
import pytest
from starlette import testclient

from neos_common.api import get_error_codes, get_permissions
from neos_common.authorization.util import create_openapi_info
from neos_common.base import Action, ResourceBase, ResourceType


class Resource(ResourceBase):
    @classmethod
    def get_resource_id_template(cls):
        return "{resource_id}"

    @classmethod
    def format_resource_id(cls, *args):
        return cls.get_resource_id_template().format(resource_id=args[0])

    @staticmethod
    def generate_from_config(
        config,  # noqa: ARG004
        resource_type,
        resource_id,
        partition,
        account_id,
    ) -> "Resource":
        return Resource.generate(
            xrn="urn",
            partition=partition,
            service="core",
            identifier="",
            account_id=account_id,
            resource_type=resource_type.value,
            resource_id=str(resource_id) if resource_id else None,
        )


@pytest.fixture
def client():
    app = fastapi.FastAPI()
    config = mock.Mock()

    def get_something() -> None:
        pass

    def get_something_else() -> None:
        pass

    app.get(
        "/something",
        summary="Get Something.",
        openapi_extra=create_openapi_info(
            config,
            Resource,
            (Action.core_register, ResourceType.core, None, "{partition}", "root"),
        ),
    )(get_something)
    app.get(
        "/something_else",
        summary="Get Something Else.",
        openapi_extra=create_openapi_info(
            config,
            Resource,
            (Action.core_register, ResourceType.core, None, "{partition}", "root"),
            (Action.core_access, ResourceType.core, None, "{partition}", "root"),
            logic_operator="or",
        ),
    )(get_something_else)

    return testclient.TestClient(app)


def test_get_error_codes():
    assert get_error_codes("tests.error_codes_fixture").model_dump() == {
        "errors": [
            {
                "class_name": "NoCodeError",
                "type": "no-code",
                "title": "Test error.",
            },
            {
                "class_name": "TestError",
                "type": "test-error",
                "title": "Test error.",
            },
            {
                "class_name": "UnauthorisedError",
                "type": "unauthorised",
                "title": "",
            },
        ],
    }


def test_get_error_codes_list():
    assert get_error_codes(["tests.error_codes_fixture"]).model_dump() == {
        "errors": [
            {
                "class_name": "NoCodeError",
                "type": "no-code",
                "title": "Test error.",
            },
            {
                "class_name": "TestError",
                "type": "test-error",
                "title": "Test error.",
            },
            {
                "class_name": "UnauthorisedError",
                "type": "unauthorised",
                "title": "",
            },
        ],
    }


def test_get_permissions(client):
    assert get_permissions(
        client.app,
        ignore_routes=["/openapi.json", "/docs/oauth2-redirect", "/docs", "/redoc"],
    ).model_dump() == {
        "routes": [
            {
                "logic_operator": "and",
                "methods": "GET",
                "path": "/something",
                "permission_pairs": [{"action": "core:register", "resource": "urn:{partition}:core::root:core"}],
                "summary": "Get Something.",
            },
            {
                "logic_operator": "or",
                "methods": "GET",
                "path": "/something_else",
                "permission_pairs": [
                    {"action": "core:register", "resource": "urn:{partition}:core::root:core"},
                    {"action": "core:access", "resource": "urn:{partition}:core::root:core"},
                ],
                "summary": "Get Something Else.",
            },
        ],
    }
