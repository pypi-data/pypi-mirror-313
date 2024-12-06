"""`bundle` subcommand for `hopctl`."""

from __future__ import annotations

from pathlib import Path  # noqa: TC003
from typing import TYPE_CHECKING, Optional

from rich.console import Group
from rich.progress import MofNCompleteColumn, Progress
from rich.table import Column, Table
from rich.tree import Tree
from typer import Argument, BadParameter, CallbackParam, Context, Option, Typer, prompt

import hoppr.utils

from hoppr import main, processor
from hoppr.cli.layout import (
    HopprBasePanel,
    HopprJobsPanel,
    HopprLayout,
    HopprSpinnerColumn,
)
from hoppr.cli.options import (
    basic_term_option,
    experimental_option,
    log_file_option,
    strict_repos_option,
    verbose_option,
)

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult


app = Typer(
    context_settings={
        "allow_interspersed_args": True,
        "help_option_names": ["-h", "--help"],
    },
    help="Run the stages specified in the transfer config file on the content specified in the manifest",
    invoke_without_command=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
    subcommand_metavar="",
)


class HopprBundleJobsPanel(HopprJobsPanel):
    """Customized Rich Progress bar Panel."""

    progress_bar = Progress(
        "{task.description}",
        MofNCompleteColumn(),
        HopprSpinnerColumn(),
        expand=True,
    )

    def __init__(self) -> None:
        super().__init__()
        self.renderable = self.progress_bar
        self.title = "[bold blue]Components"


class HopprBundleLayout(HopprLayout):
    """Layout of the `hopctl bundle` console application."""

    name: str = "root"
    jobs_panel = HopprBundleJobsPanel()


class HopprBundleSummary(HopprBasePanel):
    """`hopctl bundle` results summary."""

    def __init__(self, *args, title: str | None = "Summary", **kwargs) -> None:
        self.stage_results_map: dict[str, Table] = {}
        self.summary_group = Group()
        self.failure_table = Table(
            "Plugin",
            Column("Component", overflow="fold"),
            Column("Details", overflow="fold"),
            box=None,
            pad_edge=False,
            show_edge=False,
            expand=True,
        )

        self.total_success_count = 0
        self.total_failure_count = 0

        super().__init__(self.summary_group, title, *args, **kwargs)

    def add_failure(self, plugin_name: str, comp_str: str | None, message: str) -> None:
        """Add an entry to the failures table.

        Args:
            plugin_name (str): Name of the plugin that failed
            comp_str (str | None): Name of the failed component
            message (str): Result message
        """
        self.failure_table.add_row(plugin_name, comp_str or "", message)
        self.total_failure_count += 1
        self.total_success_count -= 1

    def add_method_result(self, stage_name: str, method_name: str, result_count: int, failure_count: int) -> None:
        """Add an entry to the results table for a plugin method.

        Args:
            stage_name (str): Name of the stage
            method_name (str): Name of the method
            result_count (int): Total number of results
            failure_count (int): Number of failed results
        """
        results_table = self.stage_results_map[stage_name]
        results_table.add_row(method_name, str(result_count - failure_count), str(failure_count))

    def add_stage_result(self, stage_name: str) -> Tree:
        """Add a results table for the specified stage to the panel.

        Args:
            stage_name (str): Name of the stage

        Returns:
            Tree: Object containing nested results table
        """
        self.stage_results_map[stage_name] = Table(
            "Step",
            "# Success",
            "# Fail",
            box=None,
            pad_edge=False,
            show_edge=False,
        )

        stage_summary = Tree(label=f"Stage: {stage_name}", guide_style="conceal")
        stage_summary.add(self.stage_results_map[stage_name])

        return stage_summary

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        if self.total_failure_count > 0:
            self.summary_group.renderables.append(self.failure_table)
            self.failure_table.add_row()

        self.summary_group.renderables.append(
            f"GRAND TOTAL: {self.total_success_count} jobs succeeded, {self.total_failure_count} failed"
        )

        if hoppr.utils.is_basic_terminal():
            console.line()
            console.rule(title="Summary", characters="=", style="[bold]rule.line")

            for renderable in self.summary_group.renderables:
                console.print(renderable)

            return []

        return super().__rich_console__(console, options)


def _verify_functionary_key_callback(ctx: Context, param: CallbackParam, value: bool) -> bool:
    """Validate input parameters when `--attest` or `--sign` is specified."""
    if not value:
        return value

    if not (functionary_key_path := ctx.params.get("functionary_key_path")):
        raise BadParameter(f"A functionary private key must be provided when using the --{param.name} option.")

    if ctx.params.get("functionary_key_prompt") and not ctx.params.get("functionary_key_password"):
        ctx.params["functionary_key_password"] = prompt(
            f"Enter password for {functionary_key_path}",
            hide_input=True,
        )

    return value


def _manifest_callback(ctx: Context, manifest_file: Path) -> Path:  # pragma: no cover
    """Add `manifest_file` value to shared Click context. Allows interspersed CLI options/arguments."""
    ctx.params["manifest_file"] = manifest_file

    return manifest_file


@app.callback()
def bundle(
    manifest_file: Path = Argument(
        ...,
        callback=_manifest_callback,
        dir_okay=False,
        exists=True,
        help="Path to manifest file",
        resolve_path=True,
        show_default=False,
    ),
    attest: bool = Option(
        False,
        "-a",
        "--attest",
        callback=_verify_functionary_key_callback,
        envvar="HOPPR_ATTESTATION",
        help="Generate in-toto attestations",
        show_default=False,
    ),
    sign: bool = Option(
        False,
        "-s",
        "--sign",
        callback=_verify_functionary_key_callback,
        envvar="HOPPR_SIGNING",
        help="Generate signature for the bundle and delivered sbom",
        show_default=False,
    ),
    credentials_file: Optional[Path] = Option(
        None,
        "-c",
        "--credentials",
        help="Specify credentials config for services",
        envvar="HOPPR_CREDS_CONFIG",
        show_default=False,
    ),
    functionary_key_path: Optional[Path] = Option(
        None,
        "-fk",
        "--functionary-key",
        envvar="HOPPR_FUNCTIONARY_KEY",
        help="Path to key used to sign in-toto layout or bundle / sbom",
        is_eager=True,
        show_default=False,
    ),
    functionary_key_password: Optional[str] = Option(
        None,
        "-fk-pass",
        "--functionary-key-password",
        confirmation_prompt=True,
        envvar="HOPPR_FUNCTIONARY_KEY_PASSWORD",
        help="Password for functionary key",
        hide_input=True,
        is_eager=True,
        prompt_required=False,
        prompt="Enter functionary key password",
        show_default=False,
    ),
    ignore_errors: bool = Option(
        False,
        "-i",
        "--ignore-errors",
        envvar="HOPPR_IGNORE_ERRORS",
        help="Generate a bundle even if some components fail to be collected",
        is_eager=True,
        show_default=True,
    ),
    functionary_key_prompt: bool = Option(
        False,
        "-p",
        "--prompt",
        rich_help_panel="Deprecated",
        envvar="HOPPR_FUNCTIONARY_KEY_PROMPT",
        help="Prompt user for functionary key's password (use --functionary-key-password instead)",
        is_eager=True,
        show_default=False,
    ),
    previous_delivery: Optional[Path] = Option(
        None,
        "-pd",
        "--previous-delivery",
        help="Path to manifest or tar bundle representing a previous delivery",
        envvar="HOPPR_PREVIOUS_DELIVERY",
        show_default=False,
    ),
    delivered_sbom: Optional[Path] = Option(
        None,
        "-S",
        "--delivered-sbom-output",
        dir_okay=False,
        envvar="HOPPR_DELIVERED_SBOM",
        help="File to which delivered SBOM will be written if specified",
        show_default=False,
    ),
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        help="Specify transfer config",
        envvar="HOPPR_TRANSFER_CONFIG",
        show_default=False,
    ),
    basic_term: bool = basic_term_option,
    experimental: bool = experimental_option,
    strict_repos: bool = strict_repos_option,
    verbose: bool = verbose_option,
    log_file: Path = log_file_option,
):  # pragma: no cover
    """Run the stages specified in the transfer config file on the content specified in the manifest."""
    processor.layout = HopprBundleLayout()
    processor.summary_panel = HopprBundleSummary()

    main.bundle(**locals())
