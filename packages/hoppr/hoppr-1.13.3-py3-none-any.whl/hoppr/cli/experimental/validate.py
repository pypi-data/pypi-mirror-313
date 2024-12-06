"""`validate` subcommand for `hopctl` (experimental)."""

from __future__ import annotations

import logging
import sys
import tempfile

from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeAlias

from rich import box
from rich.console import Group
from rich.live import Live
from rich.padding import Padding
from rich.rule import Rule
from rich.table import Table

import hoppr.main
import hoppr.models.validation
import hoppr.net
import hoppr.utils

from hoppr.cli.layout import HopprBasePanel, HopprSbomFilesLayout, console
from hoppr.logger import HopprLogger
from hoppr.models.sbom import Sbom
from hoppr.models.types import LocalFile, UrlFile
from hoppr.models.validation.base import BaseValidator
from hoppr.models.validation.code_climate import IssueList, IssueSeverity
from hoppr.models.validation.validators import validate

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult
    from typing_extensions import TypedDict

    DictStrAny: TypeAlias = dict[str, Any]

    class IssuesDict(TypedDict):  # noqa: D101
        sbom: IssueList
        metadata: IssueList
        metadata_licenses: IssueList
        components: IssueList
        component_licenses: IssueList


all_issues: IssueList
layout: HopprSbomFilesLayout
logger: HopprLogger
summary_panel: HopprValidateSummary

_EXIT_CODE = 0


class HopprValidateSummary(HopprBasePanel):
    """`hopctl validate sbom` results summary."""

    summary_group = Group()

    def __init__(self, *args, title: str | None = "Summary", log_file: Path, **kwargs) -> None:
        self.log_file = log_file
        self.issues_found: dict[str, IssueList] = {}

        super().__init__(self.summary_group, title, *args, **kwargs)

    def __rich_console__(self, console_: Console, options: ConsoleOptions) -> RenderResult:
        issues_found = {sbom_file: issues for sbom_file, issues in self.issues_found.items() if issues}

        for sbom_file, issues in issues_found.items():
            issues_dict = _get_issues_dict(issues)

            self.summary_group.renderables.append(f"\n[bold]{sbom_file}\n")
            self._sbom_issues_table(issues_dict["sbom"])
            self._metadata_issues_table(issues_dict["metadata"])
            self._license_issues_table(issues_dict["metadata_licenses"])
            self._component_issues_table(issues_dict["components"])
            self._license_issues_table(issues_dict["component_licenses"])

            self.summary_group.renderables.append(Rule(style="[bold white]rule.line"))

        self.summary_group.renderables.append(f"See log file {self.log_file} for full results.")
        if hoppr.utils.is_basic_terminal():
            console_.line()
            console_.rule(title="Summary", characters="=", style="[bold]rule.line")
            console_.print(self.summary_group)
            return []

        return super().__rich_console__(console_, options)

    def _component_issues_table(self, issue_list: IssueList):
        if not issue_list:
            return

        table = Table(
            "Check",
            "Count",
            box=box.MINIMAL,
            title="Components",
            title_justify="left",
            title_style="bold",
        )
        issue_counts = defaultdict[str, int](int)

        for issue in issue_list:
            check_name = (issue.check_name or "").removeprefix("components.")
            issue_counts[check_name] += 1

        for check, count in sorted(issue_counts.items()):
            table.add_row(check, str(count))

        self.summary_group.renderables.append(Padding.indent(table, level=4))

    def _license_issues_table(self, issue_list: IssueList):
        if not issue_list:
            return

        table = Table(
            "Check",
            "Count",
            box=box.MINIMAL,
            title="Licenses",
            title_justify="left",
            title_style="bold",
        )

        issue_counts = defaultdict[str, int](int)

        for issue in issue_list:
            check_name = (issue.check_name or "").removeprefix("metadata.").removeprefix("components.")
            check_name = check_name.removeprefix("licenses.")
            issue_counts[check_name] += 1

        for check, count in sorted(issue_counts.items()):
            table.add_row(check, str(count))

        self.summary_group.renderables.append(Padding.indent(table, level=8))

    def _metadata_issues_table(self, issue_list: IssueList):
        if not issue_list:
            return

        table = Table(
            "Check",
            "Count",
            box=box.MINIMAL,
            title="Metadata",
            title_justify="left",
            title_style="bold",
        )

        for issue in issue_list:
            table.add_row((issue.check_name or "").removeprefix("metadata."), issue.description)

        self.summary_group.renderables.append(Padding.indent(table, level=4))

    def _sbom_issues_table(self, issue_list: IssueList):
        if not issue_list:
            return

        table = Table("Check", "Details", box=box.MINIMAL)

        for issue in issue_list:
            table.add_row((issue.check_name or "").removeprefix("sbom."), issue.description)

        self.summary_group.renderables.append(table)


