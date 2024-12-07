"""IAM service schemas."""

from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EffectEnum(Enum):
    allow = "allow"
    deny = "deny"


class Statement(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    sid: str
    principal: UUID
    action: list[str]
    resource: list[str]
    condition: Optional[list[str]] = None
    effect: EffectEnum = EffectEnum.allow


class Statements(BaseModel):
    statements: list[Statement]


class Policy(BaseModel):
    version: str = "2022-10-01"
    statements: list[Statement]


class UserPolicy(BaseModel):
    user: UUID
    policy: Policy


class CreateAccount(BaseModel):
    name: str = Field(..., pattern=r"^[a-z][a-z0-9_-]*$", max_length=50, min_length=3)
    display_name: str
    description: str
    owner: str


class UpdateAccount(BaseModel):
    display_name: str
    description: str
    owner: str


GROUP_NAME_FIELD = Field(pattern=r"^[a-zA-Z0-9_][a-zA-Z0-9_\- ]{0,254}$")
GROUP_DESCRIPTION_FIELD = Field(None, max_length=1000)


class CreateUpdateGroup(BaseModel):
    name: str = GROUP_NAME_FIELD
    description: Optional[str] = GROUP_DESCRIPTION_FIELD


class Principals(BaseModel):
    principals: list[str]


class CreateUser(BaseModel):
    username: str
    enabled: bool
    first_name: str
    last_name: str
    email: str
