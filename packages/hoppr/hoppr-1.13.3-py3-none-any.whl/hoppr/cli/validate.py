"""`validate` subcommand for `hopctl`."""

from __future__ import annotations

import functools
import json
import logging
import os
import sys

from datetime import date, datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Literal, TypeAlias, cast

from pydantic.utils import deep_update
from rich.console import Group
from rich.live import Live
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from typer import Argument, BadParameter, CallbackParam, Context, Option, Typer

import hoppr.main
import hoppr.models.validation
import hoppr.net
import hoppr.utils

from hoppr.cli.layout import HopprBasePanel, HopprSbomFilesLayout, console
from hoppr.cli.options import (
    basic_term_option,
    experimental_option,
    log_file_option,
    manifest_file_option,
    sbom_dirs_option,
    sbom_files_option,
    sbom_urls_option,
    verbose_option,
)
from hoppr.logger import HopprLogger
from hoppr.models.licenses import LicenseExpressionItem, LicenseMultipleItem
from hoppr.models.sbom import Component, Metadata, Sbom
from hoppr.models.types import LocalFile, UrlFile
from hoppr.models.validate import (
    ValidateCheckResult,
    ValidateComponentResult,
    ValidateLicenseResult,
    ValidateSbomResult,
)
from hoppr.models.validation.checks import ValidateConfig
from hoppr.result import ResultStatus

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping

    from rich.console import Console, ConsoleOptions, RenderResult

    DictStrAny: TypeAlias = dict[str, Any]

CURRENT_DATE: Final[date] = date.today()
EXPIRATION_DAYS: float = 30

RESULT_MAP: Final[Mapping[ResultStatus, Text]] = {
    ResultStatus.FAIL: Text("\u274c\ufe0f"),
    ResultStatus.SUCCESS: Text.from_markup("[green]\u2714"),
    ResultStatus.WARN: Text("\u26a0\ufe0f"),
}

STRICT_ALL = False
STRICT_LICENSE = False
STRICT_NTIA = False

layout: HopprSbomFilesLayout
logger: HopprLogger

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Validate CycloneDX SBOMs or Hoppr config files",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

LICENSE_FAIL_LOG_LEVEL: int
LICENSE_FAIL_RESULT: ValidateCheckResult
NTIA_FAIL_LOG_LEVEL: int
NTIA_FAIL_RESULT: ValidateCheckResult


