"""Core Article 5 screening engine (PRD section 8.3)."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, date, datetime
from typing import Any, Literal

from litmusai import __version__
from litmusai.categories import ARTICLE_5_CATEGORIES, CATEGORY_LABELS
from litmusai.engine.expression import ExpressionError, evaluate
from litmusai.engine.hashing import sha256_hash
from litmusai.models.report import (
    CategoryResult,
    Citation,
    ReportSummary,
    RulesetProvenance,
    ScreeningReport,
)
from litmusai.models.ruleset import Ruleset
from litmusai.models.system import SystemDescription

REPORT_VERSION = "1.2"

_PENALTY = "€35M or 7% global turnover (Art. 99(3))"

_DISCLAIMERS = [
    "This is a screening tool, not legal advice.",
    "LitmusAI is not a notified body.",
    "Article 5 screening must be reviewed by qualified legal counsel.",
    "Screening does not confirm compliance with any other article of the EU AI Act.",
    (
        "The ruleset is a good-faith interpretation of Regulation (EU) 2024/1689, "
        "as amended by Regulation (EU) 2026/1744, and may not reflect the views of "
        "the European AI Office or national competent authorities."
    ),
]

UNREVIEWED_LABEL = "UNREVIEWED: internal panel authored, no external legal review"


def _build_ctx(system: SystemDescription) -> dict[str, Any]:
    return {"system": system.model_dump()}


Verdict = Literal["clear", "amber", "red"]
Confidence = Literal["high", "medium", "low"]
SigStatus = Literal["unsigned", "verified", "invalid"]


def _aggregate_verdict(verdicts: Sequence[str]) -> Verdict:
    if "red" in verdicts:
        return "red"
    if "amber" in verdicts:
        return "amber"
    return "clear"


def _aggregate_confidence(confidences: Sequence[str]) -> Confidence:
    order = {"low": 0, "medium": 1, "high": 2}
    if not confidences:
        return "high"
    result: str = min(confidences, key=lambda c: order.get(c, 0))
    return result  # type: ignore[return-value]


def format_applies_from(iso_date: str) -> str:
    """``2026-12-02`` to ``2 December 2026``; an unparsable value is returned as is."""
    try:
        d = date.fromisoformat(iso_date)
    except ValueError:
        return iso_date
    return f"{d.day} {d.strftime('%B %Y')}"


class Screener:
    """Evaluates a SystemDescription against a Ruleset."""

    def __init__(self, ruleset: Ruleset) -> None:
        self._ruleset = ruleset

    def screen(
        self,
        system: SystemDescription,
        *,
        timestamp: datetime | None = None,
    ) -> ScreeningReport:
        ctx = _build_ctx(system)
        input_hash = sha256_hash(system.model_dump())
        ts = timestamp or datetime.now(tz=UTC)

        category_results: dict[str, CategoryResult] = {}

        for cat_id in ARTICLE_5_CATEGORIES:
            cat_rules = [r for r in self._ruleset.rules if r.category == cat_id]
            triggered: list[str] = []
            verdicts: list[str] = []
            confidences: list[str] = []
            citations: list[Citation] = []
            remediations: list[str] = []
            applies_from: set[str] = set()

            for rule in cat_rules:
                try:
                    fired = evaluate(rule.expression, ctx)
                except ExpressionError:
                    fired = False

                if fired:
                    triggered.append(rule.id)
                    verdicts.append(rule.verdict_if_triggered)
                    for cit_str in rule.citations:
                        citations.append(Citation(article=cit_str))
                    if rule.confidence_delta is not None:
                        confidences.append("low")
                    else:
                        confidences.append("high")
                    if rule.applies_from:
                        applies_from.add(rule.applies_from)

            verdict = _aggregate_verdict(verdicts)
            not_screened = not cat_rules
            if not_screened:
                confidence: Confidence = "low"
            else:
                confidence = _aggregate_confidence(confidences) if confidences else "high"

            if verdict in ("red", "amber"):
                remediations.append("Seek qualified EU AI Act counsel before deployment.")

            category_results[cat_id] = CategoryResult(
                label=CATEGORY_LABELS.get(cat_id, cat_id),
                verdict=verdict,
                confidence=confidence,
                rationale=self._build_rationale(
                    cat_id, verdict, triggered, not_screened, sorted(applies_from)
                ),
                triggered_rules=triggered,
                regulation_citations=citations,
                remediation=remediations,
            )

        all_verdicts = [cr.verdict for cr in category_results.values()]
        overall = _aggregate_verdict(all_verdicts)
        red_count = all_verdicts.count("red")
        amber_count = all_verdicts.count("amber")
        clear_count = all_verdicts.count("clear")

        sig = self._ruleset.signature
        sig_status: SigStatus
        if sig is not None:
            prov_label = (
                f"{self._ruleset.ruleset_version} "
                f"(SIGNED by: {sig.signer_name} · {sig.signed_date} · signature verified)"
            )
            sig_status = "verified"
        else:
            prov_label = f"{self._ruleset.ruleset_version} ({UNREVIEWED_LABEL})"
            sig_status = "unsigned"

        return ScreeningReport(
            report_version=REPORT_VERSION,
            ruleset_version=self._ruleset.ruleset_version,
            litmusai_version=__version__,
            generated_at=ts,
            input_hash_sha256=input_hash,
            system=system,
            categories=category_results,
            summary=ReportSummary(
                overall_verdict=overall,
                red_count=red_count,
                amber_count=amber_count,
                clear_count=clear_count,
                requires_legal_review=overall in ("red", "amber"),
                highest_penalty_exposure=_PENALTY,
            ),
            ruleset_provenance=RulesetProvenance(
                ruleset_version=self._ruleset.ruleset_version,
                regulation=self._ruleset.regulation,
                effective_date=self._ruleset.effective_date,
                signer_name=sig.signer_name if sig else None,
                signed_date=sig.signed_date if sig else None,
                signature_status=sig_status,
                display_label=prov_label,
            ),
            disclaimers=_DISCLAIMERS,
            overrides_applied=[],
        )

    def _build_rationale(
        self,
        cat_id: str,
        verdict: str,
        triggered: list[str],
        not_screened: bool,
        applies_from: list[str],
    ) -> str:
        label = CATEGORY_LABELS.get(cat_id, cat_id)
        if not_screened:
            return (
                f"The active ruleset has no rules for {label}; Article {cat_id} was not screened."
            )
        rules_str = ", ".join(triggered)
        if verdict == "clear" and triggered:
            # Only notice rules give a clear verdict (for example the point (a)
            # and (b) questions left unanswered). They lower confidence.
            return (
                f"Clear for {label}, with low confidence. Rules triggered: {rules_str}. "
                f"The declaration does not answer this point's questions; answer them "
                f"in system.yaml to screen Article {cat_id} on its legal elements."
            )
        if verdict == "clear":
            return f"No rules triggered for {label}. No indicators of Article {cat_id} risk."
        if verdict == "amber":
            text = (
                f"Amber for {label}. Rules triggered: {rules_str}. "
                f"Requires legal review before deployment."
            )
        else:
            text = (
                f"RED for {label}. Rules triggered: {rules_str}. "
                f"System likely falls within Article {cat_id} prohibition."
            )
        if applies_from:
            dates = " and ".join(format_applies_from(d) for d in applies_from)
            text += f" The prohibition applies from {dates}."
        return text
