Module neos_common.authorization.util
=====================================

Functions
---------

`create_openapi_info(config: neos_common.config.Config, resource_class: type, *args: Union[tuple[neos_common.base.Action, neos_common.base.ResourceType, str | None], tuple[neos_common.base.Action, neos_common.base.ResourceType, str | None, str | None, str | None]], logic_operator: str = 'and') ‑> dict[str, str]`
:   Generate openapi info for use in FastAPI routes.

Classes
-------

`DepAccessValidatorFactory()`
:   Access validator dependency.

    ### Static methods

    `build(hub_client_dep: type[neos_common.authorization.base.HubClientDependency]) ‑> type[neos_common.authorization.base.AccessValidatorDependency]`
    :   Build an AccessValidatorDependency.
        
        Generate a fastapi dependency that creates an AccessValidator.

`DepAuthorizationFactory()`
:   Authorization dependency.
    
    Pull the config from the app.state and parse the token from the request.
    
    Returns:
    -------
        TokenData with information about current user.

    ### Static methods

    `build(config_dep: type[neos_common.authorization.base.ConfigDependency], keycloak_dep: type[neos_common.authorization.base.KeycloakClientDependency], signature_dep: type[neos_common.authorization.base.SignatureValidatorDependency], access_validator: type[neos_common.authorization.base.AccessValidatorDependency]) ‑> type[neos_common.authorization.base.AuthorizationDependency]`
    :   Build an AuthorizationDependency.
        
        Generate a fastapi dependency that validates incoming authorization
        headers and creates TokenData.

`DepHubClientFactory()`
:   

    ### Static methods

    `build(config_dep: type[neos_common.authorization.base.ConfigDependency]) ‑> type[neos_common.authorization.base.HubClientDependency]`
    :   Build an HubClientDependency.
        
        Generate a fastapi dependency that creates an HubClient.

`DepKeycloakClientFactory()`
:   Keycloak client dependency.
    
    Pull the config from the app.state, instantiate a keycloak client.
    
    Returns:
    -------
        KeycloakClient using configured keycloak parameters.

    ### Static methods

    `build(config_dep: type[neos_common.authorization.base.ConfigDependency]) ‑> type[neos_common.authorization.base.KeycloakClientDependency]`
    :   Build a KeycloakClientDependency.
        
        Generate a fastapi dependency that creates a KeycloakClient.