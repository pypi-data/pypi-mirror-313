"""Credentials file data model."""

from __future__ import annotations

import os

from pathlib import Path
from typing import TYPE_CHECKING, Annotated, ClassVar, Literal

from pydantic import Field, FilePath, NoneStr, SecretStr, root_validator

from hoppr.models.base import HopprBaseModel, HopprBaseSchemaModel

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny


class CredentialRequiredService(HopprBaseModel):
    """CredentialRequiredService data model."""

    url: str
    user_env: NoneStr = Field(None)
    pass_env: NoneStr = Field(...)
    username: str = Field(..., alias="user")
    password: NoneStr | SecretStr = Field(None, exclude=True)

    @root_validator(pre=True, allow_reuse=True)
    @classmethod
    def validate_credential_required_service(cls, values: DictStrAny) -> DictStrAny:
        """Dynamically parse credentials using specified environment variables."""
        try:
            if (user_env := values.get("user_env")) is not None:
                if username := os.environ[user_env]:
                    values["user"] = username
                else:
                    raise ValueError(user_env)

            if (pass_env := values.get("pass_env")) is not None:
                if password := os.environ[pass_env]:
                    values["password"] = SecretStr(password)
                else:
                    raise ValueError(pass_env)
        except (KeyError, ValueError) as ex:
            raise ValueError(f"The environment variable {ex} must be set with a non-empty string") from ex

        return values


class CredentialsFile(HopprBaseSchemaModel):
    """Credentials file data model."""

    kind: Literal["Credentials"]
    credential_required_services: list[CredentialRequiredService] = Field(
        [],
        unique_items=True,
        description=(
            "List of CredentialRequiredService objects to provide "
            "authentication to remote repositories and/or registries"
        ),
    )


CredentialsMap = Annotated[dict[str, CredentialRequiredService], Field(...)]


class Credentials(CredentialsFile):
    """CredentialsModel populated with environment variable passwords."""

    lookup: ClassVar[CredentialsMap] = {}

    def __getitem__(self, item: str) -> CredentialRequiredService:
        return self.lookup[item]

    @root_validator(pre=True, allow_reuse=True)
    @classmethod
    def validate_credentials(cls, values: DictStrAny) -> DictStrAny:
        """Dynamically parse credentials using specified environment variables.

        Args:
            values (DictStrAny): Field values of root object being validated

        Raises:
            AssertionError: Environment variable not set

        Returns:
            DictStrAny: The modified field values
        """
        for service in values.get("credential_required_services", []):
            cls.lookup[service.get("url")] = CredentialRequiredService.parse_obj(service)

        return values

    @classmethod
    def find(cls, url: str) -> CredentialRequiredService | None:
        """Return credentials for a repo URL."""
        longest_matching_cred_url = ""

        for cred_url in cls.lookup:
            if cred_url in url and len(cred_url) > len(longest_matching_cred_url):
                longest_matching_cred_url = cred_url

        return cls.lookup.get(longest_matching_cred_url)

    @classmethod
    def load(cls, source: str | FilePath | DictStrAny | None) -> Credentials | None:
        """Load credentials file from local path or dict."""
        # Can't use structural pattern matching here, pylint falsely reports unsubscriptable-object
        if source is None:
            return None

        if isinstance(source, dict):
            return cls.parse_obj(source)

        if isinstance(source, str | Path):
            return cls.parse_file(source)

        raise TypeError("'source' argument must be one of: 'str', 'Path', 'dict[str, Any]'")
