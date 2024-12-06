import json
import typing

import keycloak


class KeycloakClient:
    """Keycloak client that provides routes to the Keycloak."""

    def __init__(self, host: str, realm: str, client_id: str, client_secret: str) -> None:
        self._host = host
        self._realm = realm
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def openid(self) -> keycloak.KeycloakOpenID:
        """Returns the openid client for the Keycloak."""
        return keycloak.KeycloakOpenID(
            server_url=f"{self._host}/auth",
            client_id=self._client_id,
            realm_name=self._realm,
            client_secret_key=self._client_secret,
        )

    def introspect_token(self, token: str) -> dict:
        """Retrieve introspect token from keycloak.

        Useful to validat that a user token is still active.
        """
        return self.openid.introspect(token)

    def get_token_by_password(self, user: str, password: str) -> dict:
        """Retrieve access_token with user credentials."""
        return self.openid.token(user, password)

    def refresh_token(self, refresh_token: str) -> dict:
        """Obtain a new access_token using a refresh_token."""
        return self.openid.refresh_token(refresh_token)

    def logout_user(self, refresh_token: str) -> dict:
        """Logout of keycloak session."""
        return self.openid.logout(refresh_token)

    def userinfo(self, token: str) -> dict:
        """Get user info for supplied access_token."""
        return self.openid.userinfo(token)

    def decode_token(self, any_token: str, key: str) -> dict:
        return self.openid.decode_token(any_token, key)

    @staticmethod
    def parse_error(keycloak_error: keycloak.KeycloakError) -> str | dict[str, typing.Any]:
        try:
            return json.loads(keycloak_error.error_message)
        except json.decoder.JSONDecodeError:
            return str(keycloak_error.error_message)