class HopprValidateSummary(HopprBasePanel):
    """`hopctl validate sbom` results summary."""

    summary_group = Group()

    def __init__(self, *args, title: str | None = "Summary", log_file: Path, **kwargs) -> None:
        self.log_file = log_file
        self.results: list[ValidateSbomResult] = []

        super().__init__(self.summary_group, title, *args, **kwargs)

    def _component_ntia_row(self, component_results: list[ValidateComponentResult]) -> tuple[str, Text]:
        component_ntia_fails = [cr for cr in component_results if not cr.ntia_fields_result.is_success()]
        ntia_fail_status = RESULT_MAP[NTIA_FAIL_RESULT.status]

        return (
            f"{len(component_ntia_fails)} out of {len(component_results)} components missing minimum NTIA fields",
            ntia_fail_status if component_ntia_fails else RESULT_MAP[ResultStatus.SUCCESS],
        )

    def _license_fields_row(
        self,
        license_results: list[ValidateLicenseResult],
        result_type: Literal["component", "SBOM"],
    ) -> tuple[str, Text]:
        license_field_fails = [lr for lr in license_results if not lr.required_fields.is_success()]

        license_fail_status = RESULT_MAP[LICENSE_FAIL_RESULT.status]

        return (
            f"{len(license_field_fails)} out of {len(license_results)} "
            f"{result_type} licenses missing minimum license fields",
            license_fail_status if license_field_fails else RESULT_MAP[ResultStatus.SUCCESS],
        )

    def _license_expiration_row(
        self,
        license_results: list[ValidateLicenseResult],
        result_type: Literal["component", "SBOM"],
    ) -> tuple[str, Text]:
        license_exp_fails = [lr for lr in license_results if not lr.expiration.is_success()]

        license_fail_status = RESULT_MAP[LICENSE_FAIL_RESULT.status]

        return (
            f"{len(license_exp_fails)} out of {len(license_results)} "
            f"{result_type} licenses expired or expiring within {EXPIRATION_DAYS:n} days",
            license_fail_status if license_exp_fails else RESULT_MAP[ResultStatus.SUCCESS],
        )

    def __rich_console__(self, console_: Console, options: ConsoleOptions) -> RenderResult:
        for sbom_result in self.results:
            component_license_checks = [lr for cr in sbom_result.component_results for lr in cr.license_results]

            self.summary_group.renderables.append(f"Results for {sbom_result.name}:")
            summary_table = Table.grid(padding=(0, 4), pad_edge=True)

            for result in [
                sbom_result.spec_version_result,
                sbom_result.ntia_fields_result,
            ]:
                summary_table.add_row(result.message, RESULT_MAP[result.status])

            # Add SBOM metadata license results summary rows
            summary_table.add_row(*self._license_fields_row(sbom_result.license_results, "SBOM"))
            summary_table.add_row(*self._license_expiration_row(sbom_result.license_results, "SBOM"))

            # Add component NTIA minimum fields and license results summary rows
            summary_table.add_row(*self._component_ntia_row(sbom_result.component_results))
            summary_table.add_row(*self._license_fields_row(component_license_checks, "component"))
            summary_table.add_row(*self._license_expiration_row(component_license_checks, "component"))

            self.summary_group.renderables.append(summary_table)
            self.summary_group.renderables.append(Rule(style="[white]rule.line"))

        self.summary_group.renderables.append(f"See log file {self.log_file} for full results.")

        if hoppr.utils.is_basic_terminal():
            console_.line()
            console_.rule(title="Summary", characters="=", style="[bold]rule.line")
            console_.print(self.summary_group)
            return []

        return super().__rich_console__(console_, options)


class ValidateOutputFormat(str, Enum):
    """Output format for `hopctl validate sbom` when specifying an output file."""

    GITLAB = "gitlab"
    JSON = "json"


def _init_globals(
    log_file: Path,
    verbose: bool,
    expiration_days: float,
    strict: bool,
    strict_license_fields: bool,
    strict_ntia_minimum_fields: bool,
):
    global layout, logger

    logger = HopprLogger(
        name="hopctl-validate",
        filename=str(log_file),
        level=logging.DEBUG if verbose else logging.INFO,
    )

    layout = HopprSbomFilesLayout()

    global EXPIRATION_DAYS, STRICT_ALL, STRICT_LICENSE, STRICT_NTIA

    EXPIRATION_DAYS = expiration_days
    STRICT_ALL = strict
    STRICT_LICENSE = strict_license_fields
    STRICT_NTIA = strict_ntia_minimum_fields

    global LICENSE_FAIL_LOG_LEVEL, LICENSE_FAIL_RESULT, NTIA_FAIL_LOG_LEVEL, NTIA_FAIL_RESULT

    LICENSE_FAIL_LOG_LEVEL = logging.ERROR if STRICT_LICENSE else logging.WARN
    LICENSE_FAIL_RESULT = ValidateCheckResult.fail() if STRICT_LICENSE else ValidateCheckResult.warn()
    NTIA_FAIL_LOG_LEVEL = logging.ERROR if STRICT_NTIA else logging.WARN
    NTIA_FAIL_RESULT = ValidateCheckResult.fail() if STRICT_NTIA else ValidateCheckResult.warn()


def _available_profiles() -> Iterator[str]:
    """Iterate over available validation profiles.

    Returns:
        Iterator of available profiles
    """
    profile_dir = Path(hoppr.models.validation.__file__).parent / "profiles"

    yield from (path.name.removesuffix(".config.yml") for path in profile_dir.glob("*.config.yml"))