def _init_globals(log_file: Path, verbose: bool):
    global all_issues, layout, logger, summary_panel

    all_issues = IssueList()
    logger = HopprLogger(
        name="hopctl-validate",
        filename=str(log_file),
        level=logging.DEBUG if verbose else logging.INFO,
    )

    layout = HopprSbomFilesLayout()

    summary_panel = HopprValidateSummary(log_file=log_file)


def _get_issues_dict(issues: IssueList) -> IssuesDict:
    issues_dict: IssuesDict = {
        "sbom": IssueList(),
        "metadata": IssueList(),
        "metadata_licenses": IssueList(),
        "components": IssueList(),
        "component_licenses": IssueList(),
    }

    for issue in issues:
        if not issue.check_name:
            continue

        match issue.check_name.split("."):
            case ["sbom", *_]:
                issues_dict["sbom"].append(issue)

            case ["metadata", "licenses", *_]:
                issues_dict["metadata_licenses"].append(issue)

            case ["metadata", *_]:
                issues_dict["metadata"].append(issue)

            case ["components", "licenses", *_]:
                issues_dict["component_licenses"].append(issue)

            case ["components", *_]:
                issues_dict["components"].append(issue)

    return issues_dict


def _get_result_status(issues: IssueList) -> str:
    result = "success"

    for issue in issues:
        if issue.severity == IssueSeverity.MINOR:
            result = "warn"
        elif issue.severity == IssueSeverity.MAJOR:
            global _EXIT_CODE
            _EXIT_CODE = 1

            result = "fail"
            break

    return result


def _start_live_display() -> Live:
    live_display = Live(layout, console=console, refresh_per_second=10)

    if not hoppr.utils.is_basic_terminal():
        live_display.start(refresh=True)

    return live_display


def _validate_sboms(sbom_files: list[Path], sbom_urls: list[str]):
    with tempfile.TemporaryDirectory() as tmpdir:
        for sbom_url in sbom_urls:
            temp_sbom_file = Path(tmpdir) / Path(sbom_url).name
            hoppr.net.download_file(url=sbom_url, dest=str(temp_sbom_file))
            sbom_files.append(temp_sbom_file)

        # Before loop to populate the SBOM files side panel
        for sbom_file in sbom_files:
            layout.add_job(description=sbom_file.name)

        BaseValidator.subscribe(observer=logger, callback=logger.log)

        for sbom_file in sbom_files:
            msg = f"Validating {sbom_file}..."
            logger.info(msg)
            layout.print(msg)

            file_result = "success"
            sbom_file_issues = validate(sbom_file)
            summary_panel.issues_found[str(sbom_file)] = sbom_file_issues
            all_issues.extend(sbom_file_issues)

            file_result = _get_result_status(sbom_file_issues)

            layout.update_job(name=Path(sbom_file).name, status=file_result)
            layout.stop_job(Path(sbom_file).name)
            layout.advance_job(Path(sbom_file).name)

        BaseValidator.unsubscribe(observer=logger)


def _validate_experimental(
    manifest_file: Path | None,
    sbom_files: list[Path],
    sbom_urls: list[str],
    output_file: Path | None,
    log_file: Path,
    verbose: bool,
):  # pragma: no cover
    """Validate SBOM file(s)."""
    _init_globals(log_file, verbose)

    if manifest_file:
        # Get all SBOMs that were included in the manifest file
        sbom_files.extend(file.local for file in Sbom.loaded_sboms if isinstance(file, LocalFile))
        sbom_urls.extend(file.url for file in Sbom.loaded_sboms if isinstance(file, UrlFile))

    live_display = _start_live_display()

    try:
        _validate_sboms(sbom_files, sbom_urls)
    finally:
        live_display.stop()

    console.print("\n", summary_panel)

    if output_file:
        output_file.write_text(
            data=all_issues.json(indent=2, by_alias=True, exclude_none=True, exclude_unset=True),
            encoding="utf-8",
        )

    sys.exit(_EXIT_CODE)
