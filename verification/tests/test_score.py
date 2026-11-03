"""Self-tests for the verification scorer and harness helpers.

Standard library only: python3 -m unittest discover -s verification/tests
The rows here are synthetic and say nothing about LitmusAI's real results.
"""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import harness
import score


def results_for(
    case_id: str,
    target: str,
    verdict: str,
    others: dict[str, str] | None = None,
    track: str = "yaml",
):
    others = others or {}
    rows = []
    for point in score.POINTS:
        v = verdict if point == target else others.get(point, "clear")
        rows.append(
            {"case_id": case_id, "track": track, "point": point, "verdict": v, "confidence": "high"}
        )
    return rows


EXPECTED = [
    {"case_id": "t-miss", "target_point": "5.1.f", "expected": "red", "source_ref": "synthetic"},
    {"case_id": "t-flag", "target_point": "5.1.f", "expected": "red", "source_ref": "synthetic"},
    {"case_id": "t-hit", "target_point": "5.1.c", "expected": "red", "source_ref": "synthetic"},
    {"case_id": "t-alarm", "target_point": "5.1.c", "expected": "clear", "source_ref": "synthetic"},
    {
        "case_id": "t-caution",
        "target_point": "5.1.ba",
        "expected": "clear",
        "source_ref": "synthetic",
    },
    {"case_id": "t-ok", "target_point": "5.1.ba", "expected": "clear", "source_ref": "synthetic"},
]
RESULTS = (
    results_for("t-miss", "5.1.f", "clear")
    + results_for("t-flag", "5.1.f", "amber")
    + results_for("t-hit", "5.1.c", "red", {"5.1.g": "red"})
    + results_for("t-alarm", "5.1.c", "red")
    + results_for("t-caution", "5.1.ba", "amber")
    + results_for("t-ok", "5.1.ba", "clear")
)


class ScoreTests(unittest.TestCase):
    def test_five_lines(self):
        lines = score.score(EXPECTED, RESULTS)["tracks"]["yaml"]["lines"]
        self.assertEqual(lines["missed"], ["t-miss"])
        self.assertEqual(lines["flagged"], ["t-flag"])
        self.assertEqual(lines["false_alarm"], ["t-alarm"])
        self.assertEqual(lines["over_caution"], ["t-caution"])
        self.assertEqual(lines["off_target_red"], ["t-hit 5.1.g"])

    def test_table_counts(self):
        table = score.score(EXPECTED, RESULTS)["tracks"]["yaml"]["table"]
        self.assertEqual(table["5.1.f"]["red"], {"red": 0, "amber": 1, "clear": 1, "missing": 0})
        self.assertEqual(table["5.1.c"]["red"]["red"], 1)
        self.assertEqual(table["5.1.ba"]["clear"], {"red": 0, "amber": 1, "clear": 1, "missing": 0})

    def test_missing_result_is_counted_not_hidden(self):
        card = score.score(EXPECTED[:1], [])
        self.assertEqual(card["tracks"], {})
        card = score.score(EXPECTED, RESULTS[:10])
        self.assertEqual(card["tracks"]["yaml"]["table"]["5.1.f"]["red"]["missing"], 1)

    def test_tracks_are_scored_apart(self):
        quick = results_for("t-miss", "5.1.f", "red", track="describe")
        card = score.score(EXPECTED, RESULTS + quick)
        self.assertEqual(card["tracks"]["yaml"]["lines"]["missed"], ["t-miss"])
        self.assertEqual(card["tracks"]["describe"]["lines"]["missed"], [])

    def test_drift(self):
        changed = [dict(r) for r in RESULTS]
        changed[0]["verdict"] = "red"
        self.assertEqual(score.drift(RESULTS, RESULTS), [])
        self.assertEqual(len(score.drift(RESULTS, changed)), 1)
        self.assertEqual(len(score.drift(RESULTS, RESULTS[1:])), 1)

    def test_confidence_change_is_not_drift(self):
        changed = [dict(r) for r in RESULTS]
        changed[0]["confidence"] = "low"
        self.assertEqual(score.drift(RESULTS, changed), [])
        self.assertEqual(score.confidence_changes(RESULTS, changed), 1)

    def test_a_verdict_change_is_not_counted_as_a_confidence_change(self):
        changed = [dict(r) for r in RESULTS]
        changed[0]["confidence"] = "low"
        changed[0]["verdict"] = "red"
        self.assertEqual(len(score.drift(RESULTS, changed)), 1)
        self.assertEqual(score.confidence_changes(RESULTS, changed), 0)

    def test_a_short_committed_row_missing_from_the_run_is_drift(self):
        short = [{"case_id": "t-x", "track": "yaml", "point": "5.1.a", "confidence": "high"}]
        self.assertEqual(len(score.drift(short, [])), 1)

    def test_markdown_has_every_line(self):
        text = score.render_markdown(score.score(EXPECTED, RESULTS))
        for _, title in score.LINE_TITLES:
            self.assertIn(title, text)