def _profile_callback(profile: str | None) -> str:
    """Verifies that the profile given exists or is None.

    Args:
        profile: The parameter value passed in

    Returns:
        The flag that was passed or "default" if not
    """
    if profile not in [None, *_available_profiles()]:
        raise BadParameter(f"Specified profile '{profile}' is invalid. Must be one of {_available_profiles()}")

    return "default" if profile is None else profile


def _config_file_callback(ctx: Context, config_file: Path | None) -> Path:
    """Returns the config file to use for SBOM validation.

    Order of precedence:
      1. User specified path
      2. ~/.config/hoppr.config.yml
      3. ./hoppr.config.yml
      4. default config located at hoppr/models/validation/profiles/default.config.yml

    Args:
        ctx: Click context to update
        config_file: The parameter value passed in

    Returns:
        The path to the config file to use
    """
    profiles_dir = Path(hoppr.models.validation.__file__).parent / "profiles"
    profile = ctx.params.get("profile", "default")

    config_file = cast(Path, config_file or next(
            (
                cfg for cfg in [
                    Path.home() / ".config" / "hoppr.config.yml",
                    Path.cwd() / "hoppr.config.yml",
                ]
                if cfg.exists()
            ),
            profiles_dir / f"{profile}.config.yml",
        ),
    )  # fmt: skip

    # Update merged config with config file values
    merged_config = cast(dict[str, Any], hoppr.utils.load_file(profiles_dir / f"{profile}.config.yml"))
    config_dict = cast(dict[str, Any], hoppr.utils.load_file(config_file))
    merged_config = deep_update(merged_config, config_dict)

    # Load the configuration
    ValidateConfig.parse_obj(merged_config)

    return config_file


def _expiration_days_callback(expiration_days: float) -> float:
    os.environ["HOPPR_EXPIRATION_DAYS"] = str(int(expiration_days))

    return expiration_days


def _set_all_strict(ctx: Context, param: CallbackParam, value: bool) -> bool:
    """Set all strict flags to `True`.

    Args:
        ctx (Context): Click context to update
        param (CallbackParam): Typer metadata for the parameter
        value (bool): The parameter value

    Returns:
        bool: The flag that was passed, unmodified
    """
    if param.name and value:
        ctx.params[param.name] = True
        ctx.params["strict_ntia_minimum_fields"] = True
        ctx.params["strict_license_fields"] = True

    return value


def _check_fields(
    obj: object | None,
    *field_names: str,
    fail_log_level: int = logging.WARN,
    fail_result: ValidateCheckResult = ValidateCheckResult.warn(),  # noqa: B008
    indent_level: int = 1,
) -> ValidateCheckResult:
    result = ValidateCheckResult.success()

    if isinstance(obj, dict):
        field_values = (obj.get(field_name) for field_name in field_names)
    else:
        field_values = (getattr(obj, field_name, None) for field_name in field_names)

    if obj is None or not any(field_values):
        missing_fields = ", ".join(f"`{name}`" for name in field_names)
        logger.log(
            fail_log_level,
            "Missing %s field",
            missing_fields,
            indent_level=indent_level,
        )

        result.merge(fail_result)

    return result


def _check_license_expiration(
    license_: LicenseMultipleItem | LicenseExpressionItem,
) -> ValidateCheckResult:
    if isinstance(license_, LicenseExpressionItem) or not license_.license.licensing:
        return LICENSE_FAIL_RESULT

    try:
        # Raises `ValueError` if `expiration` is `None`
        expiration = datetime.fromisoformat(str(license_.license.licensing.expiration))
        if expiration.date() < CURRENT_DATE + timedelta(days=EXPIRATION_DAYS):
            raise ValueError
    except ValueError:
        logger.log(
            LICENSE_FAIL_LOG_LEVEL,
            "License expired or expiring within %d days",
            EXPIRATION_DAYS,
            indent_level=3,
        )

        return LICENSE_FAIL_RESULT

    return ValidateCheckResult.success()


