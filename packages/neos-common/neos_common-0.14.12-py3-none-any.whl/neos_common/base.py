import abc
import re
import typing as t
from dataclasses import dataclass
from enum import Enum

import pydantic

from neos_common import error

T = t.TypeVar("T", bound=pydantic.BaseModel)


STAR = "*"
ROOT = "root"


class Partition(Enum):
    ksa = "ksa"


class Service(Enum):
    iam = "iam"
    registry = "registry"
    core = "core"


class ResourceType(Enum):
    # Gateway
    data_system = "data_system"
    data_source = "data_source"
    data_product = "data_product"
    data_unit = "data_unit"
    output = "output"
    journal_note = "journal_note"
    notification = "notification"
    secret = "secret"  # noqa: S105
    spark = "spark"
    tag = "tag"

    # IAM
    account = "account"
    group = "group"
    policy = "policy"
    user = "user"
    token = "token"  # noqa: S105
    signature = "signature"
    statement = "statement"
    resource = "resource"
    principal = "principal"

    # Registry
    core = "core"
    product = "product"
    mesh = "mesh"

    # Storage
    postgres = "postgres"
    minio = "minio"

    # Superset
    dataset = "dataset"


class Action(Enum):
    """Action class base.

    When implementing IAM actions in a service, extend this class.
    """

    star = "*"

    # Gateway
    data_product_create = "data_product:create"
    data_product_browse = "data_product:browse"
    data_product_read = "data_product:read"
    data_product_manage = "data_product:manage"

    data_source_create = "data_source:create"
    data_source_browse = "data_source:browse"
    data_source_read = "data_source:read"
    data_source_manage = "data_source:manage"

    data_system_create = "data_system:create"
    data_system_browse = "data_system:browse"
    data_system_read = "data_system:read"
    data_system_manage = "data_system:manage"

    data_unit_create = "data_unit:create"
    data_unit_browse = "data_unit:browse"
    data_unit_read = "data_unit:read"
    data_unit_manage = "data_unit:manage"

    notification_read = "notification:read"
    notification_manage = "notification:manage"

    output_create = "output:create"
    output_browse = "output:browse"
    output_read = "output:read"
    output_manage = "output:manage"

    secret_create = "secret:create"  # noqa: S105
    secret_browse = "secret:browse"  # noqa: S105
    secret_read = "secret:read"  # noqa: S105
    secret_manage = "secret:manage"  # noqa: S105

    tag_create = "tag:create"
    tag_browse = "tag:browse"
    tag_manage = "tag:manage"

    # Special action for creating manual spark jobs for development tests.
    spark_develop = "spark:develop"

    journal_note_manage = "journal_note:manage"

    # IAM
    self = "self"  # Allow a user to perform an action on themselves

    account_create = "account:create"
    account_delete = "account:delete"
    account_manage = "account:manage"
    account_member = "account:member"

    user_create = "user:create"
    user_delete = "user:delete"
    user_manage = "user:manage"
    user_browse = "user:browse"

    group_create = "group:create"
    group_browse = "group:browse"
    group_read = "group:read"
    group_manage = "group:manage"

    policy_create = "policy:create"
    policy_browse = "policy:browse"
    policy_read = "policy:read"
    policy_manage = "policy:manage"

    key_manage = "key:manage"

    validate = "auth:validate"

    statement_browse = "statement:browse"
    resource_browse = "resource:browse"

    principal_browse = "principal:browse"

    # Registry
    core_announce = "core:announce"
    core_register = "core:register"
    core_migrate = "core:migrate"  # REMOVE
    core_manage = "core:manage"
    core_access = "core:access"
    _core_browse = "core:browse"  # DEPRECATED

    product_register = "product:register"
    product_update = "product:update"
    product_remove = "product:remove"

    product_consume = "product:consume"
    product_subscribe = "product:subscribe"

    # Storage
    postgres_read = "postgres:read"
    postgres_write = "postgres:write"
    postgres_manage = "postgres:manage"
    minio_read = "minio:read"
    minio_write = "minio:write"
    minio_manage = "minio:manage"

    # Superset
    dataset_read = "dataset:read"

    # Service
    service_core = "service:core"


