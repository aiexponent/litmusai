"""Ruleset v1.2 (PRD-449): the influence questions for Art. 5(1)(a) and (b),
and the exceptions and limits written in points (d) to (h).

Design decisions of 2026-11-03:
- F1: each legal element is answered yes, no or not_sure; all yes is red,
  any not_sure is amber.
- F2: a file that leaves the questions unanswered keeps its 1.1 verdict, with
  low confidence on (a) and (b).
- F3b: a fact that takes a case outside a prohibition clears it; an exception
  that needs evidence gives amber.
"""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

import pytest

from litmusai.categories import DEFAULT_RULESET_PATH
from litmusai.engine.screener import Screener
from litmusai.models.ruleset import Ruleset
from litmusai.models.system import SystemDescription


@pytest.fixture(scope="module")
def screener() -> Screener:
    return Screener(Ruleset.model_validate(json.loads(DEFAULT_RULESET_PATH.read_text())))


def _system(base: dict[str, Any], **sections: dict[str, Any]) -> SystemDescription:
    d = deepcopy(base)
    for section, values in sections.items():
        d.setdefault(section, {}).update(values)
    return SystemDescription.model_validate(d)


def _verdict(screener: Screener, system: SystemDescription, point: str) -> tuple[str, str]:
    result = screener.screen(system).categories[point]
    return result.verdict, result.confidence


A_ALL_YES = {
    "manipulative_or_deceptive_techniques": "yes",
    "materially_distorts_behaviour": "yes",
    "significant_harm_likely": "yes",
}
B_ALL_YES = {
    "exploits_vulnerability": "yes",
    "materially_distorts_behaviour": "yes",
    "significant_harm_likely": "yes",
}


class TestPointA:
    def test_all_elements_yes_is_red(self, screener, minimal_system_dict) -> None:
        s = _system(minimal_system_dict, influence=A_ALL_YES)
        assert _verdict(screener, s, "5.1.a") == ("red", "high")

    def test_subliminal_technique_counts_like_manipulation(
        self, screener, minimal_system_dict
    ) -> None:
        answers = dict(A_ALL_YES, manipulative_or_deceptive_techniques="no")
        answers["subliminal_techniques"] = "yes"
        s = _system(minimal_system_dict, influence=answers)
        assert _verdict(screener, s, "5.1.a")[0] == "red"

    @pytest.mark.parametrize(
        "field",
        [
            "manipulative_or_deceptive_techniques",
            "materially_distorts_behaviour",
            "significant_harm_likely",
        ],
    )
    def test_any_element_not_sure_is_amber(self, screener, minimal_system_dict, field) -> None:
        s = _system(minimal_system_dict, influence=dict(A_ALL_YES, **{field: "not_sure"}))
        assert _verdict(screener, s, "5.1.a")[0] == "amber"

    @pytest.mark.parametrize("field", ["materially_distorts_behaviour", "significant_harm_likely"])
    def test_an_element_ruled_out_is_clear(self, screener, minimal_system_dict, field) -> None:
        s = _system(minimal_system_dict, influence=dict(A_ALL_YES, **{field: "no"}))
        assert _verdict(screener, s, "5.1.a") == ("clear", "high")

    def test_no_technique_is_clear_even_with_proxies(self, screener, minimal_system_dict) -> None:
        # Answering the questions replaces the 1.1 proxy rules.
        s = _system(
            minimal_system_dict,
            inputs={"emotional_state_inference": True},
            outputs={"behaviour_predictions": True},
            influence={
                "subliminal_techniques": "no",
                "manipulative_or_deceptive_techniques": "no",
            },
        )
        assert _verdict(screener, s, "5.1.a") == ("clear", "high")

    def test_unanswered_keeps_the_proxy_verdict_with_low_confidence(
        self, screener, minimal_system_dict
    ) -> None:
        s = _system(
            minimal_system_dict,
            inputs={"emotional_state_inference": True},
            outputs={"behaviour_predictions": True},
        )
        assert _verdict(screener, s, "5.1.a") == ("red", "low")
        clear = _system(minimal_system_dict)
        assert _verdict(screener, clear, "5.1.a") == ("clear", "low")


