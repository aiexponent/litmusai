"""Article 5(1) category registry: the one list every module reads.

Regulation (EU) 2024/1689, Article 5(1), first subparagraph, has ten points
once Regulation (EU) 2026/1744 applies (Article 1, point (7) inserts points
(ba) and (bb); the amended Article 113, third paragraph, point (a), applies
them from 2 December 2026). The order below is the order of the regulation.

The reference ruleset shipped with the package lives next to this file under
``_data/ruleset/``. ``DEFAULT_RULESET_PATH`` is the one the CLI loads when
no ``--ruleset`` option and no ``litmus use-ruleset`` choice is in force.
"""

from __future__ import annotations

from pathlib import Path

ARTICLE_5_CATEGORIES: tuple[str, ...] = (
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

CATEGORY_LABELS: dict[str, str] = {
    "5.1.a": "Harmful manipulation",
    "5.1.b": "Exploitation of vulnerabilities",
    "5.1.ba": "Non-consensual intimate material of identifiable persons",
    "5.1.bb": "Child sexual abuse material",
    "5.1.c": "Social scoring",
    "5.1.d": "Criminal risk prediction (individual)",
    "5.1.e": "Untargeted facial image scraping",
    "5.1.f": "Emotion inference (workplace/education)",
    "5.1.g": "Biometric categorisation (sensitive attributes)",
    "5.1.h": "Real-time remote biometric identification (public spaces)",
}

# Points inserted by Regulation (EU) 2026/1744. Rules for them carry an
# ``applies_from`` date so a report run before that date says so.
OMNIBUS_CATEGORIES: frozenset[str] = frozenset({"5.1.ba", "5.1.bb"})
OMNIBUS_APPLIES_FROM = "2026-12-02"

RULESET_DIR: Path = Path(__file__).resolve().parent / "_data" / "ruleset"
DEFAULT_RULESET_FILENAME = "ruleset-2024-1689-v1.1.1.json"
DEFAULT_RULESET_PATH: Path = RULESET_DIR / DEFAULT_RULESET_FILENAME
# Earlier rulesets stay in the package so `litmus diff-ruleset` and
# `--ruleset` can still reach them. v1.1.1 corrects recital citations only.
PREVIOUS_RULESET_PATH: Path = RULESET_DIR / "ruleset-2024-1689-v1.1.json"
V1_0_RULESET_PATH: Path = RULESET_DIR / "ruleset-2024-1689-v1.0.json"

__all__ = [
    "ARTICLE_5_CATEGORIES",
    "CATEGORY_LABELS",
    "DEFAULT_RULESET_FILENAME",
    "DEFAULT_RULESET_PATH",
    "OMNIBUS_APPLIES_FROM",
    "OMNIBUS_CATEGORIES",
    "PREVIOUS_RULESET_PATH",
    "RULESET_DIR",
    "V1_0_RULESET_PATH",
]
