import enum
from uuid import UUID

import pydantic

from neos_common import base

ResourcePattern = pydantic.constr(pattern=base.ResourceBase.RESOURCE_PATTERN)


class Statement(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    sid: str
    principal: list[str] | UUID
    action: list[str]
    resource: list[ResourcePattern]  # type: ignore[reportGeneralTypeIssues]
    condition: list[str] = pydantic.Field(default_factory=list)
    effect: base.EffectEnum

    def is_allowed(self) -> bool:
        return self.effect == base.EffectEnum.allow.value


class PriorityStatement(Statement):
    priority: int


class Statements(pydantic.BaseModel):
    statements: list[Statement]


class PriorityStatements(pydantic.BaseModel):
    statements: list[PriorityStatement]


class PrincipalType(enum.Enum):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    user = "user"
    group = "group"


class Principal(pydantic.BaseModel):
    principal_id: str
    principal_type: PrincipalType


class Principals(pydantic.BaseModel):
    principals: list[Principal]

    def get_principal_ids(self) -> list[str]:
        return [p.principal_id for p in self.principals]


class ErrorCode(pydantic.BaseModel):
    """Error code."""

    class_name: str
    type_: str = pydantic.Field(alias="type")
    title: str

    def model_dump(self, *args, **kwargs) -> dict:
        kwargs["by_alias"] = True
        return super().model_dump(*args, **kwargs)


class ErrorCodes(pydantic.BaseModel):
    """Error codes."""

    errors: list[ErrorCode]

    def model_dump(self, *args, **kwargs) -> dict:
        kwargs["by_alias"] = True
        return super().model_dump(*args, **kwargs)


class PermissionPair(pydantic.BaseModel):
    """Permission pair."""

    action: str
    resource: str


class FormattedRoute(pydantic.BaseModel):
    """Formatted route."""

    methods: str
    path: str
    permission_pairs: list[PermissionPair]
    summary: str | None = None
    logic_operator: str = "and"


class FormattedRoutes(pydantic.BaseModel):
    routes: list[FormattedRoute]


class Visibility(str, enum.Enum):
    """Enumeration representing visibility levels."""

    PRIVATE = "private"
    PUBLIC = "public"


class Subscription(pydantic.BaseModel):
    """Subscription model for contract approval status."""

    approval: bool


class Contract(pydantic.BaseModel):
    """Contract model containing visibility and subscription details."""

    visibility: Visibility
    subscription: Subscription
