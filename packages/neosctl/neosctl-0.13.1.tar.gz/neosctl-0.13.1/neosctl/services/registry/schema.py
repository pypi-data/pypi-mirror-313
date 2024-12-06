"""Schema for registry service."""

from pydantic import BaseModel


class RegisterCore(BaseModel):
    name: str
    public: bool


class MigrateCore(BaseModel):
    urn: str
    account: str


class AddCoreContact(BaseModel):
    user_id: str
    role: str


class RemoveCoreContact(BaseModel):
    user_id: str