class TestPointB:
    def test_all_elements_yes_is_red(self, screener, minimal_system_dict) -> None:
        s = _system(minimal_system_dict, influence=B_ALL_YES)
        assert _verdict(screener, s, "5.1.b") == ("red", "high")

    def test_exploitation_not_sure_is_amber(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict, influence=dict(B_ALL_YES, exploits_vulnerability="not_sure")
        )
        assert _verdict(screener, s, "5.1.b")[0] == "amber"

    def test_no_exploitation_is_clear_even_for_minors(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict,
            subject_population={"categories": ["minors"]},
            outputs={"behaviour_predictions": True},
            influence={"exploits_vulnerability": "no"},
        )
        assert _verdict(screener, s, "5.1.b") == ("clear", "high")

    def test_unanswered_keeps_the_minors_proxy(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict,
            subject_population={"categories": ["minors"]},
            outputs={"behaviour_predictions": True},
        )
        assert _verdict(screener, s, "5.1.b") == ("red", "low")

    def test_older_persons_is_a_population_category(self, minimal_system_dict) -> None:
        s = _system(minimal_system_dict, subject_population={"categories": ["older_persons"]})
        assert s.subject_population.categories == ["older_persons"]


CRIME = {"criminal_risk_predictions": True}


class TestPointD:
    def test_unanswered_stays_red(self, screener, minimal_system_dict) -> None:
        s = _system(minimal_system_dict, outputs=CRIME)
        assert _verdict(screener, s, "5.1.d")[0] == "red"

    def test_human_assessment_claimed_is_amber(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict,
            outputs=CRIME,
            scope={"human_assessment_on_verifiable_facts": "yes"},
        )
        assert _verdict(screener, s, "5.1.d")[0] == "amber"

    def test_not_sure_stays_red(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict,
            outputs=CRIME,
            scope={"human_assessment_on_verifiable_facts": "not_sure"},
        )
        assert _verdict(screener, s, "5.1.d")[0] == "red"


SCRAPE = {"facial_images": True, "scraped_internet_data": True}


class TestPointE:
    def test_unanswered_stays_red(self, screener, minimal_system_dict) -> None:
        assert _verdict(screener, _system(minimal_system_dict, inputs=SCRAPE), "5.1.e")[0] == "red"

    @pytest.mark.parametrize(
        "field", ["untargeted_collection", "builds_facial_recognition_database"]
    )
    def test_a_no_clears(self, screener, minimal_system_dict, field) -> None:
        s = _system(
            minimal_system_dict,
            inputs=SCRAPE,
            deployment_context={"public_space": True},
            scope={field: "no"},
        )
        assert _verdict(screener, s, "5.1.e")[0] == "clear"


EMOTION_AT_WORK = {
    "outputs": {"emotion_inferences": True},
    "deployment_context": {"workplace": True},
}


class TestPointF:
    def test_unanswered_stays_red(self, screener, minimal_system_dict) -> None:
        assert (
            _verdict(screener, _system(minimal_system_dict, **EMOTION_AT_WORK), "5.1.f")[0] == "red"
        )

    def test_customers_only_clears(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict,
            **EMOTION_AT_WORK,
            scope={"emotions_of_workers_or_students": "no"},
        )
        assert _verdict(screener, s, "5.1.f")[0] == "clear"

    def test_patients_in_a_practice_clear(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict,
            outputs={"emotion_inferences": True},
            deployment_context={"workplace": True, "healthcare": True},
            scope={"emotions_of_workers_or_students": "no"},
        )
        assert _verdict(screener, s, "5.1.f")[0] == "clear"

    def test_medical_or_safety_claimed_is_amber(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict, **EMOTION_AT_WORK, scope={"medical_or_safety_reasons": "yes"}
        )
        assert _verdict(screener, s, "5.1.f")[0] == "amber"

    def test_education_follows_the_same_rule(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict,
            outputs={"emotion_inferences": True},
            deployment_context={"education": True},
        )
        assert _verdict(screener, s, "5.1.f")[0] == "red"
        s = _system(
            minimal_system_dict,
            outputs={"emotion_inferences": True},
            deployment_context={"education": True},
            scope={"medical_or_safety_reasons": "yes"},
        )
        assert _verdict(screener, s, "5.1.f")[0] == "amber"


SENSITIVE = {
    "inputs": {"biometric": True},
    "outputs": {"sensitive_attribute_classifications": True},
}


