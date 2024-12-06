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

    @freeze_time("2023-01-01 12:00:00")
    async def test_validate_binary_body(self):
        mock_hub = AsyncMock()
        action = base.Action("core:announce")
        resource = Resource.generate(
            partition="test",
            service="iam",
            identifier="id",
            account_id="root",
            resource_type="policy",
        )

        body = b"PAR1\x15\x00\x15\x16\x150,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x011\x18\x011\x16\x00(\x011\x18\x011\x00\x00\x00(\xb5/\xfd\x04\x00Y\x00\x00\x02\x00\x00\x00\x02\x01\x01\x00\x00\x001\xa4%\xf8\xcb\x15\x00\x15\x16\x150,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x012\x18\x012\x16\x00(\x012\x18\x012\x00\x00\x00(\xb5/\xfd\x04\x00Y\x00\x00\x02\x00\x00\x00\x02\x01\x01\x00\x00\x002\xf1\xee\xee1\x15\x00\x15\x16\x150,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x013\x18\x013\x16\x00(\x013\x18\x013\x00\x00\x00(\xb5/\xfd\x04\x00Y\x00\x00\x02\x00\x00\x00\x02\x01\x01\x00\x00\x003Yk\xbf\xfb\x15\x00\x15\x1e\x158,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x05Apple\x18\x05Apple\x16\x00(\x05Apple\x18\x05Apple\x00\x00\x00(\xb5/\xfd\x04\x00y\x00\x00\x02\x00\x00\x00\x02\x01\x05\x00\x00\x00Apple\x8f\x0b\x1b\xcd\x15\x00\x15 \x15:,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x06Orange\x18\x06Orange\x16\x00(\x06Orange\x18\x06Orange\x00\x00\x00(\xb5/\xfd\x04\x00\x81\x00\x00\x02\x00\x00\x00\x02\x01\x06\x00\x00\x00Orangel\xa2\x1cw\x15\x00\x15 \x15:,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x06Banana\x18\x06Banana\x16\x00(\x06Banana\x18\x06Banana\x00\x00\x00(\xb5/\xfd\x04\x00\x81\x00\x00\x02\x00\x00\x00\x02\x01\x06\x00\x00\x00BananaS\xae\x06\xb9\x15\x00\x15\x18\x152,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x0234\x18\x0234\x16\x00(\x0234\x18\x0234\x00\x00\x00(\xb5/\xfd\x04\x00a\x00\x00\x02\x00\x00\x00\x02\x01\x02\x00\x00\x0034\xf7\xa0\x11j\x15\x00\x15\x18\x152,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x0256\x18\x0256\x16\x00(\x0256\x18\x0256\x00\x00\x00(\xb5/\xfd\x04\x00a\x00\x00\x02\x00\x00\x00\x02\x01\x02\x00\x00\x0056\x9e\xc5\r\xa9\x15\x00\x15\x18\x152,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x0267\x18\x0267\x16\x00(\x0267\x18\x0267\x00\x00\x00(\xb5/\xfd\x04\x00a\x00\x00\x02\x00\x00\x00\x02\x01\x02\x00\x00\x0067\xee\xaa\nL\x15\x00\x15F\x15`,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x192024-12-04T12:05:25+01:00\x18\x192024-12-04T12:05:25+01:00\x16\x00(\x192024-12-04T12:05:25+01:00\x18\x192024-12-04T12:05:25+01:00\x00\x00\x00(\xb5/\xfd\x04\x00\x19\x01\x00\x02\x00\x00\x00\x02\x01\x19\x00\x00\x002024-12-04T12:05:25+01:00?f5@\x15\x00\x15F\x15`,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x192024-12-04T12:05:25+01:00\x18\x192024-12-04T12:05:25+01:00\x16\x00(\x192024-12-04T12:05:25+01:00\x18\x192024-12-04T12:05:25+01:00\x00\x00\x00(\xb5/\xfd\x04\x00\x19\x01\x00\x02\x00\x00\x00\x02\x01\x19\x00\x00\x002024-12-04T12:05:25+01:00?f5@\x15\x00\x15F\x15`,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18\x192024-12-04T12:05:25+01:00\x18\x192024-12-04T12:05:25+01:00\x16\x00(\x192024-12-04T12:05:25+01:00\x18\x192024-12-04T12:05:25+01:00\x00\x00\x00(\xb5/\xfd\x04\x00\x19\x01\x00\x02\x00\x00\x00\x02\x01\x19\x00\x00\x002024-12-04T12:05:25+01:00?f5@\x15\x00\x15\xea\x01\x15\x84\x02,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x16\x00(k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x00\x00\x00(\xb5/\xfd\x04\x00\xa9\x03\x00\x02\x00\x00\x00\x02\x01k\x00\x00\x00/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\xc4\xd8\x84\t\x15\x00\x15\xea\x01\x15\x84\x02,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x16\x00(k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x00\x00\x00(\xb5/\xfd\x04\x00\xa9\x03\x00\x02\x00\x00\x00\x02\x01k\x00\x00\x00/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\xc4\xd8\x84\t\x15\x00\x15\xea\x01\x15\x84\x02,\x15\x02\x15\x00\x15\x06\x15\x06\x1c\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x16\x00(k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x00\x00\x00(\xb5/\xfd\x04\x00\xa9\x03\x00\x02\x00\x00\x00\x02\x01k\x00\x00\x00/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\xc4\xd8\x84\t\x191\x02\x02\x02\x198\x011\x012\x013\x198\x011\x012\x013\x15\x00\x196\x00\x00\x00\x00\x191\x02\x02\x02\x198\x05Apple\x06Orange\x06Banana\x198\x05Apple\x06Orange\x06Banana\x15\x00\x196\x00\x00\x00\x00\x191\x02\x02\x02\x198\x0234\x0256\x0267\x198\x0234\x0256\x0267\x15\x00\x196\x00\x00\x00\x00\x191\x02\x02\x02\x198\x192024-12-04T12:05:25+01:00\x192024-12-04T12:05:25+01:00\x192024-12-04T12:05:25+01:00\x198\x192024-12-04T12:05:25+01:00\x192024-12-04T12:05:25+01:00\x192024-12-04T12:05:25+01:00\x15\x00\x196\x00\x00\x00\x00\x191\x02\x02\x02\x198k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsxk/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsxk/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x198k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsxk/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsxk/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x15\x00\x196\x00\x00\x00\x00\x19<\x16\x08\x15r\x16\x00\x00\x16z\x15r\x16\x02\x00\x16\xec\x01\x15r\x16\x04\x00\x00\x19<\x16\xde\x02\x15\x9a\x01\x16\x00\x00\x16\xf8\x03\x15\xa4\x01\x16\x02\x00\x16\x9c\x05\x15\xa4\x01\x16\x04\x00\x00\x19<\x16\xc0\x06\x15|\x16\x00\x00\x16\xbc\x07\x15|\x16\x02\x00\x16\xb8\x08\x15|\x16\x04\x00\x00\x19<\x16\xb4\t\x15\xe2\x02\x16\x00\x00\x16\x96\x0c\x15\xe2\x02\x16\x02\x00\x16\xf8\x0e\x15\xe2\x02\x16\x04\x00\x00\x19<\x16\xda\x11\x15\x9a\t\x16\x00\x00\x16\xf4\x1a\x15\x9a\t\x16\x02\x00\x16\x8e$\x15\x9a\t\x16\x04\x00\x00\x15\x02\x19l5\x00\x18\x0fparquet_go_root\x15\n\x00\x15\x0c\x15\x00\x15\x02\x18\x02id%\x00\x15\x00\x15\x00\x15\x00\x1c\x1c\x00\x00\x00\x15\x0c\x15\x00\x15\x02\x18\x05fruit%\x00\x15\x00\x15\x00\x15\x00\x1c\x1c\x00\x00\x00\x15\x0c\x15\x00\x15\x02\x18\x05count%\x00\x15\x00\x15\x00\x15\x00\x1c\x1c\x00\x00\x00\x15\x0c\x15\x00\x15\x02\x18\x0e__extracted_at%\x00\x15\x00\x15\x00\x15\x00\x1c\x1c\x00\x00\x00\x15\x0c\x15\x00\x15\x02\x18\n__filepath%\x00\x15\x00\x15\x00\x15\x00\x1c\x1c\x00\x00\x00\x16\x06\x19\x1c\x19\\&\x08\x1c\x15\x0c\x195\x06\x08\x00\x19\x18\x02id\x15\x0c\x16\x06\x16\x88\x02\x16\xd6\x02&\x08<\x18\x013\x18\x011\x16\x00(\x013\x18\x011\x00\x00\x16\xa6<\x152\x16\xa8-\x15:\x00&\xde\x02\x1c\x15\x0c\x195\x06\x08\x00\x19\x18\x05fruit\x15\x0c\x16\x06\x16\x94\x03\x16\xe2\x03&\xde\x02<\x18\x06Orange\x18\x05Apple\x16\x00(\x06Orange\x18\x05Apple\x00\x00\x16\xd8<\x15<\x16\xe2-\x15r\x00&\xc0\x06\x1c\x15\x0c\x195\x06\x08\x00\x19\x18\x05count\x15\x0c\x16\x06\x16\xa6\x02\x16\xf4\x02&\xc0\x06<\x18\x0267\x18\x0234\x16\x00(\x0267\x18\x0234\x00\x00\x16\x94=\x156\x16\xd4.\x15F\x00&\xb4\t\x1c\x15\x0c\x195\x06\x08\x00\x19\x18\x0e__extracted_at\x15\x0c\x16\x06\x16\xd8\x07\x16\xa6\x08&\xb4\t<\x18\x192024-12-04T12:05:25+01:00\x18\x192024-12-04T12:05:25+01:00\x16\x00(\x192024-12-04T12:05:25+01:00\x18\x192024-12-04T12:05:25+01:00\x00\x00\x16\xca=\x15<\x16\x9a/\x15\xda\x02\x00&\xda\x11\x1c\x15\x0c\x195\x06\x08\x00\x19\x18\n__filepath\x15\x0c\x16\x06\x16\x80\x1b\x16\xce\x1b&\xda\x11<\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x16\x00(k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x18k/drives/b!MQ9fxJoWKE6kuaOULF7bUw7DQKsh_IlJhBdZh6ZKbeRkHtCdmELYTaVH26RsQ1EZ/root:/Connector Test/Test 1.xlsx\x00\x00\x16\x86>\x15<\x16\xf41\x15\xb2\n\x00\x16\x9a*\x16\x06\x00\x00\t\x04\x00\x00PAR1"
        request = mock.Mock(
            method="GET",
            url=mock.Mock(scheme="http", path="/", query=b"foo=bar"),
            headers={
                "x-neos-date": "20230101T120000Z",
                "x-neos-content-sha256": "f4eb19f40510b16354e25f8b339dca7a40e44dfb846214371c054677c42146d7",
                "Authorization": "NEOS4-HMAC-SHA256 Credential=access-key/20230101/ksa/iam/neos4_request, SignedHeaders=x-neos-date, Signature=signature",
            },
            body=AsyncMock(return_value=body),
        )

        v = validator.SignatureValidator(mock_hub)

        await v.validate(request, [action], [resource], logic_operator="and")

        assert mock_hub.validate_signature.call_args == mock.call(
            "access-key",
            "NEOS4",
            "20230101/ksa/iam/neos4_request",
            "NEOS4-HMAC-SHA256\n20230101T120000Z\n20230101/ksa/iam/neos4_request\n6165f63a8c53a61e1e05933269db3eca53b2bbe6ef1d359057c5dd27dbe4d66b",
            "signature",
            [action],
            [resource.urn],
            logic_operator="and",
            return_allowed_resources=False,
        )
