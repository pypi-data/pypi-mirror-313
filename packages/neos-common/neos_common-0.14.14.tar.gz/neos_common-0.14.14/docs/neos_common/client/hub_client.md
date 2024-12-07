Module neos_common.client.hub_client
====================================

Classes
-------

`HubClient(host: str, token: str | None, key_pair: aws4.key_pair.KeyPair | None, account: str, partition: str)`
:   Identity Access Manager and Registry client.

    ### Ancestors (in MRO)

    * neos_common.client.base.NeosClient
    * typing.Protocol
    * typing.Generic

    ### Instance variables

    `core_url: str`
    :

    `data_product_url: str`
    :

    `iam_host: str`
    :

    `key_pair: aws4.key_pair.KeyPair | None`
    :

    `known_errors: set[str]`
    :

    `metadata_url: str`
    :

    `partition: str`
    :

    `registry_host: str`
    :

    `service_name: str`
    :

    `token: str | None`
    :

    `validate_signature_url: str`
    :

    `validate_token_url: str`
    :

    ### Methods

    `announce_core(self, host: str, version: str, core_identifier: str) ‑> None`
    :

    `deregister_data_product(self, urn: str, core_identifier: str) ‑> None`
    :

    `get_allowed_resources(self, principal_id: str, action: neos_common.base.Action) ‑> list[str]`
    :

    `process_response_with_mapping(self, response: httpx.Response) ‑> dict`
    :

    `register_data_product(self, urn: str, name: str, metadata: dict, description: str, label: str, sanitized_name: str, data_product_type: str, engine: str, table: str, identifier: str, core_identifier: str, *, contract: neos_common.schema.Contract) ‑> None`
    :   Registers a data product by sending a request to the specified endpoint.
        
        Args:
            urn (str): Unique resource name.
            name (str): Data product name.
            metadata (dict): Additional metadata.
            description (str): Brief data product description.
            label (str): Product label or category.
            sanitized_name (str): Sanitized version of the name.
            data_product_type (str): Type of data product.
            engine (str): Data engine used.
            table (str): Table or collection name.
            identifier (str): Unique data product identifier.
            core_identifier (str): Identifier for URL formatting.
            contract (Contract): Contract defining visibility and subscription.
        
        Returns:
            None: Function returns None.

    `update_data_product_metadata(self, urn: str, metadata: dict, description: str, core_identifier: str) ‑> None`
    :

    `validate_signature(self, access_key: str, auth_schema: str, scope: str, challenge: str, signed_challenge: str, actions: list[neos_common.base.Action], resources: list[str], logic_operator: str, *, return_allowed_resources: bool = False) ‑> tuple[uuid.UUID, list[str]]`
    :

    `validate_token(self, principal: uuid.UUID, actions: list[neos_common.base.Action], resources: list[str], logic_operator: str, *, return_allowed_resources: bool = False) ‑> tuple[uuid.UUID, list[str]]`
    :