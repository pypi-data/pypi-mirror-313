"""Entrypoint if executed as a module (`python -m hoppr`)."""

from __future__ import annotations

from hoppr.cli import app

app(prog_name="hopctl")  # pragma: no cover
