"""Top-level CLI application."""

from __future__ import annotations

import ctypes
import sys

from pathlib import Path
from platform import python_version

import rich

from rich.ansi import AnsiDecoder
from typer import Typer

import hoppr.utils

from hoppr.cli import bundle, generate, merge, validate

# Windows flags and types
NT_ENABLE_ECHO_INPUT = 0b0100
NT_ENABLE_LINE_INPUT = 0b0010
NT_ENABLE_PROCESSED_INPUT = 0b0001
NT_CONSOLE_FLAGS = NT_ENABLE_ECHO_INPUT | NT_ENABLE_LINE_INPUT | NT_ENABLE_PROCESSED_INPUT
NT_STD_OUTPUT_HANDLE = ctypes.c_uint(-11)

# Enable ANSI processing on Windows systems
if sys.platform == "win32":  # pragma: no cover
    nt_kernel = ctypes.WinDLL(name="kernel32.dll")

    nt_kernel.SetConsoleMode(nt_kernel.GetStdHandle(NT_STD_OUTPUT_HANDLE), NT_CONSOLE_FLAGS)


app = Typer(
    name="hopctl",
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Collect, process, & bundle your software supply chain",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich",
)

app.add_typer(typer_instance=bundle.app, name="bundle")
app.add_typer(typer_instance=generate.app, name="generate")
app.add_typer(typer_instance=merge.app, name="merge")
app.add_typer(typer_instance=validate.app, name="validate")


# Aliases for deprecated commands to preserve backward compatibility
generate_layout = app.command(
    name="generate-layout",
    deprecated=True,
    rich_help_panel="Deprecated",
    help="See [bold cyan]hopctl generate layout[/] subcommand",
)(generate.layout)


generate_schemas = app.command(
    name="generate-schemas",
    deprecated=True,
    rich_help_panel="Deprecated",
    help="See [bold cyan]hopctl generate schemas[/] subcommand",
)(generate.schemas)


@app.command()
def version():
    """Print version information for [bold cyan]hoppr[/]."""
    # Non-TTY terminals and MacOS Terminal.app don't support ANSI multibyte characters. Print low-resolution art instead
    suffix = ".ascii" if hoppr.utils.is_basic_terminal() else ".ansi"
    hippo_file = (Path(hoppr.__file__).parent / "resources" / "hoppr-hippo").with_suffix(suffix)

    decoder = AnsiDecoder()
    hippo = decoder.decode(hippo_file.read_text(encoding="utf-8"))

    rich.print(*hippo, sep="\n")
    rich.print(f"[green]Hoppr Framework Version[/] : {hoppr.__version__}")
    rich.print(f"[green]Python Version         [/] : {python_version()}")


__all__ = ["app"]