class EffectEnum(Enum):
    """Default effect enum for use with IAM actions."""

    allow = "allow"
    deny = "deny"


ServiceResource = [
    # Gateway
    (Service.core, ResourceType.data_system),
    (Service.core, ResourceType.data_source),
    (Service.core, ResourceType.data_product),
    (Service.core, ResourceType.data_unit),
    (Service.core, ResourceType.output),
    (Service.core, ResourceType.journal_note),
    (Service.core, ResourceType.notification),
    (Service.core, ResourceType.secret),
    (Service.core, ResourceType.spark),
    (Service.core, ResourceType.tag),
    # IAM
    (Service.iam, ResourceType.account),
    (Service.iam, ResourceType.group),
    (Service.iam, ResourceType.policy),
    (Service.iam, ResourceType.principal),
    (Service.iam, ResourceType.resource),
    (Service.iam, ResourceType.signature),
    (Service.iam, ResourceType.statement),
    (Service.iam, ResourceType.token),
    (Service.iam, ResourceType.user),
    # Registry
    (Service.registry, ResourceType.core),
    (Service.registry, ResourceType.product),
    (Service.registry, ResourceType.mesh),
    # Storage
    (Service.core, ResourceType.postgres),
    (Service.core, ResourceType.minio),
    # Superset
    (Service.core, ResourceType.dataset),
]


RL = t.TypeVar("RL", bound="ResourceLike")


@dataclass
class ResourceLike:
    all_: str | None = None

    xrn: str = "urn"
    partition: str = ""
    service: str = ""
    identifier: str = ""
    account_id: str = ""
    resource_type: str = ""
    sub_type: str = ""
    resource_id: str | None = None

    PATTERN_RULE = "[a-zA-Z0-9_\\-]{1,50}"
    OPTIONAL_PATTERN_RULE = "[a-zA-Z0-9_\\-]{0,50}"
    SUB_RESOURCE_TYPE_RULE = "[a-z-]{1,50}"
    ADDITIONAL_PATTERN_RULE = r"(\*|[a-zA-Z0-9_\-]{1,50})"
    # Valid are:
    # - *
    # - urn or nrn
    # - urn:partition:service:identifier:account_id:resource_type
    # - urn:partition:service:identifier:account_id:resource_type:*
    # - urn:partition:service:identifier:account_id:resource_type:resource_id
    # - urn:partition:service:identifier:account_id:resource_type:sub-type:resource_id
    #
    # Invalid are:
    # Pathlike
    # - urn:partition:service:identifier:account_id:resource_type/resource_id
    # - urn:partition:service:identifier:account_id:resource_type:resource_id/sub/path
    # - urn:partition:service:identifier:account_id:resource_type:resource_id:sub:path
    rule = PATTERN_RULE
    optional_rule = OPTIONAL_PATTERN_RULE
    sub_rule = SUB_RESOURCE_TYPE_RULE
    additional_rule = ADDITIONAL_PATTERN_RULE
    RESOURCE_PATTERN = rf"^((?P<all_>\*)|(?P<xrn>[un]rn):(?P<partition>{rule}):(?P<service>{rule}):(?P<identifier>{optional_rule})?:(?P<account_id>{rule})?:(?P<resource_type>{rule})(([:](?P<sub_type>{sub_rule}))?[:](?P<resource_id>{additional_rule}))?)$"

    @classmethod
    def parse(cls: type[RL], s: str) -> RL:
        m = re.match(cls.RESOURCE_PATTERN, s)
        if not m:
            msg = f"Could not parse the resource {s}"
            raise error.InvalidResourceFormatError(msg)
        m_dict = m.groupdict()
        return cls(
            all_=m_dict["all_"],
            xrn=m_dict["xrn"] or "",
            partition=m_dict["partition"] or "",
            service=m_dict["service"] or "",
            identifier=m_dict["identifier"] or "",
            account_id=m_dict["account_id"] or "",
            resource_type=m_dict["resource_type"] or "",
            sub_type=m_dict["sub_type"] or "",
            resource_id=m_dict["resource_id"],
        )

    @property
    def urn(self) -> str:
        if self.all_:
            return self.all_

        full_xrn = (
            f"{self.xrn}:{self.partition}:{self.service}:{self.identifier}:{self.account_id}:{self.resource_type}"
        )
        if self.resource_id:
            resource_id = self.resource_id if not self.sub_type else f"{self.sub_type}:{self.resource_id}"
            full_xrn = f"{full_xrn}:{resource_id}"
        return full_xrn


