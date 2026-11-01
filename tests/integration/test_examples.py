"""Integration test: verify every published example yields its expected verdict.

The `examples/` directory is a public-facing artefact: it ships with the
package, the README references it, and `litmus init` produces a starter
file modelled on `example-clear.yaml`. Any rule change that flips one of
these examples to a different verdict must surface in CI before release.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from litmusai.categories import DEFAULT_RULESET_PATH
from litmusai.engine.screener import Screener
from litmusai.models.ruleset import Ruleset
from litmusai.models.system import SystemDescription

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES_DIR = REPO_ROOT / "examples"
RULESET_PATH = DEFAULT_RULESET_PATH


@pytest.fixture(scope="module")
def screener() -> Screener:
    ruleset = Ruleset.model_validate(json.loads(RULESET_PATH.read_text()))
    return Screener(ruleset)


def _load_system(name: str) -> SystemDescription:
    path = EXAMPLES_DIR / name
    return SystemDescription.model_validate(yaml.safe_load(path.read_text()))


@pytest.mark.integration
def test_example_clear_yields_clear(screener: Screener) -> None:
    system = _load_system("example-clear.yaml")
    report = screener.screen(system)
    assert report.summary.overall_verdict == "clear"
    fired = [cat for cat, r in report.categories.items() if r.verdict != "clear"]
    assert fired == [], f"example-clear should fire no rules; got {fired}"


@pytest.mark.integration
def test_example_amber_yields_amber(screener: Screener) -> None:
    system = _load_system("example-amber.yaml")
    report = screener.screen(system)
    assert report.summary.overall_verdict == "amber"
    reds = [cat for cat, r in report.categories.items() if r.verdict == "red"]
    ambers = [cat for cat, r in report.categories.items() if r.verdict == "amber"]
    assert reds == [], f"example-amber should produce zero reds; got {reds}"
    assert len(ambers) == 1, f"example-amber should produce exactly one amber; got {ambers}"


@pytest.mark.integration
def test_example_red_yields_red_on_5_1_f_only(screener: Screener) -> None:
    system = _load_system("example-red.yaml")
    report = screener.screen(system)
    assert report.summary.overall_verdict == "red"
    reds = [cat for cat, r in report.categories.items() if r.verdict == "red"]
    assert len(reds) == 1, f"example-red should produce exactly one red (5.1.f); got {reds}"
    assert reds[0] == "5.1.f", f"example-red's red verdict should be on 5.1.f; got {reds[0]}"


@pytest.mark.integration
def test_example_ba_red_yields_red_on_5_1_ba(screener: Screener) -> None:
    system = _load_system("example-ba-red.yaml")
    report = screener.screen(system)
    assert report.summary.overall_verdict == "red"
    verdicts = {cat: r.verdict for cat, r in report.categories.items() if r.verdict != "clear"}
    assert verdicts == {"5.1.ba": "red", "5.1.bb": "amber"}, verdicts
    assert "rule_ba_intended_purpose_no_consent" in report.categories["5.1.ba"].triggered_rules


@pytest.mark.integration
def test_example_bb_red_yields_red_on_5_1_bb_only(screener: Screener) -> None:
    system = _load_system("example-bb-red.yaml")
    report = screener.screen(system)
    assert report.summary.overall_verdict == "red"
    verdicts = {cat: r.verdict for cat, r in report.categories.items() if r.verdict != "clear"}
    assert verdicts == {"5.1.bb": "red"}, verdicts
    assert report.categories["5.1.ba"].verdict == "clear", "no identifiable persons, so no (ba)"


@pytest.mark.integration
def test_example_generative_clear_yields_clear(screener: Screener) -> None:
    system = _load_system("example-generative-clear.yaml")
    report = screener.screen(system)
    assert report.summary.overall_verdict == "clear"
    fired = [cat for cat, r in report.categories.items() if r.verdict != "clear"]
    assert fired == [], f"a safeguarded generator should fire no rules; got {fired}"


@pytest.mark.integration
def test_every_example_file_is_covered() -> None:
    """A new example without a test here would ship unchecked."""
    tested = {
        "example-clear.yaml",
        "example-amber.yaml",
        "example-red.yaml",
        "example-ba-red.yaml",
        "example-bb-red.yaml",
        "example-generative-clear.yaml",
    }
    assert {p.name for p in EXAMPLES_DIR.glob("*.yaml")} == tested