def _check_license_fields(
    license_: LicenseMultipleItem | LicenseExpressionItem,
) -> ValidateCheckResult:
    required_fields_result = ValidateCheckResult.success()

    if isinstance(license_, LicenseExpressionItem):  # pragma no cover
        required_fields_result.merge(LICENSE_FAIL_RESULT)
        return required_fields_result

    check_license_fields = functools.partial(
        _check_fields,
        fail_log_level=LICENSE_FAIL_LOG_LEVEL,
        fail_result=LICENSE_FAIL_RESULT,
        indent_level=3,
    )

    required_fields_result.merge(check_license_fields(license_.license, "id", "name"))
    required_fields_result.merge(check_license_fields(license_.license, "licensing"))
    return required_fields_result


def _check_spec_version(sbom_dict: dict[str, Any]) -> ValidateCheckResult:
    result = ValidateCheckResult.success()

    match sbom_dict.get("specVersion"):
        case "1.2" | None:
            result.merge(ValidateCheckResult.fail())
        case "1.3" | "1.4":
            result.merge(ValidateCheckResult.fail() if STRICT_ALL else ValidateCheckResult.warn())

    return result


def _validate_component(component: Component) -> ValidateComponentResult:
    component_id = "@".join(filter(None, [component.name, component.version]))
    comp_result = ValidateComponentResult(component_id=component_id)

    logger.info("Validating component: %s", component_id, indent_level=1)

    check_component_fields = functools.partial(
        _check_fields,
        fail_log_level=NTIA_FAIL_LOG_LEVEL,
        fail_result=NTIA_FAIL_RESULT,
        indent_level=2,
    )

    # Validate minimum required NTIA fields for component
    comp_result.ntia_fields_result.merge(check_component_fields(component, "supplier"))
    comp_result.ntia_fields_result.merge(check_component_fields(component, "name"))
    comp_result.ntia_fields_result.merge(check_component_fields(component, "version"))
    comp_result.ntia_fields_result.merge(check_component_fields(component, "cpe", "purl", "swid"))
    comp_result.result.merge(comp_result.ntia_fields_result)

    license_results = _validate_licenses(component)

    for license_result in license_results:
        comp_result.license_results.append(license_result)

        # Merge license result into final result for this SBOM
        comp_result.result.merge(license_result.required_fields)
        comp_result.result.merge(license_result.expiration)

    return comp_result


def _validate_licenses(obj: Metadata | Component | None) -> list[ValidateLicenseResult]:
    license_results: list[ValidateLicenseResult] = []

    if not obj or not obj.licenses:
        logger.log(LICENSE_FAIL_LOG_LEVEL, "Missing `licenses` field", indent_level=2)

        license_result = ValidateLicenseResult(license_id="Missing license data")
        license_result.required_fields.merge(LICENSE_FAIL_RESULT)
        license_result.expiration.merge(LICENSE_FAIL_RESULT)
        license_results.append(license_result)

        return license_results

    for license_ in obj.licenses:
        license_id = (
            license_.expression
            if isinstance(license_, LicenseExpressionItem)
            else str(license_.license.id or license_.license.name)
        )

        logger.info("Validating license: %s", license_id, indent_level=2)

        license_result = ValidateLicenseResult(license_id=license_id)
        license_result.required_fields.merge(_check_license_fields(license_))

        # Validate license expiration not within specified number of days
        license_result.expiration.merge(_check_license_expiration(license_))

        license_results.append(license_result)

    return license_results


