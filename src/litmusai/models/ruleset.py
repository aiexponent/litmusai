"""Ruleset models including optional BYO signature block: PRD §7.3, FR-23, FR-34."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from litmusai.categories import ARTICLE_5_CATEGORIES

_ARTICLE_5_CATEGORIES = frozenset(ARTICLE_5_CATEGORIES)

_SNAKE_CASE_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

Verdict = Literal["clear", "amber", "red"]
SignatureAlgorithm = Literal["sha256", "pgp-detached", "x509-pkcs7"]


class Rule(BaseModel, extra="forbid"):
    id: str
    category: str
    version: str
    description: str
    expression: str
    verdict_if_triggered: Verdict
    confidence_delta: int | None = None
    citations: list[str] = Field(default_factory=list)
    reviewed_by: str
    reviewed_date: str
    # ISO date from which the prohibition the rule encodes applies. Empty
    # for rules on provisions that already apply. Reports run before this
    # date say so in the rationale.
    applies_from: str | None = None

    @field_validator("applies_from")
    @classmethod
    def _validate_applies_from(cls, v: str | None) -> str | None:
        if v is not None and not _ISO_DATE_RE.fullmatch(v):
            msg = f"applies_from must be an ISO date (YYYY-MM-DD). Got: {v!r}"
            raise ValueError(msg)
        return v

    @field_validator("id")
    @classmethod
    def _validate_id_snake_case(cls, v: str) -> str:
        if not _SNAKE_CASE_RE.fullmatch(v):
            msg = (
                f"Rule ID must be snake_case (lowercase letters, digits, underscores, "
                f"starting with a letter). Got: {v!r}"
            )
            raise ValueError(msg)
        return v

    @field_validator("category")
    @classmethod
    def _validate_category(cls, v: str) -> str:
        if v not in _ARTICLE_5_CATEGORIES:
            msg = f"Category must be one of {sorted(_ARTICLE_5_CATEGORIES)}. Got: {v!r}"
            raise ValueError(msg)
        return v


class RulesetSignature(BaseModel, extra="forbid"):
    signer_name: str = Field(..., min_length=1)
    signer_bar_number: str | None = None
    signer_firm: str | None = None
    signer_email: EmailStr
    signed_date: str
    signature_algorithm: SignatureAlgorithm
    signature_value: str = Field(..., min_length=1)


class Ruleset(BaseModel, extra="forbid"):
    ruleset_version: str
    regulation: str
    effective_date: str
    rules: list[Rule] = Field(..., min_length=1)
    signature: RulesetSignature | None = None

    @model_validator(mode="after")
    def _validate_unique_rule_ids(self) -> Ruleset:
        ids = [r.id for r in self.rules]
        if len(ids) != len(set(ids)):
            msg = "Rule IDs must be unique within a ruleset."
            raise ValueError(msg)
        return self
