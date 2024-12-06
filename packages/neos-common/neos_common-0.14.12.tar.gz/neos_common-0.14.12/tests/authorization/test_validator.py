from unittest import mock

import pytest
from freezegun import freeze_time

from neos_common import base
from tests.authorization.conftest import Resource
from tests.conftest import AsyncMock

validator = pytest.importorskip("neos_common.authorization.validator")


class TestAccessValidator:
    async def test_init(self):
        access_validator = validator.AccessValidator("hub_client")
        assert access_validator._hub_client == "hub_client"

    async def test_validate(self):
        hub_client = mock.Mock(validate_token=AsyncMock(return_value=("1", ["*"])))

        access_validator = validator.AccessValidator(hub_client)

        action = base.Action("core:announce")
        resource = Resource.generate(
            partition="test",
            service="iam",
            identifier="id",
            account_id="root",
            resource_type="policy",
        )
        result = await access_validator.validate(
            "1",
            [action],
            [resource],
            logic_operator="and",
            return_allowed_resources=True,
        )
        assert result == ("1", ["*"])
        hub_client.validate_token.assert_called_once_with(
            principal="1",
            actions=[action],
            resources=[resource.urn],
            logic_operator="and",
            return_allowed_resources=True,
        )


class TestSignatureValidator:
    @freeze_time("2023-01-01 12:00:00")
    async def test_validate(self):
        mock_hub = AsyncMock()
        action = base.Action("core:announce")
        resource = Resource.generate(
            partition="test",
            service="iam",
            identifier="id",
            account_id="root",
            resource_type="policy",
        )

        request = mock.Mock(
            method="GET",
            url=mock.Mock(scheme="http", path="/", query=b"foo=bar"),
            headers={
                "x-amz-date": "20230101T120000Z",
                "x-amz-content-sha256": "f4eb19f40510b16354e25f8b339dca7a40e44dfb846214371c054677c42146d7",
                "Authorization": "AWS4-HMAC-SHA256 Credential=access-key/20230101/ksa/iam/aws4_request, SignedHeaders=x-amz-date, Signature=signature",
            },
            body=AsyncMock(return_value=b'{"foo": "bar"}'),
        )

        v = validator.SignatureValidator(mock_hub)

        await v.validate(request, [action], [resource], logic_operator="and")

        assert mock_hub.validate_signature.call_args == mock.call(
            "access-key",
            "AWS4",
            "20230101/ksa/iam/aws4_request",
            "AWS4-HMAC-SHA256\n20230101T120000Z\n20230101/ksa/iam/aws4_request\nf4eb19f40510b16354e25f8b339dca7a40e44dfb846214371c054677c42146d7",
            "signature",
            [action],
            [resource.urn],
            logic_operator="and",
            return_allowed_resources=False,
        )

    @freeze_time("2023-01-01 12:00:00")
    async def test_validate_neos(self):
        mock_hub = AsyncMock()
        action = base.Action("core:announce")
        resource = Resource.generate(
            partition="test",
            service="iam",
            identifier="id",
            account_id="root",
            resource_type="policy",
        )

        request = mock.Mock(
            method="GET",
            url=mock.Mock(scheme="http", path="/", query=b"foo=bar"),
            headers={
                "x-neos-date": "20230101T120000Z",
                "x-neos-content-sha256": "f4eb19f40510b16354e25f8b339dca7a40e44dfb846214371c054677c42146d7",
                "Authorization": "NEOS4-HMAC-SHA256 Credential=access-key/20230101/ksa/iam/neos4_request, SignedHeaders=x-neos-date, Signature=signature",
            },
            body=AsyncMock(return_value=b'{"foo": "bar"}'),
        )

        v = validator.SignatureValidator(mock_hub)

        await v.validate(request, [action], [resource], logic_operator="and")

        assert mock_hub.validate_signature.call_args == mock.call(
            "access-key",
            "NEOS4",
            "20230101/ksa/iam/neos4_request",
            "NEOS4-HMAC-SHA256\n20230101T120000Z\n20230101/ksa/iam/neos4_request\n08080976e88185ead32bc4fa943273bd050be5b639c3ba38115dfb9107c3221d",
            "signature",
            [action],
            [resource.urn],
            logic_operator="and",
            return_allowed_resources=False,
        )