RR = t.TypeVar("RR", bound="ResourceReader")


@dataclass
class ResourceReader(ResourceLike):
    STAR = "*"

    @classmethod
    def to_root(cls: type[RR], other: RR) -> RR:
        return cls(
            all_=other.all_,
            xrn=other.xrn,
            partition=other.partition,
            service=other.service,
            identifier=other.identifier,
            account_id="root",
            resource_type=other.resource_type,
            sub_type=other.sub_type,
            resource_id=other.resource_id,
        )

    def to_list(self) -> list[str]:
        if self.all_ is not None and self.is_any():
            return [self.all_]

        ret = [
            el or ""
            for el in [
                self.xrn,
                self.partition,
                self.service,
                self.identifier,
                self.account_id,
                self.resource_type,
                self.sub_type,
                self.resource_id,
            ]
        ]
        if not self.sub_type:
            ret.pop(6)

        return ret

    def is_any(self) -> bool:
        return self.all_ is not None and self.all_ == self.STAR

    def is_any_resource_id(self) -> bool:
        return self.resource_id == self.STAR

    def __getitem__(self, item: slice | int) -> str:
        """Get a specific item or subset of items from a resource.

        Examples:
        -------
        Resource("a:b:c:d")[0] -> "a"
        Resource("a:b:c:d")[1:3] -> "b:c"
        """
        if isinstance(item, slice):
            if item.stop == -1 and self.sub_type:
                item = slice(item.start, -2)
            return ":".join(self.to_list()[item]).rstrip(":")
        return self.to_list()[item]

    def __len__(self) -> int:
        """Return length of resource elements."""
        return len(self.to_list())


RB = t.TypeVar("RB", bound="ResourceBase")


@dataclass
class ResourceBase(abc.ABC, ResourceLike):
    """Resource class contains information about resource.

    Args:
    ----
        partition (str): geographic location of the system
        service (str): name of the service, for the core-gateway it is fixed to the core
        identifier (t.Union[str, None]): identifier of the core
        account_id (t.Union[str, None]): owner id of the core
        resource_type (str): name of the resource type
        resource_id (t.Union[str, None]): identificator of the resource, can have a nested structure
    """

    @classmethod
    def generate(
        cls: type[RB],
        xrn: str = "urn",
        partition: str = "partition",
        service: str = "service",
        identifier: str = "identifier",
        account_id: str = "owner",
        resource_type: str = "resource_type",
        sub_type: str = "",
        resource_id: str | tuple | None = None,
        all_: str | None = None,
    ) -> RB:
        """Generate Resource."""
        init_kwargs = {
            "xrn": xrn,
            "partition": partition,
            "service": service,
            "identifier": identifier or "",
            "account_id": account_id or "",
            "resource_type": resource_type,
            "sub_type": sub_type or "",
            "all_": all_,
        }

        if isinstance(resource_id, str):
            init_kwargs["resource_id"] = resource_id
        elif isinstance(resource_id, tuple):
            init_kwargs["resource_id"] = cls.format_resource_id(*resource_id)

        return cls(**init_kwargs)

    @property
    def urn_template(self) -> str:
        if self.all_:
            return self.all_

        full_xrn = (
            f"{self.xrn}:{self.partition}:{self.service}:{self.identifier}:{self.account_id}:{self.resource_type}"
        )
        if self.resource_id:
            resource_id = "{resource_id}" if not self.sub_type else f"{self.sub_type}:{{resource_id}}"
            full_xrn = f"{full_xrn}:{resource_id}"
        return full_xrn

    @classmethod
    @abc.abstractmethod
    def get_resource_id_template(cls) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def format_resource_id(cls, *args) -> str:
        pass
