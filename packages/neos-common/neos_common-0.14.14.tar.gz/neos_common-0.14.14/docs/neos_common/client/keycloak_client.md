Module neos_common.client.keycloak_client
=========================================

Classes
-------

`KeycloakClient(host: str, realm: str, client_id: str, client_secret: str)`
:   Keycloak client that provides routes to the Keycloak.

    ### Static methods

    `parse_error(keycloak_error: keycloak.exceptions.KeycloakError) ‑> str | dict[str, typing.Any]`
    :

    ### Instance variables

    `openid: keycloak.keycloak_openid.KeycloakOpenID`
    :   Returns the openid client for the Keycloak.

    ### Methods

    `decode_token(self, any_token: str, key: str) ‑> dict`
    :

    `get_token_by_password(self, user: str, password: str) ‑> dict`
    :   Retrieve access_token with user credentials.

    `introspect_token(self, token: str) ‑> dict`
    :   Retrieve introspect token from keycloak.
        
        Useful to validat that a user token is still active.

    `logout_user(self, refresh_token: str) ‑> dict`
    :   Logout of keycloak session.

    `refresh_token(self, refresh_token: str) ‑> dict`
    :   Obtain a new access_token using a refresh_token.

    `userinfo(self, token: str) ‑> dict`
    :   Get user info for supplied access_token.