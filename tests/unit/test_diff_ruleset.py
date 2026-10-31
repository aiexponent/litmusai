"""Unit tests for the ruleset-diff engine: PRD FR-26."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest
from typer.testing import CliRunner

from litmusai.categories import ARTICLE_5_CATEGORIES, DEFAULT_RULESET_PATH, PREVIOUS_RULESET_PATH
from litmusai.cli.main import app
from litmusai.engine.diff import (
    MetadataChange,
    RuleFieldChange,
    RuleModification,
    RulesetDiff,
    diff_rulesets,
)
from litmusai.models.ruleset import Ruleset

REFERENCE_RULESET_PATH = DEFAULT_RULESET_PATH


@pytest.fixture
def reference_data() -> dict:
    return json.loads(REFERENCE_RULESET_PATH.read_text())


@pytest.fixture
def ruleset(reference_data: dict) -> Ruleset:
    return Ruleset.model_validate(reference_data)


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def _ruleset_with(reference_data: dict, **overrides: object) -> Ruleset:
    """Build a Ruleset from reference data with arbitrary top-level overrides."""
    data = deepcopy(reference_data)
    data.update(overrides)
    return Ruleset.model_validate(data)


# ---------------------------------------------------------------------------
# Engine tests: diff_rulesets
# ---------------------------------------------------------------------------


def test_identical_rulesets_have_no_changes(ruleset: Ruleset) -> None:
    diff = diff_rulesets(ruleset, ruleset)
    assert not diff.has_changes
    assert diff.added_rules == []
    assert diff.removed_rules == []
    assert diff.modified_rules == []
    assert diff.metadata_changes == []
    assert diff.unchanged_rule_count == len(ruleset.rules)
    assert diff.rule_change_total == 0


def test_added_rule_detected(reference_data: dict, ruleset: Ruleset) -> None:
    new_data = deepcopy(reference_data)
    extra_rule = deepcopy(new_data["rules"][0])
    extra_rule["id"] = "rule_added_for_test"
    new_data["rules"].append(extra_rule)
    new_ruleset = Ruleset.model_validate(new_data)

    diff = diff_rulesets(ruleset, new_ruleset)

    assert len(diff.added_rules) == 1
    assert diff.added_rules[0].id == "rule_added_for_test"
    assert diff.removed_rules == []
    assert diff.modified_rules == []
    assert diff.has_changes


def test_removed_rule_detected(reference_data: dict, ruleset: Ruleset) -> None:
    new_data = deepcopy(reference_data)
    removed_id = new_data["rules"][0]["id"]
    new_data["rules"] = new_data["rules"][1:]
    new_ruleset = Ruleset.model_validate(new_data)

    diff = diff_rulesets(ruleset, new_ruleset)

    assert len(diff.removed_rules) == 1
    assert diff.removed_rules[0].id == removed_id
    assert diff.added_rules == []
    assert diff.modified_rules == []


def test_modified_rule_description_change(reference_data: dict, ruleset: Ruleset) -> None:
    new_data = deepcopy(reference_data)
    target_id = new_data["rules"][0]["id"]
    new_data["rules"][0]["description"] = "DESCRIPTION INTENTIONALLY CHANGED FOR TEST"
    new_ruleset = Ruleset.model_validate(new_data)

    diff = diff_rulesets(ruleset, new_ruleset)

    assert diff.added_rules == []
    assert diff.removed_rules == []
    assert len(diff.modified_rules) == 1
    mod = diff.modified_rules[0]
    assert mod.id == target_id
    assert any(c.field == "description" for c in mod.changes)
    desc_change = next(c for c in mod.changes if c.field == "description")
    assert desc_change.new == "DESCRIPTION INTENTIONALLY CHANGED FOR TEST"


def test_modified_rule_verdict_and_expression_changes(
    reference_data: dict,
    ruleset: Ruleset,
) -> None:
    """A single rule with two field changes reports both in `changes`."""
    new_data = deepcopy(reference_data)
    # Pick a verdict different from whatever the reference rule currently has.
    original = new_data["rules"][0]["verdict_if_triggered"]
    new_data["rules"][0]["verdict_if_triggered"] = "red" if original != "red" else "clear"
    new_data["rules"][0]["expression"] = "false"  # always-clean expression
    new_ruleset = Ruleset.model_validate(new_data)

    diff = diff_rulesets(ruleset, new_ruleset)

    assert len(diff.modified_rules) == 1
    fields_changed = {c.field for c in diff.modified_rules[0].changes}
    assert "verdict_if_triggered" in fields_changed
    assert "expression" in fields_changed


def test_metadata_regulation_change_detected(
    reference_data: dict,
    ruleset: Ruleset,
) -> None:
    new_ruleset = _ruleset_with(reference_data, regulation="Regulation (EU) 2024/1689 (amended)")
    diff = diff_rulesets(ruleset, new_ruleset)

    assert any(c.field == "regulation" for c in diff.metadata_changes)
    assert diff.has_changes


def test_signature_status_transition_detected(
    reference_data: dict,
    ruleset: Ruleset,
) -> None:
    """Going from unsigned to signed must surface as a metadata change."""
    new_data = deepcopy(reference_data)
    new_data["signature"] = {
        "signer_name": "Smith & Co LLP",
        "signer_email": "compliance@smithco.example",
        "signed_date": "2026-05-01",
        "signature_algorithm": "sha256",
        "signature_value": "deadbeef",
    }
    new_ruleset = Ruleset.model_validate(new_data)

    diff = diff_rulesets(ruleset, new_ruleset)

    sig_changes = [c for c in diff.metadata_changes if c.field == "signature_status"]
    assert len(sig_changes) == 1
    assert sig_changes[0].old == "unsigned"
    assert sig_changes[0].new == "signed"


def test_unchanged_count_excludes_modified(
    reference_data: dict,
    ruleset: Ruleset,
) -> None:
    """unchanged_rule_count must not include rules that were modified."""
    new_data = deepcopy(reference_data)
    new_data["rules"][0]["description"] = "modified"
    new_ruleset = Ruleset.model_validate(new_data)

    diff = diff_rulesets(ruleset, new_ruleset)

    assert diff.unchanged_rule_count == len(ruleset.rules) - 1
    assert len(diff.modified_rules) == 1


def test_diff_is_deterministic(reference_data: dict, ruleset: Ruleset) -> None:
    """Same input must always produce the same diff (sorted ordering)."""
    new_data = deepcopy(reference_data)
    extra_rule = deepcopy(new_data["rules"][0])
    extra_rule["id"] = "rule_b_added"
    new_data["rules"].append(extra_rule)
    extra_rule2 = deepcopy(new_data["rules"][0])
    extra_rule2["id"] = "rule_a_added"
    new_data["rules"].append(extra_rule2)
    new_ruleset = Ruleset.model_validate(new_data)

    d1 = diff_rulesets(ruleset, new_ruleset).model_dump()
    d2 = diff_rulesets(ruleset, new_ruleset).model_dump()
    assert d1 == d2
    # Sorted ordering: a comes before b
    diff = diff_rulesets(ruleset, new_ruleset)
    assert diff.added_rules[0].id == "rule_a_added"
    assert diff.added_rules[1].id == "rule_b_added"


# ---------------------------------------------------------------------------
# CLI tests: `litmus diff-ruleset`
# ---------------------------------------------------------------------------


def test_cli_identical_exits_zero(runner: CliRunner, tmp_path: Path) -> None:
    src = REFERENCE_RULESET_PATH.read_text()
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(src)
    b.write_text(src)

    result = runner.invoke(app, ["diff-ruleset", str(a), str(b)])
    assert result.exit_code == 0, result.stdout


def test_cli_changes_exit_one(runner: CliRunner, tmp_path: Path, reference_data: dict) -> None:
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(json.dumps(reference_data))
    new_data = deepcopy(reference_data)
    new_data["rules"][0]["description"] = "changed"
    b.write_text(json.dumps(new_data))

    result = runner.invoke(app, ["diff-ruleset", str(a), str(b)])
    assert result.exit_code == 1, result.stdout


def test_cli_missing_file_exit_two(runner: CliRunner, tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        ["diff-ruleset", str(tmp_path / "nope.json"), str(REFERENCE_RULESET_PATH)],
    )
    assert result.exit_code == 2
    assert "not found" in result.stdout.lower() or "not found" in (result.stderr or "").lower()


def test_cli_invalid_format_exit_two(runner: CliRunner) -> None:
    result = runner.invoke(
        app,
        [
            "diff-ruleset",
            str(REFERENCE_RULESET_PATH),
            str(REFERENCE_RULESET_PATH),
            "--format",
            "yaml",
        ],
    )
    assert result.exit_code == 2


def test_cli_json_output_is_valid_rulesetdiff(
    runner: CliRunner,
    tmp_path: Path,
    reference_data: dict,
) -> None:
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(json.dumps(reference_data))
    new_data = deepcopy(reference_data)
    new_data["rules"][0]["description"] = "changed"
    b.write_text(json.dumps(new_data))

    result = runner.invoke(app, ["diff-ruleset", str(a), str(b), "--format", "json"])
    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    diff = RulesetDiff.model_validate(payload)
    assert len(diff.modified_rules) == 1
    assert diff.modified_rules[0].changes[0].field == "description"


# ---------------------------------------------------------------------------
# Shipped rulesets: v1.0 to v1.1 is additions plus the agreed edits (PRD-411)
# ---------------------------------------------------------------------------


def test_shipped_v1_0_to_v1_1_diff_is_additions_plus_agreed_edits() -> None:
    old = Ruleset.model_validate(json.loads(PREVIOUS_RULESET_PATH.read_text()))
    new = Ruleset.model_validate(json.loads(DEFAULT_RULESET_PATH.read_text()))
    diff = diff_rulesets(old, new)

    assert diff.removed_rules == []
    added = {r.id: r for r in diff.added_rules}
    assert set(added) == {
        "rule_ba_intended_purpose_no_consent",
        "rule_ba_foreseeable_no_safeguards",
        "rule_ba_identifiable_persons_review",
        "rule_bb_minors_sexual_material",
        "rule_bb_without_right_defence_review",
        "rule_bb_no_csam_safeguards",
    }
    assert {r.category for r in added.values()} == {"5.1.ba", "5.1.bb"}
    assert all(r.applies_from == "2026-12-02" for r in added.values())
    assert all(any("Art. 113(a)" in c for c in r.citations) for r in added.values()), (
        "every new rule cites the amended application date"
    )

    modified = {m.id: {c.field for c in m.changes} for m in diff.modified_rules}
    # litmusai#25: the social scoring expression changed. The other three are
    # wording only (em-dashes removed from descriptions).
    assert "expression" in modified.pop("rule_c_social_scoring")
    assert set(modified) == {
        "rule_b_targets_minors_freetext",
        "rule_g_sensitive_classification_general",
        "rule_h_law_enforcement_rbi_exception",
    }
    for fields in modified.values():
        assert "expression" not in fields
        assert "verdict_if_triggered" not in fields

    assert diff.unchanged_rule_count == len(old.rules) - 4
    assert [m.field for m in diff.metadata_changes] == ["regulation"]


def test_shipped_v1_1_has_rules_for_every_category() -> None:
    new = Ruleset.model_validate(json.loads(DEFAULT_RULESET_PATH.read_text()))
    assert {r.category for r in new.rules} == set(ARTICLE_5_CATEGORIES)
    assert new.ruleset_version == "ruleset-2024-1689-v1.1"
    assert new.signature is None


# ---------------------------------------------------------------------------
# Helper-class shape tests (used by the ruleset changelog artifact)
# ---------------------------------------------------------------------------


def test_rule_field_change_serializes_cleanly() -> None:
    change = RuleFieldChange(field="description", old="a", new="b")
    assert change.model_dump() == {"field": "description", "old": "a", "new": "b"}


def test_metadata_change_serializes_cleanly() -> None:
    change = MetadataChange(field="effective_date", old="2025-02-02", new="2026-08-02")
    assert change.model_dump() == {
        "field": "effective_date",
        "old": "2025-02-02",
        "new": "2026-08-02",
    }


def test_rule_modification_holds_multiple_field_changes() -> None:
    mod = RuleModification(
        id="rule_x",
        category="5.1.a",
        changes=[
            RuleFieldChange(field="description", old="old", new="new"),
            RuleFieldChange(field="verdict_if_triggered", old="clear", new="amber"),
        ],
    )
    assert len(mod.changes) == 2
    fields = {c.field for c in mod.changes}
    assert fields == {"description", "verdict_if_triggered"}
