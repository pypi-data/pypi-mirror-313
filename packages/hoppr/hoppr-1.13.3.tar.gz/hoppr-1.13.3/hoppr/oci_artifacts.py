"""Functions to faciliate interaction with non-image OCI Artifacts."""

from __future__ import annotations

import re

from pathlib import Path
from typing import TYPE_CHECKING

from oras.container import Container
from oras.provider import Registry
from pydantic import SecretStr

from hoppr import utils as utils
from hoppr.exceptions import HopprLoadDataError
from hoppr.models.credentials import Credentials

if TYPE_CHECKING:
    from oras.client import OrasClient

# Regex per: https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
SEM_VER_CORE_REGEX = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$"
SEM_VER_FULL_REGEX = (
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


def pull_artifact(
    artifact: str, allow_version_discovery: bool = False, version_regex: str = SEM_VER_CORE_REGEX
) -> dict:
    """Pulls OCI Artifact from registry into memory and returns content.

    If no version (tag) is provided on URL, hoppr can attempt to disover highest version if allow_version_discovery
    is enabled. A regex for match versions can be provided to handle less standard version formats.
    Default will look for SemVer2 core
    """
    pulled = _pull_artifact(artifact, allow_version_discovery=allow_version_discovery, version_regex=version_regex)

    # We should only get one. If we get more, just take the first
    loaded_content = utils.load_file(pulled)
    if not isinstance(loaded_content, dict):
        raise HopprLoadDataError("Pulled artifact data was not loaded as dictionary")

    return loaded_content


def pull_artifact_to_disk(
    artifact: str,
    target_dir: str,
    allow_version_discovery: bool = False,
    version_regex: str = SEM_VER_CORE_REGEX,
) -> Path:
    """Pulls OCI Artifact from registry to specified target_dir.

    If no version (tag) is provided on URL, hoppr can attempt to disover highest version if allow_version_discovery
    is enabled. A regex for match versions can be provided to handle less standard version formats.
    Default will look for SemVer2 core
    """
    return _pull_artifact(
        artifact,
        target_dir,
        allow_version_discovery=allow_version_discovery,
        version_regex=version_regex,
    )


def _create_client_info(artifact: str) -> tuple[Container, OrasClient]:
    """Utility function for creating ORAS client and intermediate objects."""
    # Use ORAS' Container object to faciliate parsing registry host
    container = Container(artifact)
    registry = Registry(hostname=container.registry)

    creds = Credentials.find(container.registry)
    if creds is not None and isinstance(creds.password, SecretStr):
        registry.auth.set_basic_auth(creds.username, creds.password.get_secret_value())

    return container, registry


def _pull_artifact(
    artifact: str,
    outdir: str | None = None,
    allow_version_discovery: bool = False,
    version_regex: str = SEM_VER_CORE_REGEX,
) -> Path:
    """Looks up and pulls artifact to disk from OCI registry."""
    container, client = _create_client_info(artifact)

    full_artifact = artifact
    # Only discover tag if it hasn't been explicitly defined.
    # We let the 'Container' do the parsing, so we'll just compare
    if not artifact.endswith(container.tag):
        if not allow_version_discovery:
            raise HopprLoadDataError(
                f"No version provided and version discovery is disabled. Cannot pull artifact {artifact}"
            )
        version_tag = _discover_highest_version_tag(artifact, version_regex=version_regex)
        full_artifact += f":{version_tag}"

    files = client.pull(target=full_artifact, outdir=outdir)
    return Path(files[0])


def _discover_highest_version_tag(artifact: str, version_regex: str = SEM_VER_CORE_REGEX) -> str:
    """Attempts to discover the highest versioned artifact based on provided regex.

    Default will use full SemVer.
    """
    container, client = _create_client_info(artifact)

    tags: list[str] = client.get_tags(str(container))

    # Only find those that match semver
    # Future enhancement can allow user to define regex to use in the artifact definition
    tags = sorted(filter(lambda x: re.match(version_regex, x), tags["tags"]))  # type: ignore[arg-type,call-overload]

    return sorted(tags)[-1]
