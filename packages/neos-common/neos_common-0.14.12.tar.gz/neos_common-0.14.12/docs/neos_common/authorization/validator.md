Module neos_common.authorization.validator
==========================================

Classes
-------

`AccessValidator(hub_client: neos_common.client.hub_client.HubClient)`
:   

    ### Ancestors (in MRO)

    * neos_common.authorization.base.AccessValidator

    ### Methods

    `validate(self, user_id: uuid.UUID, actions: list[neos_common.base.Action], resources: list[neos_common.base.ResourceLike], logic_operator: str, *, return_allowed_resources: bool = False) ‑> tuple[uuid.UUID, list[str]]`
    :

`SignatureValidator(hub_client: neos_common.client.hub_client.HubClient)`
:   Define the base requirements for an object that can validate signed requests.

    ### Ancestors (in MRO)

    * neos_common.authorization.base.SignatureValidator
    * typing.Protocol
    * typing.Generic