class ExpectedFileTests(unittest.TestCase):
    def write(self, rows, header=score.EXPECTED_COLUMNS):
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        tmp = Path(tmpdir.name) / "expected.csv"
        with tmp.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            w.writerows(rows)
        return tmp

    def test_valid(self):
        path = self.write([("c1", "5.1.bb", "red", "Reg. 2026/1744 recital 13")])
        self.assertEqual(len(score.load_expected(path)), 1)

    def test_case_id_is_stripped_and_quoted_commas_are_kept(self):
        path = self.write([(" c1 ", "5.1.a", "red", "Guidelines p. 12, para 3")])
        row = score.load_expected(path)[0]
        self.assertEqual(row["case_id"], "c1")
        self.assertEqual(row["source_ref"], "Guidelines p. 12, para 3")

    def test_rejects_bad_label_point_duplicate_and_header(self):
        bad = [
            [("c1", "5.1.z", "red", "x")],
            [("c1", "5.1.a", "maybe", "x")],
            [("c1", "5.1.a", "red", "x"), ("c1", "5.1.b", "red", "x")],
            [("c1", "5.1.a", "red", "")],
            [("_c1", "5.1.a", "red", "x")],
            [("c1", "5.1.a", "red", "Guidelines p. 12", " para 3")],
            [("c1", "5.1.a", "red")],
        ]
        for rows in bad:
            with self.assertRaises(score.InputError):
                score.load_expected(self.write(rows))
        with self.assertRaises(score.InputError):
            score.load_expected(
                self.write([("c1", "5.1.a", "red")], header=("case_id", "target_point", "expected"))
            )


class HarnessHelperTests(unittest.TestCase):
    def test_description(self):
        tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(tmpdir.cleanup)
        tmp = Path(tmpdir.name) / "c1.md"
        tmp.write_text(
            "# c1\n\n## Description\n\nA system that\nscores people.\n\n## Source\n\np. 1\n",
            encoding="utf-8",
        )
        self.assertEqual(harness.read_description(tmp), "A system that scores people.")
        tmp.write_text("# c1\n\n## Source\n", encoding="utf-8")
        with self.assertRaises(score.InputError):
            harness.read_description(tmp)

    def test_citation_mismatch(self):
        report = {
            "categories": {
                "5.1.f": {
                    "regulation_citations": [{"article": "Art. 5(1)(f)"}, {"article": "Recital 44"}]
                },
                "5.1.ba": {
                    "regulation_citations": [
                        {"article": "Art. 5(1)(ba)"},
                        {"article": "Art. 5(1a)"},
                    ]
                },
                "5.1.c": {"regulation_citations": [{"article": "Art. 5(1)(d)"}]},
                "5.1.g": {
                    "regulation_citations": [{"article": "Art. 5(1)(g)"}, {"article": "Recital 44"}]
                },
                "5.1.bb": {
                    "regulation_citations": [
                        {"article": "Regulation (EU) 2026/1744, recital 13"},
                        {"article": "Regulation (EU) 2026/1744, recital 40"},
                        {"article": "Regulation (EU) 2026/1744, recitals 12 and 13"},
                        {"article": "Regulation (EU) 2026/1744, recitals 12 and 40"},
                    ]
                },
            }
        }
        problems, inventory = harness.citation_problems(report)
        self.assertEqual(
            problems,
            [
                "5.1.c cites Art. 5(1)(d)",
                "5.1.g cites Recital 44, which is about another point",
                "5.1.bb cites Regulation (EU) 2026/1744, recital 40, which is about another point",
                "5.1.bb cites Regulation (EU) 2026/1744, recitals 12 and 40, which is about another point",
            ],
        )
        self.assertEqual(len(inventory), 11)

    def test_normalise_ignores_only_generated_at(self):
        a = {"generated_at": "1", "x": 1}
        self.assertEqual(harness.normalise(a), harness.normalise({"generated_at": "2", "x": 1}))
        self.assertNotEqual(harness.normalise(a), harness.normalise({"generated_at": "1", "x": 2}))


if __name__ == "__main__":
    unittest.main()