def _validate_sbom(name: str, sbom_data: dict[str, Any]) -> ValidateSbomResult:
    sbom_result = ValidateSbomResult(name=name)

    # Check raw `specVersion` and NTIA minimum fields values before parsing data as Sbom object
    sbom_result.spec_version_result.merge(_check_spec_version(sbom_data))

    check_sbom_fields = functools.partial(
        _check_fields,
        fail_log_level=NTIA_FAIL_LOG_LEVEL,
        fail_result=NTIA_FAIL_RESULT,
        indent_level=1,
    )

    sbom_result.ntia_fields_result.merge(check_sbom_fields(sbom_data, "metadata"))
    sbom_result.ntia_fields_result.merge(check_sbom_fields(sbom_data.get("metadata"), "authors", "tools"))
    sbom_result.ntia_fields_result.merge(check_sbom_fields(sbom_data.get("metadata"), "timestamp"))
    sbom_result.result.merge(sbom_result.ntia_fields_result)

    logger.info("Validating SBOM licenses", indent_level=1)

    # Parse SBOM data and run all validation checks
    sbom_ = Sbom.load(sbom_data)
    sbom_result.license_results = _validate_licenses(sbom_.metadata)

    # Merge license results into final result for this SBOM
    for license_result in sbom_result.license_results:
        sbom_result.result.merge(license_result.required_fields)
        sbom_result.result.merge(license_result.expiration)

    # Skip validation for components with type of `operating-system`
    for component in [comp for comp in sbom_.components if str(comp.type) != "operating-system"]:
        component_result = _validate_component(component)
        sbom_result.component_results.append(component_result)

        # Merge component NTIA fields result into final result for this SBOM
        sbom_result.ntia_fields_result.merge(component_result.ntia_fields_result)

        # Merge component result into final result for this SBOM
        sbom_result.result.merge(component_result.result)

    return sbom_result


def _create_sbom_data_map(manifest_file: Path, sbom_files: list[Path], sbom_urls: list[str]) -> dict[str, DictStrAny]:
    """Create mapping of SBOM file paths to file contents.

    Args:
        manifest_file: Path to manifest file
        sbom_files: A list of paths for sbom files
        sbom_urls: A list of paths for sbom URLs

    Returns:
        Mapping of SBOM file paths to file contents
    """
    if manifest_file:
        # Get all SBOMs that were included in the manifest file
        sbom_files.extend(file.local for file in Sbom.loaded_sboms if isinstance(file, LocalFile))
        sbom_urls.extend(file.url for file in Sbom.loaded_sboms if isinstance(file, UrlFile))

    sbom_data_map: dict[str, dict[str, Any]] = {}

    for sbom_file in sbom_files:
        sbom_dict = hoppr.utils.load_file(sbom_file)
        if not isinstance(sbom_dict, dict):
            raise TypeError("SBOM file was not loaded as dictionary")

        sbom_data_map[str(sbom_file)] = sbom_dict
        layout.add_job(description=sbom_file.name)

    for sbom_url in sbom_urls:
        sbom_dict = hoppr.net.load_url(sbom_url)
        if not isinstance(sbom_dict, dict):
            raise TypeError("SBOM URL was not loaded as dictionary")

        sbom_data_map[sbom_url] = sbom_dict
        layout.add_job(description=Path(sbom_url).name)

    return sbom_data_map


