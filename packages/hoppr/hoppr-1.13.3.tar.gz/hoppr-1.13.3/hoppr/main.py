"""Framework for manipulating bundles for airgapped transfers."""

from __future__ import annotations

import logging
import sys

from typing import TYPE_CHECKING

from typer import prompt

from hoppr.in_toto import generate_in_toto_layout
from hoppr.models.credentials import Credentials
from hoppr.models.manifest import Manifest
from hoppr.models.transfer import Transfer
from hoppr.processor import HopprProcessor as HopprProcessor

if TYPE_CHECKING:
    from pathlib import Path


def bundle(
    manifest_file: Path,
    credentials_file: Path | None,
    transfer_file: Path,
    log_file: Path | None,
    verbose: bool = False,
    strict_repos: bool = True,
    attest: bool = False,
    sign: bool = False,
    functionary_key_path: Path | None = None,
    functionary_key_prompt: bool = False,
    functionary_key_password: str | None = None,
    previous_delivery: Path | None = None,
    delivered_sbom: Path | None = None,
    basic_term: bool = False,
    experimental: bool = False,
    ignore_errors: bool = False,
):
    """Run the stages specified in the transfer config file on the content specified in the manifest."""
    log_level = logging.DEBUG if verbose else logging.INFO

    processor = HopprProcessor(
        transfer_file=transfer_file,
        manifest_file=manifest_file,
        credentials_file=credentials_file,
        attest=attest,
        sign=sign,
        functionary_key_path=functionary_key_path,
        functionary_key_password=functionary_key_password,
        log_level=log_level,
        log_file=log_file,
        strict_repos=strict_repos,
        previous_delivery=previous_delivery,
        ignore_errors=ignore_errors,
    )

    result = processor.run()

    if result.is_fail() and not ignore_errors:
        sys.exit(1)

    if delivered_sbom:
        delivered_sbom.write_text(processor.context.delivered_sbom.json(indent=2))


def generate_layout(
    transfer_file: Path,
    project_owner_key_path: Path,
    functionary_key_path: Path,
    project_owner_key_prompt: bool,
    project_owner_key_password: str,
):
    """Create in-toto layout based on transfer file."""
    if project_owner_key_prompt:
        project_owner_key_password = prompt(f"Enter password for {project_owner_key_path!s}", hide_input=True)

    transfer = Transfer.load(transfer_file)
    generate_in_toto_layout(
        transfer,
        project_owner_key_path,
        functionary_key_path,
        project_owner_key_password,
    )


def validate(input_files: list[Path], credentials_file: Path, transfer_file: Path):
    """Validate multiple manifest files for schema errors."""
    if credentials_file is not None:
        Credentials.load(credentials_file)

    if transfer_file is not None:
        Transfer.load(transfer_file)

    for file in input_files:
        Manifest.load(file)
