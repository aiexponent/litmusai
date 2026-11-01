"""Rules for Article 5(1)(ba) and (bb), the litmusai#25 social scoring fix,
the ``applies_from`` field and the "not screened" rationale (PRD-411).

Source for the rule text: Regulation (EU) 2026/1744, Article 1, point (7),
read at the Publications Office Cellar (CELEX 32026R1744) on 2026-10-31.
"""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from litmusai.categories import (
    ARTICLE_5_CATEGORIES,
    DEFAULT_RULESET_PATH,
    OMNIBUS_APPLIES_FROM,
    PREVIOUS_RULESET_PATH,
)
from litmusai.engine.diff import diff_rulesets
from litmusai.engine.screener import Screener, format_applies_from
from litmusai.models.ruleset import Rule, Ruleset
from litmusai.models.system import SystemDescription

FIXED_TS = datetime(2026, 11, 15, 12, 0, 0, tzinfo=UTC)


@pytest.fixture(scope="module")
def screener() -> Screener:
    return Screener(Ruleset.model_validate(json.loads(DEFAULT_RULESET_PATH.read_text())))


@pytest.fixture(scope="module")
def v1_0_screener() -> Screener:
    return Screener(Ruleset.model_validate(json.loads(PREVIOUS_RULESET_PATH.read_text())))


def _system(base: dict[str, Any], **sections: dict[str, Any]) -> SystemDescription:
    """Build a SystemDescription from the clear baseline plus nested overrides."""
    d = deepcopy(base)
    for section, values in sections.items():
        target = d.setdefault(section, {})
        for key, val in values.items():
            if isinstance(val, dict):
                target.setdefault(key, {}).update(val)
            else:
                target[key] = val
    return SystemDescription.model_validate(d)


ALL_SAFEGUARDS = {
    "consent_demonstrable": True,
    "intimate_output_prevention": True,
    "csam_prevention": True,
    "misuse_correction": True,
    "documented": True,
}


# ---------------------------------------------------------------------------
# 5.1.ba: non-consensual intimate material of identifiable persons
# ---------------------------------------------------------------------------


