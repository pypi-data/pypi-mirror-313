"""`merge` subcommand for `hopctl`."""

from __future__ import annotations

import time

from pathlib import Path
from typing import TYPE_CHECKING

from rich.console import Group
from rich.live import Live
from rich.table import Table
from typer import BadParameter, Option, Typer

import hoppr.utils

from hoppr.cli.layout import HopprBasePanel, HopprSbomFilesLayout, console
from hoppr.cli.options import (
    basic_term_option,
    log_file_option,
    manifest_file_option,
    sbom_dirs_option,
    sbom_files_option,
    sbom_urls_option,
    verbose_option,
)
from hoppr.models.base import CycloneDXBaseModel
from hoppr.models.sbom import Sbom

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Merge all properties of two or more SBOM files",
    invoke_without_command=True,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich",
    subcommand_metavar="",
)


class HopprMergeSummary(HopprBasePanel):
    """`hopctl merge` results summary."""

    def __init__(self, *args, title: str | None = "Summary", **kwargs) -> None:
        self.total_components = 0
        self.merged_components = 0

        self.summary_table = Table(
            "File Name",
            "# Components",
            "Elapsed Time",
            box=None,
            pad_edge=False,
            show_edge=False,
        )

        self.before_after_table = Table.grid(padding=(0, 1))

        self.summary_group = Group(self.summary_table, self.before_after_table)

        super().__init__(self.summary_group, title, *args, **kwargs)

    def __rich_console__(self, console_: Console, options: ConsoleOptions) -> RenderResult:
        self.before_after_table.add_row()
        self.before_after_table.add_row("Total components before merge:", str(self.total_components))
        self.before_after_table.add_row("Total components after merge:", str(self.merged_components))

        if hoppr.utils.is_basic_terminal():
            console_.line()
            console_.rule(title="Summary", characters="=", style="[bold]rule.line")
            console_.print(self.summary_table)
            console_.print(self.before_after_table)
            return []

        return super().__rich_console__(console_, options)


def output_file_callback(output_file: Path | None) -> Path:
    """Auto-generate an output file name if not provided."""
    return output_file or Path.cwd() / f"hopctl-merge-{time.strftime('%Y%m%d-%H%M%S')}.json"


def _merge_sboms() -> Sbom:
    """Merge SBOMs into single object."""
    merged_sbom = Sbom()
    layout = HopprSbomFilesLayout()
    live_display = Live(layout, console=console, refresh_per_second=10)
    merged_sbom.subscribe(observer=layout, callback=layout.print)
    summary_panel = HopprMergeSummary()

    for sbom_ref, sbom in Sbom.loaded_sboms.items():
        summary_panel.total_components += len(sbom.components)
        layout.add_job(description=Path(str(sbom_ref)).name, sbom=sbom)

    if not hoppr.utils.is_basic_terminal():
        live_display.start(refresh=True)

    for task in layout.jobs_panel.progress_bar.tasks:
        layout.print(f"Merging {task.description}...")
        layout.start_job(task.description)

        merged_sbom.merge(task.fields["sbom"])

        layout.stop_job(task.description)
        layout.advance_job(task.description)

        summary_panel.summary_table.add_row(
            task.description,
            str(len(task.fields["sbom"].components)),
            f"{task.elapsed:.3f}",
        )

    layout.print("Writing merged SBOM...")

    layout.overall_progress.progress_bar.stop_task(layout.progress_task.id)

    summary_panel.merged_components = len(merged_sbom.components)

    if not hoppr.utils.is_basic_terminal():
        live_display.stop()

    console.print("\n", summary_panel)

    merged_sbom.unsubscribe(observer=layout)
    return merged_sbom


@app.callback()
def merge(
    manifest_file: Path = manifest_file_option,
    sbom_files: list[Path] = sbom_files_option,
    sbom_dirs: list[Path] = sbom_dirs_option,
    sbom_urls: list[str] = sbom_urls_option,
    output_file: Path = Option(
        None,
        "-o",
        "--output-file",
        callback=output_file_callback,
        dir_okay=False,
        exists=False,
        help="Path to output file [dim]\\[default: hopctl-merge-YYMMDD-HHMMSS.json]",
        resolve_path=True,
        show_default=False,
    ),
    deep_merge: bool = Option(
        False,
        "--deep-merge",
        help="Resolve and expand [cyan]externalReferences[/] in-place",
        show_default=False,
    ),
    flatten: bool = Option(
        False,
        "--flatten",
        help="Flatten nested [cyan]components[/] into single unified list",
        show_default=False,
    ),
    basic_term: bool = basic_term_option,
    log_file: Path = log_file_option,
    verbose: bool = verbose_option,
):
    """Merge SBOM files."""
    if not any([manifest_file, *sbom_dirs, *sbom_files, *sbom_urls]) or len(Sbom.loaded_sboms) < 2:
        raise BadParameter(
            "A minimum of two SBOM files must be provided via the "
            "--sbom, --sbom-dir, --sbom-url, and --manifest arguments."
        )

    CycloneDXBaseModel.deep_merge = deep_merge
    CycloneDXBaseModel.flatten = flatten

    merged_sbom = _merge_sboms()

    output_file.write_text(
        data=merged_sbom.json(exclude_none=True, exclude_unset=True, by_alias=True, indent=2),
        encoding="utf-8",
    )