class TestPointG:
    def test_unanswered_stays_red(self, screener, minimal_system_dict) -> None:
        assert _verdict(screener, _system(minimal_system_dict, **SENSITIVE), "5.1.g")[0] == "red"

    def test_labelling_claimed_is_amber(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict, **SENSITIVE, scope={"dataset_labelling_or_filtering_only": "yes"}
        )
        assert _verdict(screener, s, "5.1.g")[0] == "amber"


RBI = {
    "inputs": {"biometric": True, "facial_images": True},
    "deployment_context": {"public_space": True, "real_time_operation": True},
}


class TestPointH:
    def test_unanswered_stays_red(self, screener, minimal_system_dict) -> None:
        assert _verdict(screener, _system(minimal_system_dict, **RBI), "5.1.h")[0] == "red"

    @pytest.mark.parametrize(
        "scope",
        [
            {"role": "provider_only"},
            {"remote_identification": "no"},
            {"law_enforcement_purpose": "no"},
        ],
    )
    def test_outside_the_prohibition_clears(self, screener, minimal_system_dict, scope) -> None:
        s = _system(minimal_system_dict, **RBI, scope=scope)
        assert _verdict(screener, s, "5.1.h")[0] == "clear"

    def test_objective_claimed_is_amber(self, screener, minimal_system_dict) -> None:
        s = _system(
            minimal_system_dict,
            **RBI,
            scope={"law_enforcement_purpose": "yes", "article_5_1_h_objective": "yes"},
        )
        assert _verdict(screener, s, "5.1.h")[0] == "amber"

    def test_deployer_for_law_enforcement_without_objective_is_red(
        self, screener, minimal_system_dict
    ) -> None:
        s = _system(
            minimal_system_dict,
            **RBI,
            scope={"role": "deployer", "law_enforcement_purpose": "yes"},
        )
        assert _verdict(screener, s, "5.1.h")[0] == "red"


def test_invalid_answer_is_rejected(minimal_system_dict) -> None:
    with pytest.raises(ValueError):
        _system(minimal_system_dict, influence={"significant_harm_likely": "maybe"})


def test_unquoted_yaml_yes_and_no_are_answers(minimal_system_dict) -> None:
    import yaml

    raw = yaml.safe_load(
        "influence:\n  subliminal_techniques: yes\n  significant_harm_likely: no\n"
    )
    s = _system(minimal_system_dict, **raw)
    assert s.influence.subliminal_techniques == "yes"
    assert s.influence.significant_harm_likely == "no"


PROXY_A: dict[str, dict[str, Any]] = {
    "inputs": {"emotional_state_inference": True},
    "outputs": {"behaviour_predictions": True},
}


class TestPartialAnswers:
    """Review of litmusai#38: a partly answered (a) or (b) must not read as
    fully screened, and a shared element ruled out must clear the proxies."""

    def test_one_technique_no_other_unanswered_keeps_proxies_and_low_confidence(
        self, screener, minimal_system_dict
    ) -> None:
        s = _system(minimal_system_dict, **PROXY_A, influence={"subliminal_techniques": "no"})
        assert _verdict(screener, s, "5.1.a") == ("red", "low")
        clear = _system(minimal_system_dict, influence={"subliminal_techniques": "no"})
        assert _verdict(screener, clear, "5.1.a") == ("clear", "low")

    @pytest.mark.parametrize("field", ["materially_distorts_behaviour", "significant_harm_likely"])
    def test_a_shared_element_ruled_out_clears_the_a_proxies(
        self, screener, minimal_system_dict, field
    ) -> None:
        s = _system(minimal_system_dict, **PROXY_A, influence={field: "no"})
        assert _verdict(screener, s, "5.1.a") == ("clear", "high")

    @pytest.mark.parametrize("field", ["materially_distorts_behaviour", "significant_harm_likely"])
    def test_a_shared_element_ruled_out_clears_the_b_proxies(
        self, screener, minimal_system_dict, field
    ) -> None:
        s = _system(
            minimal_system_dict,
            subject_population={"categories": ["minors"]},
            outputs={"behaviour_predictions": True},
            influence={field: "no"},
        )
        assert _verdict(screener, s, "5.1.b") == ("clear", "high")

    def test_rationale_states_the_computed_confidence(self, screener, minimal_system_dict) -> None:
        result = screener.screen(_system(minimal_system_dict)).categories["5.1.a"]
        assert result.confidence == "low"
        assert "with low confidence" in result.rationale
