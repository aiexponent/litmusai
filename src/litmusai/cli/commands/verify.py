"""litmus verify: check report integrity against input (FR-8, US-07, AC-5)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer
import yaml

from litmusai.cli.main import app
from litmusai.engine.hashing import sha256_hash
from litmusai.models.system import GenerativeMedia, SystemDescription

# Declaration fields that did not exist in report version 1.0 (litmus-screener
# 1.0.x). A 1.0 report hashed a system without them, so verifying such a
# report against its source file must hash the same shape.
_ADDED_IN_1_1: tuple[tuple[str, ...], ...] = (
    ("generative_media",),
    ("inputs", "social_behaviour_data"),
    ("outputs", "detrimental_treatment_unrelated_context"),
)
_LEGACY_REPORT_VERSIONS = frozenset({"1.0"})


def _declares_1_1_fields(dump: dict[str, Any]) -> bool:
    """True when any field added in 1.1 is set away from its default."""
    if dump.get("generative_media") != GenerativeMedia().model_dump():
        return True
    return bool(
        dump.get("inputs", {}).get("social_behaviour_data")
        or dump.get("outputs", {}).get("detrimental_treatment_unrelated_context")
    )


def _hashable_view(system: SystemDescription, report_version: str) -> dict[str, Any] | None:
    """The system as the report's writer hashed it, or None when the file
    declares fields the report's version never covered."""
    dump = system.model_dump()
    if report_version not in _LEGACY_REPORT_VERSIONS:
        return dump
    if _declares_1_1_fields(dump):
        return None
    for path in _ADDED_IN_1_1:
        parent = dump
        for key in path[:-1]:
            parent = parent[key]
        parent.pop(path[-1], None)
    return dump


@app.command()
def verify(
    report_path: Path = typer.Argument(..., help="Path to a LitmusAI JSON report."),
    system_path: Path = typer.Argument(
        None, help="Path to the original system.yaml (optional; uses embedded system if omitted)."
    ),
) -> None:
    """Verify a screening report's input hash has not been tampered with."""
    try:
        report_data = json.loads(report_path.read_text())
    except Exception as exc:
        typer.echo(f"Error reading report: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    stored_hash = report_data.get("input_hash_sha256", "")
    report_version = str(report_data.get("report_version", "1.0"))

    if system_path:
        # Hash the validated declaration, exactly as `litmus screen` does, so a
        # file that leaves optional fields at their defaults verifies. Hashing
        # the raw YAML made every file without the generative_media block read
        # as tampered from 1.1.0 (fixed in 1.1.1). Any read, parse or
        # validation failure (missing file, bad bytes, a date that does not
        # exist, a schema error) exits 2: the file could not be checked.
        try:
            raw = yaml.safe_load(system_path.read_text(encoding="utf-8"))
            system = SystemDescription.model_validate(raw)
        except Exception as exc:
            typer.echo(f"Error reading {system_path}: {exc}", err=True)
            raise typer.Exit(code=2) from exc
        view = _hashable_view(system, report_version)
        if view is None:
            typer.echo("TAMPERED: input hash does not match.", err=True)
            typer.echo(
                f"  The report (version {report_version}) was written before the "
                f"generative_media block and the Article 5(1)(c) fields existed, and "
                f"{system_path} now declares them. Screen the file again.",
                err=True,
            )
            raise typer.Exit(code=3)
        computed_hash = sha256_hash(view)
    else:
        system_data = report_data.get("system")
        if not system_data:
            typer.echo("No system data in report and no system_path provided.", err=True)
            raise typer.Exit(code=2)
        computed_hash = sha256_hash(system_data)

    if computed_hash == stored_hash:
        typer.echo("VERIFIED: input hash matches.")
        raise typer.Exit(code=0)
    typer.echo("TAMPERED: input hash does not match.", err=True)
    typer.echo(f"  Stored:   {stored_hash}", err=True)
    typer.echo(f"  Computed: {computed_hash}", err=True)
    raise typer.Exit(code=3)
