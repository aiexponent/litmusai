"""Every recital a shipped rule cites must be about the point the rule screens.

The map below was read from the text of Regulation (EU) 2024/1689, OJ L,
12.7.2024, at the Publications Office Cellar on 2026-11-02, and from
Regulation (EU) 2026/1744, recitals 12 to 14, on 2026-10-31. Recital 28
introduces the Article 5 prohibitions as a whole; it is allowed for (a) and
(b), the points it describes ("manipulative, exploitative ... practices").

The independent test (PRD-274, verification/) found that ruleset v1.0 and
v1.1 cited recitals about other points; v1.1.1 corrects them. A new rule or a
new citation must pass this test, so the error cannot come back unnoticed.
"""

from __future__ import annotations

import json
import re

import pytest

from litmusai.categories import DEFAULT_RULESET_PATH, OMNIBUS_CATEGORIES, RULESET_DIR
from litmusai.models.ruleset import Ruleset

# Point -> recitals of Regulation (EU) 2024/1689 that are about that point.
RECITALS_2024_1689: dict[str, set[int]] = {
    "5.1.a": {28, 29},  # 29: manipulative and deceptive techniques
    "5.1.b": {28, 29},  # 29: exploiting age, disability or social or economic situation
    "5.1.c": {31},  # social scoring
    "5.1.d": {42},  # individual crime risk prediction, presumption of innocence
    "5.1.e": {43},  # untargeted scraping of facial images
    "5.1.f": {44},  # emotion recognition in the workplace and education
    "5.1.g": {30},  # biometric categorisation of sensitive characteristics
    "5.1.h": set(range(32, 42)),  # real-time remote biometric identification, 32 to 41
}
# Recitals of Regulation (EU) 2026/1744 on points (ba) and (bb).
RECITALS_2026_1744 = {12, 13, 14}

PLAIN_RECITAL = re.compile(r"^Recital (\d+)$")
AMENDING_RECITAL = re.compile(r"^Regulation \(EU\) 2026/1744, recitals? (.+)$")
ARTICLE_5_POINT = re.compile(r"^Art\. 5\(1\)\(([a-z]+)\)")

RULESET = Ruleset.model_validate(json.loads(DEFAULT_RULESET_PATH.read_text()))


@pytest.mark.parametrize("rule", RULESET.rules, ids=lambda r: r.id)
def test_recitals_match_the_point(rule) -> None:
    for citation in rule.citations:
        plain = PLAIN_RECITAL.match(citation)
        if plain:
            assert rule.category not in OMNIBUS_CATEGORIES, (
                f"{rule.id}: points (ba) and (bb) have no recital in 2024/1689; "
                f"cite Regulation (EU) 2026/1744 instead of {citation!r}"
            )
            assert int(plain.group(1)) in RECITALS_2024_1689[rule.category], (
                f"{rule.id} ({rule.category}) cites {citation}, which is about another point"
            )
        amending = AMENDING_RECITAL.match(citation)
        if amending:
            assert rule.category in OMNIBUS_CATEGORIES, f"{rule.id}: {citation}"
            # Every number in "recitals 12 and 13" is checked, not only the first.
            numbers = [int(n) for n in re.findall(r"\d+", amending.group(1))]
            assert numbers, f"{rule.id}: no recital number in {citation!r}"
            assert set(numbers) <= RECITALS_2026_1744, f"{rule.id}: {citation}"
        assert "Recital" not in citation or plain or "2026/1744" in citation, (
            f"{rule.id}: unrecognised recital citation {citation!r}"
        )


@pytest.mark.parametrize("rule", RULESET.rules, ids=lambda r: r.id)
def test_article_citation_names_the_rule_point(rule) -> None:
    letter = rule.category.rsplit(".", 1)[-1]
    points = [m.group(1) for c in rule.citations if (m := ARTICLE_5_POINT.match(c))]
    assert points, f"{rule.id} cites no Article 5(1) point"
    assert set(points) == {letter}, f"{rule.id} ({rule.category}) cites Art. 5(1)({points})"


@pytest.mark.parametrize("path", sorted(RULESET_DIR.glob("ruleset-*.json")), ids=lambda p: p.name)
def test_every_bundled_ruleset_has_its_review_record(path) -> None:
    # The README says the records ship with the package. A .gitignore pattern
    # once kept them out of git and out of every wheel; a fresh CI checkout
    # fails here if that happens again.
    record = RULESET_DIR / path.name.replace("ruleset-", "internal-review-record-").replace(
        ".json", ".md"
    )
    assert record.is_file(), f"{path.name} has no {record.name}"
