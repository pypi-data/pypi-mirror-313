"""Enumeration to indicate how a plugin may change a BOM."""

from __future__ import annotations

import re as re

from enum import Enum
from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING

from hoppr_cyclonedx_models.cyclonedx_1_5 import (
    Component,
    CyclonedxSoftwareBillOfMaterialsStandard as Bom,
)
from pydantic import AnyUrl, Field, FileUrl, HttpUrl, SecretStr, root_validator
from typing_extensions import Self

from hoppr.models.base import HopprBaseModel

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pydantic.typing import DictStrAny


class LocalFile(HopprBaseModel):
    """LocalFile data model."""

    local: Path

    def __str__(self) -> str:
        return self.local.resolve().as_uri()


class OciFile(HopprBaseModel):
    """OciFile data model."""

    oci: AnyUrl | str

    def __str__(self) -> str:
        return str(self.oci)


class UrlFile(HopprBaseModel):
    """UrlFile data model."""

    url: HttpUrl | FileUrl | AnyUrl | str

    def __str__(self) -> str:
        return str(self.url)


class BomAccess(int, Enum):
    """Enumeration to indicate how a plugin may change a BOM."""

    NO_ACCESS = 0
    COMPONENT_ACCESS = 1
    FULL_ACCESS = 2

    def has_access_to(self, obj: object | None) -> bool:
        """Determine whether the specified value allows updates to an object."""
        match self:
            case BomAccess.NO_ACCESS:
                return obj is None
            case BomAccess.COMPONENT_ACCESS:
                return isinstance(obj, Component)
            case BomAccess.FULL_ACCESS:
                return isinstance(obj, Bom)


class PurlType(str, Enum):
    """Enumeration of supported purl types."""

    CARGO = "Cargo"
    DEB = "Deb"
    DOCKER = "Docker"
    GEM = "Gem"
    GENERIC = "Generic"
    GIT = "Git"
    GITHUB = "GitHub"
    GITLAB = "GitLab"
    GOLANG = "Golang"
    HELM = "Helm"
    MAVEN = "Maven"
    NPM = "NPM"
    NUGET = "NuGet"
    OCI = "OCI"
    PYPI = "PyPI"
    RAW = "Raw"
    REPO = "Repo"
    RPM = "RPM"

    def __str__(self) -> str:
        return self.value.lower()

    @classmethod
    def _missing_(cls, value: object):  # noqa: ANN206
        return next((member for member in cls if member.name == str(value).upper()), None)

    @classmethod
    def values(cls) -> Iterator[str]:
        """Iterate over enum member strings.

        Yields:
            Iterator[str]: Iterator of enum member strings.
        """
        yield from [str(member) for member in cls]


class RepositoryUrl(HopprBaseModel, allow_mutation=False, validate_assignment=True):
    """RepositoryUrl data model."""

    url: str = Field(...)
    scheme: str | None = Field(default=None)
    username: str | None = Field(default=None)
    password: SecretStr | str | None = Field(default=None)
    hostname: str | None = Field(default=None)
    port: int | None = Field(default=None)
    path: str | None = Field(default=None)
    query: str | None = Field(default=None)
    fragment: str | None = Field(default=None)
    netloc: str | None = Field(default=None, exclude=True)

    @root_validator(pre=True)
    @classmethod
    def validate_model(cls, values: DictStrAny) -> DictStrAny:
        """Validate RepositoryUrl model."""
        if not (url := values.get("url")):
            raise ValueError("Input parameter `url` must be a non-empty string")

        if url.endswith(":"):
            url = f"{url}//"

        if not (
            match := re.search(
                pattern=(
                    r"^((?P<scheme>[^:/?#]+):(?=//))?(//)?((("
                    r"?P<username>[^:]+)(?::("
                    r"?P<password>[^@]+)?)?@)?("
                    r"?P<hostname>[^@/?#:]*)(?::("
                    r"?P<port>\d+)?)?)?("
                    r"?P<path>[^?#]*)(\?("
                    r"?P<query>[^#]*))?(#("
                    r"?P<fragment>.*))?"
                ),
                string=url,
            )
        ):
            raise ValueError(f"Not a valid URL: {url}")

        values.update({name: value for name, value in match.groupdict().items() if value is not None})

        if values.get("port"):
            values["port"] = int(values["port"])

        if isinstance(password := values.get("password"), str):
            password = SecretStr(password)

        auth = ":".join(filter(None, [values.get("username"), values.get("password")]))
        host_port = ":".join(filter(None, [values.get("hostname"), str(values.get("port") or "")]))
        values["netloc"] = "@".join(filter(None, [auth, host_port]))

        values["url"] = f"{values['scheme']}://" if values.get("scheme") else ""
        values["url"] = f"{values['url']}{values['netloc']}"
        values["url"] = "/".join(filter(None, [values["url"], values["path"].strip("/") if values.get("path") else ""]))
        values["url"] = "?".join(filter(None, [values["url"], values.get("query")]))
        values["url"] = "#".join(filter(None, [values["url"], values.get("fragment")]))

        return values

    def __repr__(self) -> str:
        props = ", ".join(f"{name}={value!r}" for name, value in dict(self).items())
        return f"RepositoryUrl({props})"

    def __str__(self) -> str:
        return self.url

    def __truediv__(self, other: str) -> Self:
        return self.join(other)

    def __itruediv__(self, other: str) -> Self:
        # Convert all instances of two or more slashes to single slash
        other = "/".join(filter(None, other.split("/")))
        return self.join(other)

    def join(self, other: str) -> Self:  # noqa: D102
        # Convert two or more slashes to single slash (ignores `://`)
        joined = "/".join([re.sub(pattern="(?<!:)//+", repl="/", string=self.url), other.strip("/")])
        return type(self)(url=joined)


LocalFile.update_forward_refs()
