from unittest import mock

import pytest

keycloak = pytest.importorskip("keycloak")
keycloak_client = pytest.importorskip("neos_common.client.keycloak_client")


@pytest.fixture
def client():
    return keycloak_client.KeycloakClient(
        "https://keycloak-host",
        "test-realm",
        "test-client",
        "test-secret",
    )


class TestKeycloakClient:
    def test_init(self):
        c = keycloak_client.KeycloakClient(
            "https://keycloak-host",
            "test-realm",
            "test-client",
            "test-secret",
        )

        assert c._host == "https://keycloak-host"
        assert c._realm == "test-realm"
        assert c._client_id == "test-client"
        assert c._client_secret == "test-secret"

    def test_openid(self, client, monkeypatch):
        mocked_thing = mock.Mock()
        monkeypatch.setattr(keycloak_client.keycloak, "KeycloakOpenID", mocked_thing)
        client.openid  # noqa: B018
        mocked_thing.assert_called_once_with(
            server_url="https://keycloak-host/auth",
            client_id="test-client",
            realm_name="test-realm",
            client_secret_key="test-secret",
        )

    def test_introspect_token(self, client, monkeypatch):
        monkeypatch.setattr(keycloak_client.keycloak.KeycloakOpenID, "introspect", mock.Mock())

        client.introspect_token("token")

        keycloak_client.keycloak.KeycloakOpenID.introspect.assert_called_once_with("token")

    def test_token_by_password(self, client, monkeypatch):
        mocked_thing = mock.Mock()
        monkeypatch.setattr(keycloak_client.keycloak.KeycloakOpenID, "token", mocked_thing)
        client.get_token_by_password("user", "password")
        mocked_thing.assert_called_once_with("user", "password")

    def test_refresh_token(self, client, monkeypatch):
        mocked_thing = mock.Mock()
        monkeypatch.setattr(keycloak_client.keycloak.KeycloakOpenID, "refresh_token", mocked_thing)
        client.refresh_token("token")
        mocked_thing.assert_called_once_with("token")

    def test_logout_user(self, client, monkeypatch):
        mocked_thing = mock.Mock()
        monkeypatch.setattr(keycloak_client.keycloak.KeycloakOpenID, "logout", mocked_thing)
        client.logout_user("token")
        mocked_thing.assert_called_once_with("token")

    def test_userinfo(self, client, monkeypatch):
        monkeypatch.setattr(keycloak_client.keycloak.KeycloakOpenID, "userinfo", mock.Mock())

        client.userinfo("token")

        keycloak_client.keycloak.KeycloakOpenID.userinfo.assert_called_once_with("token")

    def test_decode_token(self, client, monkeypatch):
        monkeypatch.setattr(keycloak_client.keycloak.KeycloakOpenID, "decode_token", mock.Mock())

        client.decode_token("token", "key")

        keycloak_client.keycloak.KeycloakOpenID.decode_token.assert_called_once_with("token", "key")

    @pytest.mark.parametrize(
        ("error", "expected"),
        [
            ('{"description": "thing"}', {"description": "thing"}),
            ("{unparsable JSON}", "{unparsable JSON}"),
            ("just some string", "just some string"),
        ],
    )
    def test_parse_error(self, client, error, expected):
        assert client.parse_error(keycloak.KeycloakError(error)) == expected
