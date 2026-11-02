"""Run LitmusAI on every verification case and collect the verdicts.

Runs inside the environment that ``run.sh`` builds, where ``litmus`` and
``jsonschema`` come from ``requirements.lock``. For each case listed in
``expected.csv`` it:

1. screens ``declarations/<case_id>.yaml`` twice and checks the two reports
   are identical apart from ``generated_at`` (repeatability);
2. exports the report to SARIF and validates it against the OASIS SARIF 2.1.0
   schema, fetched once and checked against a pinned SHA-256;
3. checks that every ``Art. 5(1)(x)`` citation names the point it sits under,
   and lists every citation in ``citations.csv`` for a reader to check by hand;
4. screens the case's "Description" paragraph with ``litmus screen --describe``
   (the quick-screen track, scored apart).

Writes ``results.csv``, ``citations.csv`` and ``errors.txt`` under ``--out``.
Exit codes: 0 all checks passed, 2 a check failed or a file is missing.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score

SARIF_SCHEMA_URL = (
    "https://docs.oasis-open.org/sarif/sarif/v2.1.0/errata01/os/schemas/sarif-schema-2.1.0.json"
)
SARIF_SCHEMA_SHA256 = "c3b4bb2d6093897483348925aaa73af03b3e3f4bd4ca38cef26dcb4212a2682e"
ARTICLE_POINT = re.compile(r"Art\.\s*5\(1\)\(([a-z]+)\)")


def read_description(case_file: Path) -> str:
    """The paragraph(s) under '## Description' in a case file."""
    lines = case_file.read_text(encoding="utf-8").splitlines()
    body: list[str] = []
    inside = False
    for line in lines:
        if line.strip().lower() == "## description":
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside:
            body.append(line)
    text = " ".join(" ".join(body).split())
    if not text:
        raise score.InputError(f"{case_file}: no '## Description' section")
    return text


def normalise(report: dict) -> dict:
    """The report without the one field that may change between runs."""
    return {k: v for k, v in report.items() if k != "generated_at"}


def citation_problems(report: dict) -> tuple[list[str], list[tuple[str, str]]]:
    """Citations naming a different Article 5(1) point, and the full inventory."""
    problems: list[str] = []
    inventory: list[tuple[str, str]] = []
    for point, result in report["categories"].items():
        letter = point.rsplit(".", 1)[-1]
        for citation in result.get("regulation_citations", []):
            article = citation.get("article") or ""
            inventory.append((point, article))
            match = ARTICLE_POINT.search(article)
            if match and match.group(1) != letter:
                problems.append(f"{point} cites {article}")
    return problems, inventory


def load_sarif_validator(cache: Path):
    """A jsonschema validator for SARIF 2.1.0, from a hash-checked download."""
    import jsonschema  # installed from requirements.lock

    data = cache.read_bytes() if cache.exists() else b""
    if hashlib.sha256(data).hexdigest() != SARIF_SCHEMA_SHA256:
        # No cache, or a cache that fails the check: download afresh.
        with urllib.request.urlopen(SARIF_SCHEMA_URL, timeout=60) as resp:
            data = resp.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != SARIF_SCHEMA_SHA256:
        raise score.InputError(
            f"SARIF schema hash {digest} does not match the pinned {SARIF_SCHEMA_SHA256}"
        )
    # Cache only bytes that passed the hash check, so a bad download is not reused.
    cache.write_bytes(data)
    # Structure only: string formats (uri, date-time) need optional packages
    # that are not in requirements.lock, so they are not checked.
    return jsonschema.Draft4Validator(json.loads(data.decode("utf-8")))


def litmus(exe: str, *args: str) -> subprocess.CompletedProcess[str]:
    # exe is the litmus command this script installed; args are file paths it built.
    return subprocess.run([exe, *args], capture_output=True, text=True, check=False)  # noqa: S603


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--verification-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--litmus", default="litmus", help="Path to the litmus command")
    args = parser.parse_args(argv)

    vdir: Path = args.verification_dir
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    try:
        version = litmus(args.litmus, "--version")
    except OSError as exc:
        print(f"Error: cannot run litmus ({exc})", file=sys.stderr)
        return 2
    if version.returncode != 0:
        print(f"Error: `litmus --version` failed: {version.stderr.strip()}", file=sys.stderr)
        return 2
    print(version.stdout.strip())

    try:
        validator = load_sarif_validator(out / "sarif-schema-2.1.0.json")
    except (OSError, score.InputError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    expected_path = vdir / "expected.csv"
    if not expected_path.exists():
        print(
            "No expected.csv yet: the install and the SARIF schema check passed; nothing to screen."
        )
        return 0
    try:
        expected = score.load_expected(expected_path)
    except (OSError, score.InputError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    rows: list[dict[str, str]] = []
    inventory: list[tuple[str, str, str]] = []
    for sub in ("yaml", "yaml-repeat", "describe", "sarif"):
        (out / "reports" / sub).mkdir(parents=True, exist_ok=True)

    for case in expected:
        cid = case["case_id"]
        decl = vdir / "declarations" / f"{cid}.yaml"
        case_file = vdir / "cases" / f"{cid}.md"
        if not decl.exists():
            errors.append(f"{cid}: missing declarations/{cid}.yaml")
            continue
        first = out / "reports" / "yaml" / f"{cid}.json"
        second = out / "reports" / "yaml-repeat" / f"{cid}.json"
        failed = False
        for target in (first, second):
            proc = litmus(
                args.litmus,
                "screen",
                str(decl),
                "--output",
                str(target),
                "--fail-on",
                "none",
                "--quiet",
            )
            if proc.returncode != 0:
                errors.append(
                    f"{cid}: screen exited {proc.returncode}: {proc.stderr.strip()[:300]}"
                )
                failed = True
                break
        if failed:
            continue
        report = json.loads(first.read_text(encoding="utf-8"))
        if normalise(report) != normalise(json.loads(second.read_text(encoding="utf-8"))):
            errors.append(f"{cid}: two screens of the same file gave different reports")

        sarif = out / "reports" / "sarif" / f"{cid}.sarif"
        proc = litmus(
            args.litmus, "export", str(first), "--format", "sarif", "--output", str(sarif)
        )
        if proc.returncode != 0:
            errors.append(f"{cid}: SARIF export exited {proc.returncode}")
        else:
            for err in validator.iter_errors(json.loads(sarif.read_text(encoding="utf-8"))):
                errors.append(
                    f"{cid}: SARIF invalid at {list(err.absolute_path)}: {err.message[:200]}"
                )

        problems, cites = citation_problems(report)
        errors += [f"{cid}: {p}" for p in problems]
        inventory += [(cid, point, article) for point, article in cites]

        for point, result in report["categories"].items():
            rows.append(
                {
                    "case_id": cid,
                    "track": "yaml",
                    "point": point,
                    "verdict": result["verdict"],
                    "confidence": result["confidence"],
                }
            )
        rows.append(
            {
                "case_id": cid,
                "track": "yaml",
                "point": "overall",
                "verdict": report["summary"]["overall_verdict"],
                "confidence": "",
            }
        )

        if case_file.exists():
            quick = out / "reports" / "describe" / f"{cid}.json"
            try:
                text = read_description(case_file)
            except score.InputError as exc:
                errors.append(str(exc))
                continue
            proc = litmus(
                args.litmus,
                "screen",
                "--describe",
                text,
                "--output",
                str(quick),
                "--fail-on",
                "none",
                "--quiet",
            )
            if proc.returncode != 0:
                errors.append(f"{cid}: quick screen exited {proc.returncode}")
                continue
            qreport = json.loads(quick.read_text(encoding="utf-8"))
            for point, result in qreport["categories"].items():
                rows.append(
                    {
                        "case_id": cid,
                        "track": "describe",
                        "point": point,
                        "verdict": result["verdict"],
                        "confidence": result["confidence"],
                    }
                )
            rows.append(
                {
                    "case_id": cid,
                    "track": "describe",
                    "point": "overall",
                    "verdict": qreport["summary"]["overall_verdict"],
                    "confidence": "",
                }
            )
        else:
            errors.append(f"{cid}: missing cases/{cid}.md")

    score.write_results(out / "results.csv", rows)
    with (out / "citations.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(("case_id", "point", "citation"))
        writer.writerows(sorted(set(inventory)))
    (out / "errors.txt").write_text("".join(f"{e}\n" for e in errors), encoding="utf-8")

    print(f"Screened {len(expected)} cases; {len(errors)} check(s) failed.")
    for e in errors:
        print(f"  {e}", file=sys.stderr)
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
