"""Common options for typer commands."""

from __future__ import annotations

import logging
import os
import textwrap
import time

from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import ValidationError
from typer import BadParameter, CallbackParam, Context, Option

import hoppr.utils

from hoppr.exceptions import HopprLoadDataError
from hoppr.logger import HopprLogger
from hoppr.models.manifest import Manifest
from hoppr.models.sbom import Sbom

if TYPE_CHECKING:
    from collections.abc import Iterable


_logger: HopprLogger | None = None


def _log_file_callback(log_file: Path | None) -> Path:
    """Generate a default log file if none was specified.

    Args:
        log_file: Path to the log file if specified, otherwise None

    Returns:
        Path to either the log file that was passed or an automatically generated one
    """
    return log_file or Path(f"hoppr_{time.strftime('%Y%m%d-%H%M%S')}.log")


def _set_global_option(ctx: Context, param: CallbackParam, value: bool) -> bool:
    """Add option value to shared Click context. Allows interspersed CLI options/arguments.

    Args:
        ctx: Click context to update
        param: Typer metadata for the parameter
        value: The parameter value

    Returns:
        bool: The flag that was passed, unmodified
    """
    if param.name:
        ctx.params[param.name] = value

        if param.envvar and value:
            os.environ[str(param.envvar)] = "1"

    return value


basic_term_option: bool = Option(
    False,
    "-b",
    "--basic-term",
    callback=_set_global_option,
    help="Use simplified output for non-TTY or legacy terminal emulators",
    is_eager=True,
    envvar="HOPPR_BASIC_TERM",
    rich_help_panel="Global options",
    show_default=False,
)

experimental_option: bool = Option(
    False,
    "-x",
    "--experimental",
    callback=_set_global_option,
    help="Enable experimental features",
    is_eager=True,
    envvar="HOPPR_EXPERIMENTAL",
    rich_help_panel="Global options",
    show_default=False,
)

log_file_option: Path = Option(
    None,
    "-l",
    "--log",
    callback=_log_file_callback,
    help="File to which log will be written",
    is_eager=True,
    envvar="HOPPR_LOG_FILE",
    rich_help_panel="Global options",
    show_default=False,
)

strict_repos_option: bool = Option(
    True,
    "--strict/--no-strict",
    callback=_set_global_option,
    help="Utilize only manifest repositories for package collection",
    is_eager=True,
    envvar="HOPPR_STRICT_REPOS",
    rich_help_panel="Global options",
    show_default=False,
)

verbose_option: bool = Option(
    False,
    "-v",
    "--debug",
    "--verbose",
    callback=_set_global_option,
    help="Enable debug output",
    is_eager=True,
    rich_help_panel="Global options",
    show_default=False,
)


# ------------------------------------------------------------------------------------------------- #
# SBOM input options
# ------------------------------------------------------------------------------------------------- #
def _manifest_callback(manifest_file: Path | None) -> Path | None:
    """Load SBOM files from Hoppr manifest and populate the `--sbom-files` parameter variable.

    Args:
        manifest_file: Path to manifest file if specified, otherwise None

    Returns:
        The manifest file that was passed, unmodified
    """
    if manifest_file is None:
        return None

    # Load manifest file to populate `Sbom.loaded_sboms`
    Manifest.load(manifest_file)

    return manifest_file


def _sbom_callback(ctx: Context, sbom_sources: list[str | Path]) -> list[str | Path]:
    """Load SBOM input files.

    Args:
        ctx: Click context
        sbom_sources: Local SBOM files or URLs to parse

    Returns:
        The list of directories that was passed, unmodified
    """
    sbom_sources.extend(ctx.params.get("sbom_files", []))

    # Combine SBOM files from all CLI input file arguments
    log_file = Path(ctx.params.get("log_file", ""))
    verbose = bool(ctx.params.get("verbose"))
    _load_sbom_files(sbom_sources, log_file, verbose)

    return sbom_sources


def _sbom_dir_callback(ctx: Context, sbom_dirs: list[Path]) -> list[Path]:
    """Load SBOM files from input directories and populate the `--sbom-files` parameter variable.

    Args:
        ctx: Click context
        sbom_dirs: List of directories containing SBOM files

    Returns:
        The list of directories that was passed, unmodified
    """
    log_file = Path(ctx.params.get("log_file", ""))
    verbose = bool(ctx.params.get("verbose"))

    sbom_files: list[str | Path] = ctx.params.setdefault("sbom_files", [])

    def _is_sbom_file(json_file: Path) -> bool:
        try:
            data = hoppr.utils.load_file(json_file)
        except HopprLoadDataError:  # pragma: no cover
            return False

        return bool(data) and isinstance(data, dict) and data.get("bomFormat") == "CycloneDX"

    for sbom_dir in sbom_dirs:
        # Get all files with `.json` extension recursively containing the key value pair `"bomFormat": "CycloneDX"`
        sbom_dir_files = list(filter(_is_sbom_file, sbom_dir.rglob(pattern="*.json")))

        _load_sbom_files(sbom_dir_files, log_file, verbose)
        sbom_files.extend(sbom_dir_files)

    sbom_files = hoppr.utils.dedup_list(sbom_files)

    return sbom_dirs


def _load_sbom_files(sbom_files: Iterable[str | Path], log_file: Path, verbose: bool) -> None:
    """Load SBOM input files."""
    global _logger
    _logger = _logger or HopprLogger(
        name="hoppr",
        filename=str(log_file),
        level=logging.DEBUG if verbose else logging.INFO,
    )

    for sbom_file in sbom_files:
        try:
            Sbom.load(sbom_file)
        except ValidationError as ex:
            msg = f"'{sbom_file}' failed to validate against the CycloneDX schema"

            _logger.error(f"{msg}:\n{textwrap.indent(text=str(ex), prefix='    ')}")
            raise BadParameter(f"{msg}. See {log_file} for details.") from ex


manifest_file_option: Path = Option(
    None,
    "-m",
    "--manifest",
    callback=_manifest_callback,
    dir_okay=False,
    exists=True,
    help="Manifest file containing input SBOMs",
    resolve_path=True,
    show_default=False,
)

sbom_files_option: list[Path] = Option(
    [],
    "-s",
    "--sbom",
    callback=_sbom_callback,
    dir_okay=False,
    exists=True,
    help="Path to SBOM file (can be specified multiple times)",
    show_default=False,
)

sbom_dirs_option: list[Path] = Option(
    [],
    "-d",
    "--sbom-dir",
    callback=_sbom_dir_callback,
    exists=True,
    file_okay=False,
    help="Directory containing SBOM files (can be specified multiple times)",
    show_default=False,
)

sbom_urls_option: list[str] = Option(
    [],
    "-u",
    "--sbom-url",
    help="SBOM file URL (can be specified multiple times)",
    metavar="URL",
    show_default=False,
)
