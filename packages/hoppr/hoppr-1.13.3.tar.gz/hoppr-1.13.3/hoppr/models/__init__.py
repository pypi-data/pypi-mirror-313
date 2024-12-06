"""Base model for Hoppr config files."""

from __future__ import annotations

import logging

from pathlib import Path
from threading import _RLock as RLock

from pydantic import Field

from hoppr.models.base import HopprBaseModel
from hoppr.models.credentials import (
    CredentialRequiredService,
    Credentials,
    CredentialsFile,
)
from hoppr.models.manifest import Manifest, ManifestFile, Repositories
from hoppr.models.sbom import Sbom
from hoppr.models.transfer import StageRef, Transfer, TransferFile
from hoppr.models.validation.checks import ValidateConfig

__all__ = [
    "Credentials",
    "CredentialsFile",
    "HopprBaseModel",
    "Manifest",
    "ManifestFile",
    "Transfer",
    "TransferFile",
    "ValidateConfig",
]


class HopprSchemaModel(HopprBaseModel):
    """Consolidated Hoppr config file schema definition."""

    __root__: CredentialsFile | ManifestFile | TransferFile = Field(..., discriminator="kind")


class HopprContext(HopprBaseModel):
    """Consolidated data model for Hoppr runtime context."""

    collect_root_dir: Path
    consolidated_sbom: Sbom
    credential_required_services: list[CredentialRequiredService] | None
    delivered_sbom: Sbom
    log_level: int = logging.INFO
    logfile_location: Path = Path("hoppr.log")
    logfile_lock: RLock
    max_attempts: int = 3
    max_processes: int
    previous_delivery: Path | str | None = None
    repositories: Repositories
    retry_wait_seconds: float = 5
    sboms: list[Sbom]
    stages: list[StageRef]
    strict_repos: bool = True
    signable_file_paths: list[Path] = []


HopprContext.update_forward_refs()