class TestArticle5BA:
    def test_intended_purpose_without_consent_is_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": True,
                "intimate_depictions_intended": True,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.ba"]
        assert cat.verdict == "red"
        assert "rule_ba_intended_purpose_no_consent" in cat.triggered_rules
        assert report.summary.overall_verdict == "red"

    def test_intended_purpose_safeguards_do_not_rescue(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        """Art. 5(1a)(a)(i): intended purpose is prohibited whatever the filters."""
        safeguards = dict(ALL_SAFEGUARDS, consent_demonstrable=False)
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": True,
                "intimate_depictions_intended": True,
                "safeguards": safeguards,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.ba"].verdict == "red"

    def test_consent_takes_intended_purpose_out_of_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        """(ba) only bites "without that person's ... explicit consent"."""
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": True,
                "intimate_depictions_intended": True,
                "safeguards": {"consent_demonstrable": True, "documented": True},
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.ba"].verdict == "clear"

    def test_foreseeable_outcome_without_safeguards_is_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        """Art. 5(1a)(a)(ii): a general generator with no measures."""
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": True,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.ba"]
        assert cat.verdict == "red"
        assert "rule_ba_foreseeable_no_safeguards" in cat.triggered_rules
        assert "rule_ba_intended_purpose_no_consent" not in cat.triggered_rules

    def test_partial_safeguards_stay_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        """Prevention without misuse correction, or without documentation, is not adequate."""
        for partial in (
            {"intimate_output_prevention": True, "documented": True},
            {"intimate_output_prevention": True, "misuse_correction": True},
        ):
            system = _system(
                minimal_system_dict,
                generative_media={
                    "realistic_media_generation": True,
                    "identifiable_persons": True,
                    "intimate_depictions_possible": True,
                    "safeguards": partial,
                },
            )
            report = screener.screen(system, timestamp=FIXED_TS)
            assert report.categories["5.1.ba"].verdict == "red", partial

    def test_adequate_safeguards_make_foreseeable_case_clear(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": False,
                "safeguards": ALL_SAFEGUARDS,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.ba"].verdict == "clear"
        assert report.categories["5.1.bb"].verdict == "clear"
        assert report.summary.overall_verdict == "clear"

    def test_identifiable_persons_with_unclear_safeguards_is_amber(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": False,
                "safeguards": {"intimate_output_prevention": True, "documented": False},
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.ba"]
        assert cat.verdict == "amber"
        assert cat.triggered_rules == ["rule_ba_identifiable_persons_review"]

    def test_manipulation_within_1b_is_never_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        """Art. 5(1b): edits that do not increase exposure are not manipulation."""
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": True,
                "manipulation_within_1b_only": True,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.ba"]
        assert cat.verdict == "amber"
        assert "rule_ba_foreseeable_no_safeguards" not in cat.triggered_rules

    def test_no_identifiable_persons_means_no_ba(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": False,
                "intimate_depictions_possible": True,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.ba"].verdict == "clear"

    def test_ba_citations_and_applies_from(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": True,
                "intimate_depictions_intended": True,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.ba"]
        articles = {c.article for c in cat.regulation_citations}
        assert "Art. 5(1)(ba)" in articles
        assert any(
            a.startswith("Art. 113(a), as amended by Regulation (EU) 2026/1744") for a in articles
        )
        assert "The prohibition applies from 2 December 2026." in cat.rationale


# ---------------------------------------------------------------------------
# 5.1.bb: child sexual abuse material
# ---------------------------------------------------------------------------


class TestArticle5BB:
    def test_minors_material_without_prevention_is_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "intimate_depictions_possible": True,
                "minors_depictions_possible": True,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.bb"]
        assert cat.verdict == "red"
        assert "rule_bb_minors_sexual_material" in cat.triggered_rules
        assert "Directive 2011/93/EU, Art. 2(c) and (e)" in {
            c.article for c in cat.regulation_citations
        }

    def test_consent_is_irrelevant_for_bb(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "intimate_depictions_possible": True,
                "minors_depictions_possible": True,
                "safeguards": {"consent_demonstrable": True, "documented": True},
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.bb"].verdict == "red"

    def test_csam_prevention_takes_it_out_of_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "intimate_depictions_possible": True,
                "minors_depictions_possible": True,
                "safeguards": {"csam_prevention": True},
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.bb"]
        assert cat.verdict == "amber"
        assert cat.triggered_rules == ["rule_bb_no_csam_safeguards"]

    def test_documented_csam_prevention_is_clear(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "intimate_depictions_possible": True,
                "minors_depictions_possible": False,
                "safeguards": {"csam_prevention": True, "documented": True},
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.bb"].verdict == "clear"

    def test_law_enforcement_use_is_amber_for_review(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        """A 'without right' defence under national law may apply; never cleared here."""
        system = _system(
            minimal_system_dict,
            deployment_context={"law_enforcement_use": True},
            generative_media={
                "realistic_media_generation": True,
                "intimate_depictions_possible": True,
                "minors_depictions_possible": True,
            },
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.bb"]
        assert cat.verdict == "amber"
        assert "rule_bb_without_right_defence_review" in cat.triggered_rules
        assert "rule_bb_minors_sexual_material" not in cat.triggered_rules

    def test_any_realistic_generator_without_documented_prevention_is_amber(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={"realistic_media_generation": True},
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.bb"].verdict == "amber"
        assert report.categories["5.1.ba"].verdict == "clear"

    def test_non_generative_system_is_clear(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        report = screener.screen(SystemDescription(**minimal_system_dict), timestamp=FIXED_TS)
        assert report.categories["5.1.ba"].verdict == "clear"
        assert report.categories["5.1.bb"].verdict == "clear"
        assert report.categories["5.1.ba"].confidence == "high"


# ---------------------------------------------------------------------------
# litmusai#25: social scoring is about social behaviour, not any history
# ---------------------------------------------------------------------------


class TestSocialScoringIssue25:
    def test_scores_from_behaviour_history_alone_are_amber(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        """Credit scoring from repayment history: high-risk (Annex III), not prohibited."""
        system = _system(
            minimal_system_dict,
            inputs={"behaviour_history": True},
            outputs={"individual_scores": True},
            deployment_context={"financial_services": True},
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.c"]
        assert cat.verdict == "amber"
        assert cat.triggered_rules == ["rule_c_scoring_general"]

    def test_scores_from_social_behaviour_data_are_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            inputs={"social_behaviour_data": True},
            outputs={"individual_scores": True},
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        cat = report.categories["5.1.c"]
        assert cat.verdict == "red"
        assert "rule_c_social_scoring" in cat.triggered_rules

    def test_scores_used_in_unrelated_context_are_red(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            inputs={"behaviour_history": True},
            outputs={"individual_scores": True, "detrimental_treatment_unrelated_context": True},
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.c"].verdict == "red"

    def test_v1_0_ruleset_still_flags_credit_scoring_red(
        self, v1_0_screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        """Documents the behaviour the v1.1 ruleset corrects."""
        system = _system(
            minimal_system_dict,
            inputs={"behaviour_history": True},
            outputs={"individual_scores": True},
        )
        report = v1_0_screener.screen(system, timestamp=FIXED_TS)
        assert report.categories["5.1.c"].verdict == "red"


# ---------------------------------------------------------------------------
# Categories the active ruleset has no rules for
# ---------------------------------------------------------------------------


class TestNotScreened:
    def test_v1_0_ruleset_reports_ba_and_bb_as_not_screened(
        self, v1_0_screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            generative_media={
                "realistic_media_generation": True,
                "identifiable_persons": True,
                "intimate_depictions_possible": True,
                "intimate_depictions_intended": True,
            },
        )
        report = v1_0_screener.screen(system, timestamp=FIXED_TS)
        for cat_id in ("5.1.ba", "5.1.bb"):
            cat = report.categories[cat_id]
            assert cat.verdict == "clear"
            assert cat.confidence == "low"
            assert "not screened" in cat.rationale
            assert cat.triggered_rules == []
        assert report.summary.overall_verdict == "clear"
        assert list(report.categories) == list(ARTICLE_5_CATEGORIES)

    def test_screened_but_quiet_category_keeps_high_confidence(
        self, v1_0_screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        report = v1_0_screener.screen(SystemDescription(**minimal_system_dict), timestamp=FIXED_TS)
        assert report.categories["5.1.a"].confidence == "high"
        assert "not screened" not in report.categories["5.1.a"].rationale


# ---------------------------------------------------------------------------
# applies_from
# ---------------------------------------------------------------------------


class TestAppliesFrom:
    def _rule(self, **overrides: Any) -> Rule:
        data: dict[str, Any] = {
            "id": "rule_test",
            "category": "5.1.ba",
            "version": "v1",
            "description": "test",
            "expression": "true",
            "verdict_if_triggered": "amber",
            "reviewed_by": "panel",
            "reviewed_date": "2026-10-31",
        }
        data.update(overrides)
        return Rule.model_validate(data)

    def test_optional_and_defaults_to_none(self) -> None:
        assert self._rule().applies_from is None

    def test_accepts_iso_date(self) -> None:
        assert self._rule(applies_from=OMNIBUS_APPLIES_FROM).applies_from == "2026-12-02"

    @pytest.mark.parametrize("bad", ["2 December 2026", "2026/12/02", "20261202", ""])
    def test_rejects_non_iso(self, bad: str) -> None:
        with pytest.raises(ValidationError):
            self._rule(applies_from=bad)

    def test_diff_engine_sees_applies_from_change(self) -> None:
        base = {
            "ruleset_version": "t",
            "regulation": "r",
            "effective_date": "2025-02-02",
            "rules": [self._rule().model_dump()],
        }
        old = Ruleset.model_validate(base)
        changed = deepcopy(base)
        changed["rules"][0]["applies_from"] = OMNIBUS_APPLIES_FROM
        new = Ruleset.model_validate(changed)
        diff = diff_rulesets(old, new)
        assert [c.field for c in diff.modified_rules[0].changes] == ["applies_from"]

    def test_format_applies_from(self) -> None:
        assert format_applies_from("2026-12-02") == "2 December 2026"
        assert format_applies_from("not-a-date") == "not-a-date"

    def test_rules_without_applies_from_add_nothing_to_rationale(
        self, screener: Screener, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = _system(
            minimal_system_dict,
            outputs={"emotion_inferences": True},
            deployment_context={"workplace": True},
        )
        report = screener.screen(system, timestamp=FIXED_TS)
        assert "applies from" not in report.categories["5.1.f"].rationale


# ---------------------------------------------------------------------------
# Backwards compatibility of the declaration schema
# ---------------------------------------------------------------------------


class TestSchemaCompatibility:
    def test_v1_0_system_yaml_without_new_fields_still_validates(
        self, minimal_system_dict: dict[str, Any]
    ) -> None:
        system = SystemDescription(**minimal_system_dict)
        assert system.generative_media.realistic_media_generation is False
        assert system.generative_media.safeguards.documented is False
        assert system.inputs.social_behaviour_data is False
        assert system.outputs.detrimental_treatment_unrelated_context is False

    def test_unknown_generative_media_field_rejected(
        self, minimal_system_dict: dict[str, Any]
    ) -> None:
        d = deepcopy(minimal_system_dict)
        d["generative_media"] = {"deepfakes": True}
        with pytest.raises(ValidationError):
            SystemDescription.model_validate(d)