@app.command(no_args_is_help=True)
def sbom(
    manifest_file: Path = manifest_file_option,
    sbom_files: list[Path] = sbom_files_option,
    sbom_dirs: list[Path] = sbom_dirs_option,
    sbom_urls: list[str] = sbom_urls_option,
    strict: bool = Option(
        False,
        "-S",
        "--strict",
        callback=_set_all_strict,
        help="Enable all strict validation options",
        show_default=False,
    ),
    strict_ntia_minimum_fields: bool = Option(
        False,
        "-n",
        "--strict-ntia-minimum-fields",
        help="Raise error if minimum fields recommended by NTIA are not set",
        is_eager=True,
        show_default=False,
    ),
    strict_license_fields: bool = Option(
        False,
        "-L",
        "--strict-license-fields",
        help="Raise error if SBOM license or SBOM/component license expiration fields are not set",
        is_eager=True,
        show_default=False,
    ),
    profile: str = Option(
        None,
        "-p",
        "--profile",
        callback=_profile_callback,
        help="Profile of configuration presets to apply [bold](supersedes [cyan]--strict*[/] flags)[/]",
        metavar=f"[{'|'.join(_available_profiles())}]",
        rich_help_panel="Experimental",
        show_default=False,
    ),
    config_file: Path = Option(
        None,
        "-c",
        "--config",
        callback=_config_file_callback,
        dir_okay=False,
        envvar="HOPPR_CONFIG",
        exists=True,
        help="Path to a validation config file",
        rich_help_panel="Experimental",
        show_default=False,
    ),
    expiration_days: float = Option(
        30,
        "-e",
        "--expiration-days",
        callback=_expiration_days_callback,
        help="Number of days allowed by license expiration check",
        show_default=False,
    ),
    output_format: ValidateOutputFormat = Option(
        ValidateOutputFormat.JSON,
        "-f",
        "--output-format",
        help=r"Format for output file [dim]\[default: json]",
        show_default=False,
    ),
    output_file: Path = Option(
        None,
        "-o",
        "--output-file",
        dir_okay=False,
        exists=False,
        help="Path to output file",
        resolve_path=True,
        show_default=False,
    ),
    basic_term: bool = basic_term_option,
    log_file: Path = log_file_option,
    verbose: bool = verbose_option,
    experimental: bool = experimental_option,
):  # pragma: no cover
    """Validate SBOM file(s)."""
    if experimental:
        from hoppr.cli.experimental.validate import _validate_experimental

        _validate_experimental(manifest_file, sbom_files, sbom_urls, output_file, log_file, verbose)

    _init_globals(
        log_file,
        verbose,
        expiration_days,
        strict,
        strict_license_fields,
        strict_ntia_minimum_fields,
    )

    live_display = Live(layout, console=console, refresh_per_second=10)

    summary_panel = HopprValidateSummary(log_file=log_file)

    result = ValidateCheckResult.success()

    sbom_results: list[ValidateSbomResult] = []
    sbom_data_map = _create_sbom_data_map(manifest_file, sbom_files, sbom_urls)

    if not hoppr.utils.is_basic_terminal():
        live_display.start(refresh=True)

    for name, sbom_data in sbom_data_map.items():
        msg = f"Validating {name}..."
        logger.info(msg)
        layout.print(msg)

        sbom_result = _validate_sbom(name, sbom_data)
        summary_panel.results.append(sbom_result)
        result.merge(sbom_result.result)
        sbom_results.append(sbom_result)

        layout.update_job(name=Path(name).name, status=result.status.name)
        layout.stop_job(Path(name).name)
        layout.advance_job(Path(name).name)

    if not hoppr.utils.is_basic_terminal():
        live_display.stop()

    console.print("\n", summary_panel)

    if output_file:
        # Can be extended in the future to write other types of reports
        output_data = json.loads(f"[{', '.join([sbom_result.json() for sbom_result in sbom_results])}]")
        output_file.write_text(data=json.dumps(output_data, indent=2), encoding="utf-8")

    sys.exit(1 if result.is_fail() else 0)


@app.command(no_args_is_help=True)
def config(
    input_files: list[Path] = Argument(
        ...,
        dir_okay=False,
        exists=True,
        help="Path to manifest file",
        resolve_path=True,
        show_default=False,
    ),
    credentials_file: Path = Option(
        None,
        "-c",
        "--credentials",
        help="Specify credentials config for services",
        envvar="HOPPR_CREDS_CONFIG",
        show_default=False,
    ),
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        help="Specify transfer config",
        envvar="HOPPR_TRANSFER_CONFIG",
    ),
):  # pragma: no cover
    """Validate Hoppr manifest, transfer, and credentials file(s)."""
    hoppr.main.validate(input_files, credentials_file, transfer_file)
