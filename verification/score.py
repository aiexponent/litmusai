"""Score LitmusAI verdicts against the expected answers.

Standard library only. Reads ``expected.csv`` (written before any run) and
``results.csv`` (written by ``harness.py``) and produces a scorecard.

How a verdict is counted, per Article 5 point and per track:

1. Missed prohibition: expected red, got clear. The target is zero.
2. Flagged for review: expected red, got amber. Not a hit and not a miss.
3. False alarm: expected clear, got red.
4. Over-caution: expected clear, got amber. The ruleset prefers amber when
   unsure, so this is expected and reported, not hidden.
5. Off-target red: a point other than the case's target came back red.

The full 3 by 3 table (expected against actual) is printed under the lines.

Usage:
    python3 score.py score --expected expected.csv --results results.csv --out DIR
    python3 score.py drift --committed results.csv --current DIR/results.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

POINTS = (
    "5.1.a",
    "5.1.b",
    "5.1.ba",
    "5.1.bb",
    "5.1.c",
    "5.1.d",
    "5.1.e",
    "5.1.f",
    "5.1.g",
    "5.1.h",
)
LABELS = ("red", "amber", "clear")
TRACKS = ("yaml", "describe")
EXPECTED_COLUMNS = ("case_id", "target_point", "expected", "source_ref")
RESULT_COLUMNS = ("case_id", "track", "point", "verdict", "confidence")


class InputError(ValueError):
    """A file does not have the shape this script needs."""


def load_expected(path: Path) -> list[dict[str, str]]:
    """Read and check expected.csv. Raises InputError on any bad row."""
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != EXPECTED_COLUMNS:
            raise InputError(f"{path}: columns must be {','.join(EXPECTED_COLUMNS)}")
        rows = list(reader)
    seen: set[str] = set()
    for n, row in enumerate(rows, start=2):
        if None in row or any(v is None for v in row.values()):
            raise InputError(
                f"{path}:{n}: expected {len(EXPECTED_COLUMNS)} fields (quote a value that contains a comma)"
            )
        case_id = row["case_id"].strip()
        row["case_id"] = case_id
        if not case_id or case_id.startswith("_"):
            raise InputError(f"{path}:{n}: case_id is empty or starts with '_'")
        if case_id in seen:
            raise InputError(f"{path}:{n}: duplicate case_id {case_id}")
        seen.add(case_id)
        if row["target_point"] not in POINTS:
            raise InputError(
                f"{path}:{n}: target_point {row['target_point']!r} is not one of {POINTS}"
            )
        if row["expected"] not in LABELS:
            raise InputError(f"{path}:{n}: expected {row['expected']!r} is not one of {LABELS}")
        if not row["source_ref"].strip():
            raise InputError(f"{path}:{n}: source_ref is empty")
    return rows


def load_results(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != RESULT_COLUMNS:
            raise InputError(f"{path}: columns must be {','.join(RESULT_COLUMNS)}")
        return list(reader)


def write_results(path: Path, rows: list[dict[str, str]]) -> None:
    """Write results.csv in a stable order so a diff means a real change."""
    order = {p: i for i, p in enumerate((*POINTS, "overall"))}
    rows = sorted(rows, key=lambda r: (r["case_id"], TRACKS.index(r["track"]), order[r["point"]]))
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=RESULT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def score(expected: list[dict[str, str]], results: list[dict[str, str]]) -> dict:
    """Return the scorecard as plain data (see the module docstring)."""
    verdict: dict[tuple[str, str, str], str] = {
        (r["case_id"], r["track"], r["point"]): r["verdict"] for r in results
    }
    card: dict = {"tracks": {}}
    for track in TRACKS:
        if not any(k[1] == track for k in verdict):
            continue
        table = {p: {e: dict.fromkeys((*LABELS, "missing"), 0) for e in LABELS} for p in POINTS}
        lines: dict[str, list[str]] = {
            "missed": [],
            "flagged": [],
            "false_alarm": [],
            "over_caution": [],
            "off_target_red": [],
        }
        cases_per_point = dict.fromkeys(POINTS, 0)
        for row in expected:
            case_id, target, want = row["case_id"], row["target_point"], row["expected"]
            got = verdict.get((case_id, track, target), "missing")
            cases_per_point[target] += 1
            table[target][want][got] += 1
            if want == "red" and got == "clear":
                lines["missed"].append(case_id)
            elif want == "red" and got == "amber":
                lines["flagged"].append(case_id)
            elif want == "clear" and got == "red":
                lines["false_alarm"].append(case_id)
            elif want == "clear" and got == "amber":
                lines["over_caution"].append(case_id)
            for point in POINTS:
                if point != target and verdict.get((case_id, track, point)) == "red":
                    lines["off_target_red"].append(f"{case_id} {point}")
        card["tracks"][track] = {
            "cases_per_point": cases_per_point,
            "table": table,
            "lines": lines,
        }
    return card


LINE_TITLES = (
    ("missed", "Missed prohibitions (expected red, got clear)"),
    ("flagged", "Flagged for review (expected red, got amber)"),
    ("false_alarm", "False alarms (expected clear, got red)"),
    ("over_caution", "Over-caution (expected clear, got amber)"),
    ("off_target_red", "Off-target reds (a point other than the target came back red)"),
)


def render_markdown(card: dict) -> str:
    out: list[str] = ["# Scorecard", ""]
    if not card["tracks"]:
        return "# Scorecard\n\nNo results to score.\n"
    for track, data in card["tracks"].items():
        title = "Full screen of system.yaml" if track == "yaml" else "Quick screen (--describe)"
        out += [f"## {title}", ""]
        for key, label in LINE_TITLES:
            ids = data["lines"][key]
            out.append(f"- **{label}:** {len(ids)}" + (f" ({', '.join(ids)})" if ids else ""))
        out += [
            "",
            "| Point | Cases | Expected | Got red | Got amber | Got clear | Missing |",
            "|---|---|---|---|---|---|---|",
        ]
        for point in POINTS:
            n = data["cases_per_point"][point]
            for want in LABELS:
                cells = data["table"][point][want]
                if sum(cells.values()) == 0:
                    continue
                out.append(
                    f"| {point} | {n} | {want} | {cells['red']} | {cells['amber']} | {cells['clear']} | {cells['missing']} |"
                )
        out.append("")
    return "\n".join(out)


_ABSENT = "(no row)"


def _by_key(rows: list[dict[str, str]], field: str) -> dict[tuple[str, str, str], str | None]:
    return {(r["case_id"], r["track"], r["point"]): r.get(field) for r in rows}


def drift(committed: list[dict[str, str]], current: list[dict[str, str]]) -> list[str]:
    """Rows whose verdict differs between the published results and this run,
    including rows present on one side only."""
    old, new = _by_key(committed, "verdict"), _by_key(current, "verdict")
    return [
        f"{' '.join(k)}: published {old.get(k, _ABSENT)} now {new.get(k, _ABSENT)}"
        for k in sorted(old.keys() | new.keys())
        if k not in old or k not in new or old[k] != new[k]
    ]


def confidence_changes(committed: list[dict[str, str]], current: list[dict[str, str]]) -> int:
    """Rows with the same verdict but a different confidence. Reported, not a failure."""
    old_v, new_v = _by_key(committed, "verdict"), _by_key(current, "verdict")
    old_c, new_c = _by_key(committed, "confidence"), _by_key(current, "confidence")
    return sum(
        1 for k in old_c.keys() & new_c.keys() if old_v[k] == new_v[k] and old_c[k] != new_c[k]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score", help="Write scorecard.md and scorecard.json")
    s.add_argument("--expected", type=Path, required=True)
    s.add_argument("--results", type=Path, required=True)
    s.add_argument("--out", type=Path, required=True)
    d = sub.add_parser("drift", help="Compare this run with the published results.csv")
    d.add_argument("--committed", type=Path, required=True)
    d.add_argument("--current", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        if args.cmd == "score":
            card = score(load_expected(args.expected), load_results(args.results))
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "scorecard.json").write_text(
                json.dumps(card, indent=2) + "\n", encoding="utf-8"
            )
            text = render_markdown(card)
            (args.out / "scorecard.md").write_text(text, encoding="utf-8")
            print(text)
            return 0
        if not args.committed.exists():
            print("No published results.csv yet; drift check skipped.")
            return 0
        committed, current = load_results(args.committed), load_results(args.current)
        diffs = drift(committed, current)
        changed = confidence_changes(committed, current)
        if changed:
            print(f"Note: {changed} row(s) keep their verdict but report a different confidence.")
        if diffs:
            print("Verdicts differ from the published results.csv:", file=sys.stderr)
            for line in diffs:
                print(f"  {line}", file=sys.stderr)
            print("Re-publish REPORT.md and results.csv for this version.", file=sys.stderr)
            return 1
        print("Verdicts match the published results.csv.")
        return 0
    except (InputError, OSError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
