"""Schema for neosctl."""

import configparser
import dataclasses
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Auth(BaseModel):
    access_token: str = ""
    expires_in: Optional[int] = None
    refresh_token: str = ""
    refresh_expires_in: Optional[int] = None


class OptionalProfile(BaseModel):
    gateway_api_url: str = ""
    hub_api_url: str = ""
    storage_api_url: str = ""
    user: str = ""
    access_token: str = ""
    refresh_token: str = ""
    ignore_tls: bool = False
    account: str = ""
    http_proxy: str = ""


class Profile(OptionalProfile):
    gateway_api_url: str
    hub_api_url: str = ""
    storage_api_url: str
    user: str
    access_token: str
    refresh_token: str
    ignore_tls: bool
    account: str = "root"  # backwards compat default


class Core(BaseModel):
    name: str
    host: str
    account: Optional[str] = None
    active: bool = False

    @field_validator("account", mode="before")
    @classmethod
    def convert_null_account(cls: "type[Core]", v: str) -> Optional[str]:
        """Toml treats None as "null", convert back to None."""
        if v == "null":
            return None
        return v


class Env(BaseModel):
    name: str
    hub_api_url: str
    user: str
    access_token: str
    refresh_token: str
    ignore_tls: bool
    active: bool
    account: str = "root"
    http_proxy: Optional[str] = None
    cores: dict[str, Core] = Field(default_factory=dict)

    @field_validator("http_proxy", mode="before")
    @classmethod
    def convert_null_account(cls: "type[Env]", v: str) -> Optional[str]:
        """Toml treats None as "null", convert back to None."""
        if v == "null":
            return None
        return v


class Credential(BaseModel):
    access_key_id: str
    secret_access_key: str


@dataclasses.dataclass
class Common:
    env: dict
    credential: configparser.ConfigParser
    active_env: Optional[Env] = None
    active_core: Optional[Core] = None
    output_format: str = "json"
    fields: Optional[list[str]] = None

    @property
    def http_proxy(self) -> Optional[str]:
        """Return name configuration."""
        if self.active_env:
            return self.active_env.http_proxy

        return None

    @property
    def name(self) -> str:
        """Return name configuration."""
        if self.active_env:
            return self.active_env.name

        return ""

    @property
    def access_token(self) -> str:
        """Return access_token configuration."""
        if self.active_env:
            return self.active_env.access_token

        return ""

    @property
    def refresh_token(self) -> str:
        """Return access_token configuration."""
        if self.active_env:
            return self.active_env.refresh_token

        return ""

    @property
    def ignore_tls(self) -> bool:
        """Return ignore_tls configuration."""
        if self.active_env:
            return self.active_env.ignore_tls

        return False

    @property
    def account(self) -> str:
        """Return system account."""
        if self.active_env:
            return self.active_env.account

        return "root"

    @property
    def gateway_api_url(self) -> str:
        """Return gateway api url.

        If a user profile is provided and defines a gateway url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.active_core:
            return self.active_core.host

        return "unset"

    @property
    def storage_api_url(self) -> str:
        """Return storage api url.

        If a user profile is provided and defines a storage url, return that,
        otherwise or fall back to cli defined default.
        """
        if self.active_core:
            return self.active_core.host.replace("://", "://saas.").replace("/api/gateway", "")

        return "unset"

    @property
    def hub_api_url(self) -> str:
        """Return hub api url.

        If a user profile is provided and defines a hub url, return that,
        otherwise fall back to cli defined default.
        """
        if self.active_env:
            return self.active_env.hub_api_url

        return "unset"
