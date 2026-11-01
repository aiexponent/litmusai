"""litmus verify: check report integrity against input (FR-8, US-07, AC-5)."""

from __future__ import annotations

import json
from pathlib import Path

import typer
import yaml
from pydantic import ValidationError

from litmusai.cli.main import app
from litmusai.engine.hashing import sha256_hash
from litmusai.models.system import SystemDescription


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

    if system_path:
        # Hash the validated declaration, exactly as `litmus screen` does, so a
        # file that leaves optional fields at their defaults verifies. Hashing
        # the raw YAML made every file without the generative_media block read
        # as tampered from 1.1.0 (fixed in 1.1.1).
        try:
            raw = yaml.safe_load(system_path.read_text())
            system = SystemDescription.model_validate(raw)
        except (yaml.YAMLError, OSError, ValidationError) as exc:
            typer.echo(f"Error reading {system_path}: {exc}", err=True)
            raise typer.Exit(code=2) from exc
        computed_hash = sha256_hash(system.model_dump())
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
