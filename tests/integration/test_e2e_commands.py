"""End-to-end integration tests for all LitmusAI CLI commands.

Spawns real subprocesses using sys.executable so tests exercise the full
import stack, Typer routing, screener engine, exporters, and exit-code
contract: exactly as a user would from a shell.

Acceptance criteria covered:
  AC-12  --help fast (see test_cli_smoke.py)
  AC-16  --describe chatbot/teenagers → amber 5.1.b  (xfail until NLP inference)
  AC-2   calculator → clear
  AC-3   social scoring → red on 5.1.c
  AC-5   verify round-trip
  AC-6   fail-on red → exit 1
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from litmusai.categories import ARTICLE_5_CATEGORIES

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_PORTFOLIO_DIR = Path(__file__).parents[1] / "fixtures" / "portfolio"

# Map fixture stem to expected overall verdict: verified against live ruleset.
_EXPECTED_VERDICTS: dict[str, str] = {
    "calculator_clear": "clear",
    "social_scoring_red": "red",
    "workplace_emotion_red": "red",
    "healthcare_emotion_amber": "amber",
    "criminal_risk_red": "red",
    "minors_chatbot_amber": "amber",
    "facial_scraping_red": "red",
    "loan_scorer_amber": "amber",
    "minors_behaviour_red": "red",
    "public_space_biometric_amber": "amber",
    # Article 5(1)(ba) and (bb), ruleset v1.1 (PRD-411)
    "undress_app_red": "red",
    "video_generator_no_csam_safeguards_red": "red",
    "image_generator_safeguarded_clear": "clear",
    "photo_retouch_1b_amber": "amber",
}


def _run(*args: str, cwd: Path | None = None, **kwargs: object) -> subprocess.CompletedProcess:  # type: ignore[type-arg]
    """Run litmusai as a subprocess and return the CompletedProcess.

    Forces PYTHONIOENCODING=utf-8 + encoding="utf-8" on the captured
    streams so Windows runners (whose default console codepage is
    cp1252) don't choke on any unicode the CLI may emit. Linux/macOS
    runners default to UTF-8 already; this is a no-op there.
    """
    import os

    cmd = [sys.executable, "-m", "litmusai", *args]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        cwd=cwd,
        env=env,
        **kwargs,  # type: ignore[arg-type]
    )


# Written by litmus-screener 1.0.1 from tests/fixtures/portfolio/calculator_clear.yaml
# on 2026-11-01, unchanged since: report_version 1.0, eight categories.
_REPORT_1_0_1 = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "reports"
    / "calculator_clear-litmus-screener-1.0.1.json"
)


def _fixture(name: str) -> Path:
    """Return absolute path to a portfolio fixture file."""
    return _PORTFOLIO_DIR / f"{name}.yaml"


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestE2ECommands:
    # ── 1. litmus init ────────────────────────────────────────────────────

    def test_init_creates_system_yaml(self, tmp_path: Path) -> None:
        """litmus init writes a system.yaml that passes screening with clear."""
        out_file = tmp_path / "system.yaml"
        result = _run("init", "--output", str(out_file))
        assert result.returncode == 0, result.stderr
        assert out_file.exists(), "system.yaml was not created"
        assert out_file.stat().st_size > 0

    def test_init_created_file_screens_clear(self, tmp_path: Path) -> None:
        """The template produced by litmus init passes screening as clear."""
        out_file = tmp_path / "system.yaml"
        _run("init", "--output", str(out_file))

        report_file = tmp_path / "report.json"
        _run("screen", str(out_file), "--output", str(report_file))
        # returncode may be 0 (clear/amber): template has all false flags
        assert report_file.exists(), "No report written"
        report = json.loads(report_file.read_text())
        assert report["summary"]["overall_verdict"] == "clear"

    def test_init_refuses_overwrite_without_force(self, tmp_path: Path) -> None:
        """litmus init exits non-zero if output exists and --force not given."""
        out_file = tmp_path / "system.yaml"
        out_file.write_text("existing content")
        result = _run("init", "--output", str(out_file))
        assert result.returncode != 0

    # ── 2. litmus screen <fixture> ────────────────────────────────────────

    def test_screen_calculator_gives_clear(self, tmp_path: Path) -> None:
        """Calculator fixture → overall_verdict: clear."""
        report_file = tmp_path / "report.json"
        result = _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        assert result.returncode == 0, result.stderr
        report = json.loads(report_file.read_text())
        assert report["summary"]["overall_verdict"] == "clear"
        assert report["summary"]["red_count"] == 0
        assert report["summary"]["amber_count"] == 0

    def test_screen_social_scoring_gives_red(self, tmp_path: Path) -> None:
        """Social scoring fixture → overall_verdict: red, triggered in 5.1.c.

        Note: the default --fail-on is "red", so the process exits 1 when the
        verdict is red.  We accept either 0 or 1 here and assert via the report.
        """
        report_file = tmp_path / "report.json"
        result = _run("screen", str(_fixture("social_scoring_red")), "--output", str(report_file))
        # default --fail-on red means returncode is 1 for a red result
        assert result.returncode in (0, 1), result.stderr
        assert report_file.exists(), "Report not written"
        report = json.loads(report_file.read_text())
        assert report["summary"]["overall_verdict"] == "red"
        assert report["categories"]["5.1.c"]["verdict"] == "red"
        assert len(report["categories"]["5.1.c"]["triggered_rules"]) > 0

    # ── 3. litmus screen --describe ───────────────────────────────────────

    def test_screen_describe_teenagers_chatbot_gives_amber(self, tmp_path: Path) -> None:
        """AC-16: --describe mental health chatbot for teenagers → amber on 5.1.b."""
        report_file = tmp_path / "report.json"
        result = _run(
            "screen",
            "--describe",
            "a chatbot for mental health support for teenagers",
            "--output",
            str(report_file),
        )
        assert result.returncode == 0, result.stderr
        assert report_file.exists()
        report = json.loads(report_file.read_text())
        assert report["summary"]["overall_verdict"] == "amber"
        assert report["categories"]["5.1.b"]["verdict"] == "amber"
        assert len(report["categories"]["5.1.b"]["triggered_rules"]) > 0

    def test_screen_describe_returns_zero_exit(self) -> None:
        """--describe always exits 0 when no --fail-on is set."""
        result = _run(
            "screen",
            "--describe",
            "a chatbot for mental health support for teenagers",
        )
        assert result.returncode == 0

    def test_screen_describe_produces_system_quick_screen(self, tmp_path: Path) -> None:
        """--describe embeds system.name == 'Quick Screen' in the report."""
        report_file = tmp_path / "report.json"
        _run(
            "screen",
            "--describe",
            "a basic recommendation engine",
            "--output",
            str(report_file),
        )
        report = json.loads(report_file.read_text())
        assert report["system"]["name"] == "Quick Screen"

    # ── 4. litmus screen <fixture> --output report.json ──────────────────

    def test_screen_output_writes_valid_json(self, tmp_path: Path) -> None:
        """--output flag writes a well-formed JSON report."""
        report_file = tmp_path / "report.json"
        result = _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        assert result.returncode == 0, result.stderr
        assert report_file.exists()
        report = json.loads(report_file.read_text())
        # Check required top-level keys from ScreeningReport schema
        for key in ("report_version", "summary", "categories", "system", "input_hash_sha256"):
            assert key in report, f"Missing key in report: {key!r}"

    def test_screen_output_report_has_all_categories(self, tmp_path: Path) -> None:
        """JSON report contains all ten Article 5 categories, in regulation order."""
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        report = json.loads(report_file.read_text())
        assert list(report["categories"].keys()) == list(ARTICLE_5_CATEGORIES)

    def test_screen_output_report_embeds_system(self, tmp_path: Path) -> None:
        """JSON report embeds the parsed SystemDescription."""
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        report = json.loads(report_file.read_text())
        assert report["system"]["name"] == "SimpleCalc"

    # ── 5. litmus verify report.json ─────────────────────────────────────

    def test_verify_exits_zero_for_intact_report(self, tmp_path: Path) -> None:
        """litmus verify exits 0 when the report hash matches the embedded system."""
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        result = _run("verify", str(report_file))
        assert result.returncode == 0, result.stderr
        assert "VERIFIED" in result.stdout

    def test_verify_exits_nonzero_for_tampered_report(self, tmp_path: Path) -> None:
        """litmus verify exits non-zero when the report has been tampered with."""
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        # Tamper: change the system name in the report
        data = json.loads(report_file.read_text())
        data["system"]["name"] = "TAMPERED"
        report_file.write_text(json.dumps(data))
        result = _run("verify", str(report_file))
        assert result.returncode != 0
        assert "TAMPERED" in result.stderr

    def test_verify_with_system_path_accepts_defaults(self, tmp_path: Path) -> None:
        """1.1.1: `litmus verify report.json system.yaml` hashes the validated
        declaration, so a file that leaves optional fields at their defaults
        (no generative_media block, empty inputs) verifies like the one-argument
        form. 1.1.0 hashed the raw YAML and reported every such file as tampered."""
        report_file = tmp_path / "report.json"
        fixture = _fixture("calculator_clear")
        _run("screen", str(fixture), "--output", str(report_file))
        result = _run("verify", str(report_file), str(fixture))
        assert result.returncode == 0, result.stderr
        assert "VERIFIED" in result.stdout

    def test_verify_with_changed_system_file_is_tampered(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.json"
        fixture = _fixture("calculator_clear")
        _run("screen", str(fixture), "--output", str(report_file))
        changed = tmp_path / "system.yaml"
        changed.write_text(fixture.read_text().replace("SimpleCalc", "OtherCalc"))
        result = _run("verify", str(report_file), str(changed))
        assert result.returncode == 3
        assert "TAMPERED" in result.stderr

    def test_verify_with_invalid_system_file_exits_two(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        bad = tmp_path / "bad.yaml"
        bad.write_text("name: only-a-name\n")
        result = _run("verify", str(report_file), str(bad))
        assert result.returncode == 2

    def test_verify_with_impossible_date_exits_two(self, tmp_path: Path) -> None:
        """PyYAML raises ValueError for a calendar date that does not exist."""
        report_file = tmp_path / "report.json"
        fixture = _fixture("calculator_clear")
        _run("screen", str(fixture), "--output", str(report_file))
        bad = tmp_path / "bad-date.yaml"
        bad.write_text(fixture.read_text() + "metadata:\n  last_reviewed: 2026-02-30\n")
        result = _run("verify", str(report_file), str(bad))
        assert result.returncode == 2
        assert "Error reading" in result.stderr

    def test_verify_with_undecodable_file_exits_two(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        bad = tmp_path / "bytes.yaml"
        bad.write_bytes(b"name: \xff\xfe\n")
        result = _run("verify", str(report_file), str(bad))
        assert result.returncode == 2

    # ── 5b. reports written by litmus-screener 1.0.x (report_version 1.0) ──

    def test_verify_1_0_report_against_its_unchanged_source(self) -> None:
        """A report generated by litmus-screener 1.0.1 (fixture) hashed a system
        without the fields added in 1.1. The two-argument form drops those fields
        for a 1.0 report, so the unchanged source file verifies."""
        result = _run("verify", str(_REPORT_1_0_1), str(_fixture("calculator_clear")))
        assert result.returncode == 0, result.stderr
        assert "VERIFIED" in result.stdout

    def test_verify_1_0_report_one_argument_form_still_works(self) -> None:
        result = _run("verify", str(_REPORT_1_0_1))
        assert result.returncode == 0, result.stderr

    def test_verify_1_0_report_against_file_declaring_1_1_fields_is_tampered(
        self, tmp_path: Path
    ) -> None:
        """A 1.0 hash cannot vouch for fields that did not exist; a file that now
        sets them must not verify against the old report."""
        changed = tmp_path / "system.yaml"
        changed.write_text(
            _fixture("calculator_clear").read_text()
            + "generative_media:\n  realistic_media_generation: true\n"
        )
        result = _run("verify", str(_REPORT_1_0_1), str(changed))
        assert result.returncode == 3
        assert "TAMPERED" in result.stderr
        assert "written before" in result.stderr

    def test_verify_1_0_report_against_changed_source_is_tampered(self, tmp_path: Path) -> None:
        changed = tmp_path / "system.yaml"
        changed.write_text(_fixture("calculator_clear").read_text().replace("SimpleCalc", "X"))
        result = _run("verify", str(_REPORT_1_0_1), str(changed))
        assert result.returncode == 3

    # ── 6. litmus export report.json --format markdown ───────────────────

    def test_export_markdown_creates_file(self, tmp_path: Path) -> None:
        """litmus export --format markdown creates a .md file."""
        report_file = tmp_path / "report.json"
        md_file = tmp_path / "report.md"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        result = _run("export", str(report_file), "--output", str(md_file), "--format", "markdown")
        assert result.returncode == 0, result.stderr
        assert md_file.exists()
        content = md_file.read_text()
        assert len(content) > 0
        # Should contain markdown heading markers
        assert "#" in content

    def test_export_markdown_contains_system_name(self, tmp_path: Path) -> None:
        """Markdown export includes the system name."""
        report_file = tmp_path / "report.json"
        md_file = tmp_path / "report.md"
        _run("screen", str(_fixture("social_scoring_red")), "--output", str(report_file))
        _run("export", str(report_file), "--output", str(md_file), "--format", "markdown")
        content = md_file.read_text()
        assert "CitizenTrustScore" in content

    # ── 7. litmus export report.json --format sarif ───────────────────────

    def test_export_sarif_creates_valid_sarif(self, tmp_path: Path) -> None:
        """litmus export --format sarif creates valid SARIF 2.1.0."""
        report_file = tmp_path / "report.json"
        sarif_file = tmp_path / "report.sarif"
        _run("screen", str(_fixture("social_scoring_red")), "--output", str(report_file))
        result = _run("export", str(report_file), "--output", str(sarif_file), "--format", "sarif")
        assert result.returncode == 0, result.stderr
        assert sarif_file.exists()
        sarif = json.loads(sarif_file.read_text())
        assert sarif.get("version") == "2.1.0"
        assert "$schema" in sarif
        assert "runs" in sarif

    def test_export_sarif_red_fixture_has_results(self, tmp_path: Path) -> None:
        """SARIF export for a RED fixture contains at least one result entry."""
        report_file = tmp_path / "report.json"
        sarif_file = tmp_path / "report.sarif"
        _run("screen", str(_fixture("social_scoring_red")), "--output", str(report_file))
        _run("export", str(report_file), "--output", str(sarif_file), "--format", "sarif")
        sarif = json.loads(sarif_file.read_text())
        results = sarif["runs"][0].get("results", [])
        assert len(results) > 0

    def test_export_json_creates_file(self, tmp_path: Path) -> None:
        """litmus export --format json creates formatted JSON file."""
        report_file = tmp_path / "report.json"
        out_file = tmp_path / "report_out.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        result = _run("export", str(report_file), "--output", str(out_file), "--format", "json")
        assert result.returncode == 0, result.stderr
        assert out_file.exists()
        data = json.loads(out_file.read_text())
        assert "categories" in data
        assert "summary" in data

    def test_export_unsupported_format_pdf(self, tmp_path: Path) -> None:
        """litmus export --format pdf prints clear error with supported formats."""
        report_file = tmp_path / "report.json"
        out_file = tmp_path / "report.pdf"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        result = _run("export", str(report_file), "--output", str(out_file), "--format", "pdf")
        assert result.returncode == 2
        assert "PDF export is not supported" in result.stderr
        assert "Supported formats: json, markdown, sarif" in result.stderr

    def test_export_unknown_format(self, tmp_path: Path) -> None:
        """litmus export with an arbitrary unknown format exits with code 2 and lists supported formats."""
        report_file = tmp_path / "report.json"
        out_file = tmp_path / "report.xyz"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        result = _run("export", str(report_file), "--output", str(out_file), "--format", "xyz")
        assert result.returncode == 2
        assert "Unknown format: 'xyz'" in result.stderr
        assert "Supported formats: json, markdown, sarif" in result.stderr

    def test_export_missing_output_option(self, tmp_path: Path) -> None:
        """litmus export without --output/-o fails with missing option error."""
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        result = _run("export", str(report_file), "--format", "sarif")
        assert result.returncode == 2
        assert "Missing option" in result.stderr

    # ── 8. litmus portfolio tests/fixtures/portfolio/ ─────────────────────

    def test_portfolio_screens_all_fixtures(self) -> None:
        """litmus portfolio finds and screens all 10 YAML fixtures without error.

        Rich truncates long file names with an ellipsis, so we assert on the
        system names (which are shorter) rather than the raw filenames.
        """
        result = _run("portfolio", str(_PORTFOLIO_DIR))
        assert result.returncode == 0, f"portfolio failed:\n{result.stderr}"
        # System names always fit within the column width: assert on those.
        expected_system_names = [
            "SimpleCalc",
            "CitizenTrustScore",
            "EmployeeSentimentTracker",
            "ClinicalMoodAssist",
            "RecidivismRiskEngine",
            "TeenTalkBot",
            "FaceVaultDB",
            "LoanRiskScorer",
            "KidsBehaviourPredictor",
            "RetailFaceAnalytics",
        ]
        for name in expected_system_names:
            assert name in result.stdout, f"Expected system name {name!r} in portfolio output"

    def test_portfolio_output_writes_json_array(self, tmp_path: Path) -> None:
        """--output flag on portfolio writes a JSON array of individual reports."""
        out_file = tmp_path / "portfolio.json"
        result = _run("portfolio", str(_PORTFOLIO_DIR), "--output", str(out_file))
        assert result.returncode == 0, result.stderr
        assert out_file.exists()
        reports = json.loads(out_file.read_text())
        assert isinstance(reports, list)
        assert len(reports) == len(_EXPECTED_VERDICTS)

    def test_portfolio_output_contains_expected_verdicts(self, tmp_path: Path) -> None:
        """Portfolio JSON output matches expected verdicts for each fixture."""
        out_file = tmp_path / "portfolio.json"
        _run("portfolio", str(_PORTFOLIO_DIR), "--output", str(out_file))
        reports = json.loads(out_file.read_text())
        # Build map: system name → verdict
        verdict_map = {r["system"]["name"]: r["summary"]["overall_verdict"] for r in reports}
        # Spot-check a selection of systems
        assert verdict_map["SimpleCalc"] == "clear"
        assert verdict_map["CitizenTrustScore"] == "red"
        assert verdict_map["EmployeeSentimentTracker"] == "red"
        assert verdict_map["ClinicalMoodAssist"] == "amber"
        assert verdict_map["RecidivismRiskEngine"] == "red"
        assert verdict_map["LoanRiskScorer"] == "amber"
        assert verdict_map["UndressSnap"] == "red"
        assert verdict_map["OpenVid Weights"] == "red"
        assert verdict_map["Headshot Studio"] == "clear"
        assert verdict_map["RetouchPro"] == "amber"

    # ── 7. litmus --help and --describe on the new categories ────────────

    def test_help_names_ten_categories(self) -> None:
        """PRD-411: the help text names the ten Article 5(1) categories."""
        result = _run("--help")
        assert result.returncode == 0
        # Rich wraps the help text to the console width (narrower on the
        # Windows runners), so compare on collapsed whitespace.
        flat = " ".join(result.stdout.split())
        assert "10 categories" in flat
        assert "(ba) and (bb)" in flat

    def test_describe_undress_app_is_red_on_ba(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.json"
        result = _run(
            "screen",
            "--describe",
            "an app that undresses photos of real people",
            "--output",
            str(report_file),
            "--fail-on",
            "none",
        )
        assert result.returncode == 0, result.stderr
        report = json.loads(report_file.read_text())
        assert report["categories"]["5.1.ba"]["verdict"] == "red"
        assert report["summary"]["overall_verdict"] == "red"

    def test_describe_never_infers_safeguards_from_free_text(self, tmp_path: Path) -> None:
        """'without consent' and 'no content filter' must not read as safeguards in place."""
        report_file = tmp_path / "report.json"
        _run(
            "screen",
            "--describe",
            "an app that undresses photos of real people without consent and no content filter",
            "--output",
            str(report_file),
            "--fail-on",
            "none",
        )
        report = json.loads(report_file.read_text())
        safeguards = report["system"]["generative_media"]["safeguards"]
        assert not any(safeguards.values()), safeguards
        assert report["categories"]["5.1.ba"]["verdict"] == "red"

    def test_describe_filtered_image_generator_is_not_red(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.json"
        result = _run(
            "screen",
            "--describe",
            "a text-to-image generator with a content filter and consent checks",
            "--output",
            str(report_file),
            "--fail-on",
            "none",
        )
        assert result.returncode == 0, result.stderr
        report = json.loads(report_file.read_text())
        assert report["summary"]["overall_verdict"] != "red"
        assert report["categories"]["5.1.bb"]["verdict"] == "amber", "safeguards not documented"

    def test_describe_credit_scoring_is_amber_not_red(self, tmp_path: Path) -> None:
        """litmusai#25: a credit score from repayment history is not social scoring."""
        report_file = tmp_path / "report.json"
        _run(
            "screen",
            "--describe",
            "a credit scoring model using repayment history and engagement patterns",
            "--output",
            str(report_file),
            "--fail-on",
            "none",
        )
        report = json.loads(report_file.read_text())
        assert report["categories"]["5.1.c"]["verdict"] == "amber"

    def test_describe_social_credit_is_red(self, tmp_path: Path) -> None:
        report_file = tmp_path / "report.json"
        _run(
            "screen",
            "--describe",
            "a social credit score of citizens from social media behaviour",
            "--output",
            str(report_file),
            "--fail-on",
            "none",
        )
        report = json.loads(report_file.read_text())
        assert report["categories"]["5.1.c"]["verdict"] == "red"

    # ── 9. litmus debug report.json ───────────────────────────────────────

    def test_debug_prints_trace(self, tmp_path: Path) -> None:
        """litmus debug prints a rule-firing trace containing category IDs."""
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("social_scoring_red")), "--output", str(report_file))
        result = _run("debug", str(report_file))
        assert result.returncode == 0, result.stderr
        # Should print each Article 5 category
        assert "5.1.c" in result.stdout
        assert "red" in result.stdout.lower() or "RED" in result.stdout

    def test_debug_prints_system_name(self, tmp_path: Path) -> None:
        """litmus debug output contains the system name from the report."""
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("criminal_risk_red")), "--output", str(report_file))
        result = _run("debug", str(report_file))
        assert result.returncode == 0
        assert "RecidivismRiskEngine" in result.stdout

    def test_debug_clear_fixture_shows_no_triggered_rules(self, tmp_path: Path) -> None:
        """litmus debug on a clear fixture does not print any triggered rule IDs."""
        report_file = tmp_path / "report.json"
        _run("screen", str(_fixture("calculator_clear")), "--output", str(report_file))
        result = _run("debug", str(report_file))
        assert result.returncode == 0
        assert "triggered:" not in result.stdout

    # ── 10. litmus screen <red_fixture> --fail-on red → exit 1 ───────────

    def test_fail_on_red_exits_one_for_red_fixture(self) -> None:
        """--fail-on red exits with code 1 when overall verdict is red."""
        result = _run(
            "screen",
            str(_fixture("social_scoring_red")),
            "--fail-on",
            "red",
        )
        assert result.returncode == 1, (
            f"Expected exit 1 for red verdict with --fail-on red, got {result.returncode}"
        )

    def test_fail_on_red_exits_zero_for_clear_fixture(self) -> None:
        """--fail-on red exits with code 0 when overall verdict is clear."""
        result = _run(
            "screen",
            str(_fixture("calculator_clear")),
            "--fail-on",
            "red",
        )
        assert result.returncode == 0, (
            f"Expected exit 0 for clear verdict with --fail-on red, got {result.returncode}"
        )

    def test_fail_on_red_exits_zero_for_amber_fixture(self) -> None:
        """--fail-on red exits with code 0 when overall verdict is amber (not red)."""
        result = _run(
            "screen",
            str(_fixture("loan_scorer_amber")),
            "--fail-on",
            "red",
        )
        assert result.returncode == 0, (
            f"Expected exit 0 for amber verdict with --fail-on red, got {result.returncode}"
        )

    def test_fail_on_amber_exits_one_for_amber_fixture(self) -> None:
        """--fail-on amber exits with code 1 when overall verdict is amber."""
        result = _run(
            "screen",
            str(_fixture("loan_scorer_amber")),
            "--fail-on",
            "amber",
        )
        assert result.returncode == 1, (
            f"Expected exit 1 for amber verdict with --fail-on amber, got {result.returncode}"
        )

    def test_fail_on_amber_exits_one_for_red_fixture(self) -> None:
        """--fail-on amber exits with code 1 when overall verdict is red (red >= amber)."""
        result = _run(
            "screen",
            str(_fixture("criminal_risk_red")),
            "--fail-on",
            "amber",
        )
        assert result.returncode == 1

    # ── Fixture verdict coverage (parametrised) ───────────────────────────

    @pytest.mark.parametrize(
        "fixture_name,expected_verdict",
        list(_EXPECTED_VERDICTS.items()),
    )
    def test_all_fixtures_produce_expected_verdicts(
        self,
        tmp_path: Path,
        fixture_name: str,
        expected_verdict: str,
    ) -> None:
        """Each portfolio fixture produces its documented expected verdict."""
        report_file = tmp_path / "report.json"
        result = _run(
            "screen",
            str(_fixture(fixture_name)),
            "--output",
            str(report_file),
        )
        # returncode may be 1 if --fail-on red fires; screen always writes the report
        assert report_file.exists(), (
            f"Report not written for {fixture_name}. stderr: {result.stderr}"
        )
        report = json.loads(report_file.read_text())
        actual = report["summary"]["overall_verdict"]
        assert actual == expected_verdict, (
            f"{fixture_name}: expected {expected_verdict!r}, got {actual!r}"
        )
