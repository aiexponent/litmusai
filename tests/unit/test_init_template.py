"""The `litmus init` template (PRD-464).

Founder decision of 2026-11-03: the template asks factual questions only;
what each answer does to a verdict is documented in the README, so a user
is not steered towards the answer that gives the verdict they want.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from litmusai.cli.commands.init import _TEMPLATE
from litmusai.models.system import SystemDescription

README = Path(__file__).resolve().parents[2] / "README.md"


def test_template_is_a_valid_declaration() -> None:
    SystemDescription.model_validate(yaml.safe_load(_TEMPLATE))


def test_template_states_no_verdict_effects() -> None:
    lowered = _TEMPLATE.lower()
    for word in ("clears", "amber", "red", "verdict: "):
        assert not re.search(rf"\b{re.escape(word)}\b", lowered), word


def test_every_new_question_has_guidance() -> None:
    lines = _TEMPLATE.splitlines()
    questions = [
        "subliminal_techniques",
        "manipulative_or_deceptive_techniques",
        "exploits_vulnerability",
        "materially_distorts_behaviour",
        "significant_harm_likely",
        "role",
        "human_assessment_on_verifiable_facts",
        "untargeted_collection",
        "builds_facial_recognition_database",
        "emotions_of_workers_or_students",
        "medical_or_safety_reasons",
        "dataset_labelling_or_filtering_only",
        "remote_identification",
        "law_enforcement_purpose",
        "article_5_1_h_objective",
    ]
    for q in questions:
        idx = next(i for i, line in enumerate(lines) if line.strip().startswith(f"{q}:"))
        assert lines[idx - 1].strip().startswith("#"), f"{q} has no comment above it"


def test_readme_shows_the_template_byte_for_byte() -> None:
    text = README.read_text(encoding="utf-8")
    match = re.search(r"This is what `litmus init` writes.*?```yaml\n(.*?)```", text, re.S)
    assert match is not None
    assert match.group(1) == _TEMPLATE
