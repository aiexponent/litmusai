"""litmus export — export a screening report to different formats (FR-5, US-05)."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from litmusai.cli.main import app


@app.command(name="export")
def export_cmd(
    report_path: Path = typer.Argument(..., help="Path to a LitmusAI JSON report."),
    output: Path = typer.Option(..., "--output", "-o", help="Output file path."),
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format: json, markdown, sarif.",
    ),
) -> None:
    """Export a screening report to JSON, Markdown, or SARIF."""
    try:
        report_data = json.loads(report_path.read_text())
    except Exception as exc:
        typer.echo(f"Error reading report: {exc}", err=True)
        raise typer.Exit(code=2) from exc

    fmt_clean = fmt.strip().lower()
    if fmt_clean == "json":
        output.write_text(json.dumps(report_data, indent=2) + "\n")
    elif fmt_clean == "markdown":
        from litmusai.export.markdown_exporter import to_markdown

        output.write_text(to_markdown(report_data))
    elif fmt_clean == "sarif":
        from litmusai.export.sarif_exporter import to_sarif

        output.write_text(json.dumps(to_sarif(report_data), indent=2) + "\n")
    elif fmt_clean == "pdf":
        typer.echo(
            "PDF export is not supported. Supported formats: json, markdown, sarif.",
            err=True,
        )
        raise typer.Exit(code=2)
    else:
        typer.echo(
            f"Unknown format: '{fmt}'. Supported formats: json, markdown, sarif.",
            err=True,
        )
        raise typer.Exit(code=2)

    typer.echo(f"Exported to {output} ({fmt_clean})")
