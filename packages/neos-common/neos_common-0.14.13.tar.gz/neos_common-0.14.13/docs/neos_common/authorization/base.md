Module neos_common.authorization.base
=====================================

Classes
-------

`AccessValidator()`
:   

    ### Descendants

    * neos_common.authorization.validator.AccessValidator

    ### Methods

    `validate(self, user_id: uuid.UUID, actions: list[neos_common.base.Action | str], resources: list[neos_common.base.ResourceLike], logic_operator: str, *, return_allowed_resources: bool = True) ‑> tuple[uuid.UUID, list[str]]`
    :

`AccessValidatorDependency(*args, **kwargs)`
:   Define the base requirements for a dependency that returns an AccessValidator.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

`ActionResource(action: neos_common.base.Action, resource_type: neos_common.base.ResourceType, resource: neos_common.base.ResourceLike, resource_extractor: typing.Callable[[fastapi.Request], dict[str, str]] | None = None)`
:   ActionResource(action: neos_common.base.Action, resource_type: neos_common.base.ResourceType, resource: neos_common.base.ResourceLike, resource_extractor: 'typing.Callable[[fastapi.Request], dict[str, str]] | None' = None)

    ### Class variables

    `action: neos_common.base.Action`
    :

    `resource: neos_common.base.ResourceLike`
    :

    `resource_extractor: typing.Callable[[fastapi.Request], dict[str, str]] | None`
    :

    `resource_type: neos_common.base.ResourceType`
    :

`ActionResourceList(action_resources: list[neos_common.authorization.base.ActionResource], logic_operator: Literal['and', 'or'] = 'and')`
:   ActionResourceList(action_resources: list[neos_common.authorization.base.ActionResource], logic_operator: Literal['and', 'or'] = 'and')

    ### Class variables

    `action_resources: list[neos_common.authorization.base.ActionResource]`
    :

    `logic_operator: Literal['and', 'or']`
    :

`AuthorizationDependency(action_resources: neos_common.authorization.base.ActionResourceList | list[neos_common.authorization.base.ActionResource] | neos_common.authorization.base.ActionResource, *, return_allowed_resources: bool = False)`
:   Define the base requirements for a dependency that validates authorization.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

`ConfigDependency(*args, **kwargs)`
:   Define the base requirements for a dependency that returns Config.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

`HubClientDependency(*args, **kwargs)`
:   Define the base requirements for a dependency that returns an HubClient.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

`KeycloakClientDependency(*args, **kwargs)`
:   Define the base requirements for a dependency that returns a KeycloakClient.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

`SignatureValidator(*args, **kwargs)`
:   Define the base requirements for an object that can validate signed requests.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

    ### Descendants

    * neos_common.authorization.validator.SignatureValidator

    ### Methods

    `validate(self, request: fastapi.Request, action: list[neos_common.base.Action | str], resource: list[neos_common.base.ResourceLike], logic_operator: str, *, return_allowed_resources: bool)`
    :   Validate a request and return the associated user_id and resources.

`SignatureValidatorDependency(*args, **kwargs)`
:   Define the base requirements for a dependency that returns a SignatureValidator.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic