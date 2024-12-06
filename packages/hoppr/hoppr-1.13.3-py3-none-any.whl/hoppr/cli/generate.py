"""`generate` subcommand for `hopctl`."""

from __future__ import annotations

import os

from pathlib import Path
from runpy import run_module

from rich.console import Console
from rich.markdown import Markdown
from typer import Option, Typer

from hoppr import main

app = Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Generate [bold cyan]in-toto[/] keys/layout or schemas for Hoppr input files",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich",
)


@app.command()
def layout(
    transfer_file: Path = Option(
        "transfer.yml",
        "-t",
        "--transfer",
        envvar="HOPPR_TRANSFER_CONFIG",
        help="Specify transfer config",
    ),
    project_owner_key_path: Path = Option(
        ...,
        "-pk",
        "--project-owner-key",
        envvar="HOPPR_PROJECT_OWNER_KEY",
        help="Path to key used to sign in-toto layout",
    ),
    functionary_key_path: Path = Option(
        ...,
        "-fk",
        "--functionary-key",
        envvar="HOPPR_FUNCTIONARY_KEY",
        help="Path to key used to sign in-toto layout",
    ),
    project_owner_key_prompt: bool = Option(
        False,
        "-p",
        "--prompt",
        rich_help_panel="Deprecated",
        envvar="HOPPR_PROJECT_OWNER_KEY_PROMPT",
        help="Prompt user for project owner key's password (use --project-owner-key-password instead)",
        show_default=False,
    ),
    project_owner_key_password: str = Option(
        None,
        "-pk-pass",
        "--project-owner-key-password",
        confirmation_prompt=True,
        envvar="HOPPR_PROJECT_OWNER_KEY_PASSWORD",
        help="Password for project owner key",
        hide_input=True,
        prompt_required=False,
        prompt="Enter project owner key password",
        show_default=False,
    ),
):  # pragma: no cover
    """Create in-toto layout based on transfer file."""
    main.generate_layout(**locals())


@app.command(hidden=True)
def schemas(
    output_dir: Path = Option(
        Path("schema"),
        "-o",
        "--output-dir",
        exists=True,
        file_okay=False,
        help="Output directory for schema files [dim]\\[default: ./schema]",
        is_eager=True,
        resolve_path=True,
        show_default=False,
    ),
):  # pragma: no cover
    """Generate JSON/YAML schemas for Hoppr manifest, credential, and transfer files."""
    os.chdir(output_dir)
    run_module(mod_name="hoppr.models", run_name="__main__")


@app.command(hidden=True)
def validate_config(
    output: Path = Option(
        Path("hoppr") / "models" / "validation" / "profiles" / "default.config.yml",
        "-o",
        "--output",
        dir_okay=False,
        help="Path to default validation config file to write",
        is_eager=True,
    ),
):  # pragma: no cover
    """Generate SBOM validation configuration file populated with default values."""
    from hoppr.models.validation.checks import ValidateConfig

    default_config = ValidateConfig().yaml()

    console = Console()
    console.print(f"Writing default SBOM validation configuration to {output}...")

    output.write_text(default_config, encoding="utf-8")

    markdown = Markdown(
        markup="\n".join([
            "```yaml",
            output.read_text(encoding="utf-8").strip("\n"),
            "```",
        ]),
        code_theme="github-dark",
    )

    console.print(markdown)
