import logging
from uuid import UUID

import httpx
from aws4.key_pair import KeyPair

from neos_common import error
from neos_common.base import Action
from neos_common.client.base import NeosClient
from neos_common.schema import Contract

logger = logging.getLogger(__name__)


class HubClient(NeosClient):
    """Identity Access Manager and Registry client."""

    @property
    def service_name(self) -> str:
        return "Hub"

    @property
    def known_errors(self) -> set[str]:
        return {
            "policy-not-found",
            "core-already-registered",
            "core-not-registered",
            "data-product-already-registered",
            "data-product-not-registered",
            "core-already-subscribed",
            "core-not-subscribed",
            "core-host-not-defined",
            "data-product-has-active-subscriptions",
            "core-service-user-not-defined",
            "user-manager-service-error",
        }

    def process_response_with_mapping(self, response: httpx.Response) -> dict:
        try:
            return self.process_response(response)
        except (error.ServiceApiError, error.UnhandledServiceApiError) as exc:
            if exc.reason == "authorization-required":
                raise error.AuthorizationRequiredError(exc.debug) from exc
            if exc.reason == "invalid-authorization":
                raise error.InvalidAuthorizationError(exc.debug) from exc
            if exc.reason == "insufficient-permissions":
                raise error.InsufficientPermissionsError(exc.debug) from exc
            if exc.reason == "invalid-resource-format":
                raise error.InvalidResourceFormatError(exc.debug) from exc
            if exc.reason == "identity-access-manager-error":
                raise error.IdentityAccessManagerError(exc.debug) from exc
            if exc.reason == "signature-error":
                raise error.SignatureError(exc.debug) from exc
            raise

    def __init__(
        self,
        host: str,
        token: str | None,
        key_pair: KeyPair | None,
        account: str,
        partition: str,
    ) -> None:
        # TODO(edgy): Use a better error
        assert token is not None or key_pair is not None  # noqa: S101

        self._token = token
        self._key_pair = key_pair

        self._account = account
        self._partition = partition

        self._host = host
        self._principals = None

    @property
    def token(self) -> str | None:
        return self._token

    @property
    def key_pair(self) -> KeyPair | None:
        return self._key_pair

    @property
    def partition(self) -> str:
        return self._partition

    @property
    def iam_host(self) -> str:
        return f"{self._host}/iam"

    @property
    def registry_host(self) -> str:
        return f"{self._host}/registry"

    @property
    def validate_token_url(self) -> str:
        return f"{self.iam_host}/validate/token"

    @property
    def validate_signature_url(self) -> str:
        return f"{self.iam_host}/validate/signature"

    @property
    def core_url(self) -> str:
        return f"{self.registry_host}/core/{{identifier}}/announce"

    @property
    def data_product_url(self) -> str:
        return f"{self.registry_host}/core/{{identifier}}/data_product"

    @property
    def metadata_url(self) -> str:
        return f"{self.registry_host}/core/{{identifier}}/data_product/metadata"

    async def validate_token(
        self,
        principal: UUID,
        actions: list[Action],
        resources: list[str],
        logic_operator: str,
        *,
        return_allowed_resources: bool = False,
    ) -> tuple[UUID, list[str]]:
        r = await self._get(
            url=self.validate_token_url,
            params={
                "principal_id": principal,
                "action": [action.value for action in actions],
                "resource": resources,
                "logic_operator": logic_operator,
                "return_allowed_resources": return_allowed_resources,
            },
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        data = self.process_response_with_mapping(r)
        logger.info(data)
        return data["principal_id"], data["resources"]

    async def validate_signature(
        self,
        access_key: str,
        auth_schema: str,
        scope: str,
        challenge: str,
        signed_challenge: str,
        actions: list[Action],
        resources: list[str],
        logic_operator: str,
        *,
        return_allowed_resources: bool = False,
    ) -> tuple[UUID, list[str]]:
        r = await self._get(
            url=self.validate_signature_url,
            params={
                "access_key_id": access_key,
                "auth_schema": auth_schema,
                "scope": scope,
                "challenge": challenge,
                "signed_challenge": signed_challenge,
                "action": [action.value for action in actions],
                "resource": resources,
                "logic_operator": logic_operator,
                "return_allowed_resources": return_allowed_resources,
            },
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        data = self.process_response_with_mapping(r)

        return data["principal_id"], data["resources"]

    async def get_allowed_resources(
        self,
        principal_id: str,
        action: Action,
    ) -> list[str]:
        r = await self._get(
            f"{self.iam_host}/principal/{principal_id}/resource",
            params={"action": action.value},
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        d = self.process_response(r)

        return d["resources"]

    async def announce_core(self, host: str, version: str, core_identifier: str) -> None:
        r = await self._post(
            url=self.core_url.format(identifier=core_identifier),
            json={
                "host": host,
                "version": version,
            },
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        self.process_response(r)

    async def register_data_product(
        self,
        urn: str,
        name: str,
        metadata: dict,
        description: str,
        label: str,
        sanitized_name: str,
        data_product_type: str,
        engine: str,
        table: str,
        identifier: str,
        core_identifier: str,
        *,
        contract: Contract,
    ) -> None:
        """Registers a data product by sending a request to the specified endpoint.

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

        """
        json = {
            "urn": urn,
            "name": name,
            "metadata": metadata,
            "description": description,
            "label": label,
            "sanitized_name": sanitized_name,
            "data_product_type": data_product_type,
            "engine": engine,
            "table": table,
            "identifier": identifier,
            "contract": contract.model_dump(mode="json"),
        }
        logger.info(
            f"Register data product request: {json}",
        )

        r = await self._post(
            url=self.data_product_url.format(identifier=core_identifier),
            json=json,
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        self.process_response(r)

    async def update_data_product_metadata(
        self,
        urn: str,
        metadata: dict,
        description: str,
        core_identifier: str,
    ) -> None:
        r = await self._post(
            url=self.metadata_url.format(identifier=core_identifier),
            json={
                "urn": urn,
                "metadata": metadata,
                "description": description,
            },
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        self.process_response(r)

    async def deregister_data_product(self, urn: str, core_identifier: str) -> None:
        r = await self._delete(
            url=self.data_product_url.format(identifier=core_identifier),
            json={
                "urn": urn,
            },
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        self.process_response(r)
