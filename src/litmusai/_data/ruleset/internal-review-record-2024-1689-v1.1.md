# Internal Ruleset Review Record

**Ruleset version:** `ruleset-2024-1689-v1.1`
**Regulation:** Regulation (EU) 2024/1689 (EU AI Act), as amended by Regulation (EU) 2026/1744 (Digital Omnibus on AI)
**Review date:** 2026-10-31
**Status:** Internal panel review, NOT external legal review
**Supersedes:** `internal-review-record-2024-1689-v1.0.md` (2026-04-16), which stays in the package as the record for the 22 rules carried over.

---

## What changed from v1.0

| Change | Rules | Why |
|--------|-------|-----|
| Added | `rule_ba_intended_purpose_no_consent`, `rule_ba_foreseeable_no_safeguards`, `rule_ba_identifiable_persons_review` | Article 5(1)(ba), inserted by Regulation (EU) 2026/1744, applies from 2 December 2026 |
| Added | `rule_bb_minors_sexual_material`, `rule_bb_without_right_defence_review`, `rule_bb_no_csam_safeguards` | Article 5(1)(bb), same regulation and date |
| Modified | `rule_c_social_scoring` (expression) | litmusai#25: the v1.0 expression fired Red on any individual score built from behaviour history, including credit scoring, which is high-risk under Annex III, point 5(b), not prohibited |
| Modified | `rule_b_targets_minors_freetext`, `rule_g_sensitive_classification_general`, `rule_h_law_enforcement_rbi_exception` (description only) | Wording: em-dashes removed. Expressions and verdicts unchanged |
| Metadata | `regulation` | Names the amending regulation |

All 28 rules carry `reviewed_by: aiexponent-internal-panel-v2` where they were touched in this review, and the v1 panel id where they were not.

## Source

Regulation (EU) 2026/1744 of the European Parliament and of the Council of 8 July 2026, Official Journal L series, 24 July 2026. Read at the Publications Office Cellar, CELEX 32026R1744, on 2026-10-31:

- Article 1, point (7)(a): inserts points (ba) and (bb) into Article 5(1), first subparagraph.
- Article 1, point (7)(b): inserts paragraphs 1a and 1b into Article 5.
- Article 1, point (40)(a): replaces Article 113, third paragraph, point (a), so that points (ba) and (bb) and paragraphs 1a and 1b apply from 2 December 2026.
- Recitals 12, 13 and 14 on the scope of the two prohibitions, the measures expected of providers, the "without right" defence and proportionality.

Every claim in this record about what the regulation says was checked against that text on that date. The rule expressions are the panel's interpretation of it and have not been checked by a lawyer.

---

## Panel Members

| Role | Name | Affiliation |
|------|------|-------------|
| Compliance Engineer | AiExponent Internal | AI Exponent LLC |
| AI Governance Analyst | AiExponent Internal | AI Exponent LLC |
| Responsible AI Lead | AiExponent Internal | AI Exponent LLC |
| Head of AI Governance (Chair) | AiExponent Internal | AI Exponent LLC |
| Security Engineer | AiExponent Internal | AI Exponent LLC |

**None of the above are qualified EU AI Act lawyers. This record is an engineering review by AiExponent staff, not legal advice to any specific customer and not a substitute for qualified EU AI Act counsel.**

---

## Per-Category Sign-Off (new and changed rules)

### 5.1.ba: Non-consensual intimate material of identifiable persons (3 rules, new)

The declaration block `generative_media` carries the facts these rules test. Article 5(1a)(a) gives two provider-side cases; Article 5(1a)(b) limits the deployer-side prohibition to use for that purpose; Article 5(1b) takes a class of edits out of "manipulation".

- `rule_ba_intended_purpose_no_consent`: RED when `intimate_depictions_intended`, `identifiable_persons`, and consent is not demonstrable. Encodes Art. 5(1a)(a)(i) and (b). Technical safeguards do not rescue an intended-purpose system; only consent of the depicted person does, because point (ba) reads "without that person's freely-given, specific, informed, unambiguous and explicit consent". **Approved.**
- `rule_ba_foreseeable_no_safeguards`: RED when realistic media of identifiable persons can show intimate parts or sexual activity as a foreseeable and reproducible outcome, consent is not demonstrable, the edits are not within Art. 5(1b), and the system lacks the combination of prevention, misuse correction and documentation. Encodes Art. 5(1a)(a)(ii): "reasonable and adequate technical safety measures and other safeguards to reliably prevent that generation or manipulation ... and to correct observed or reported misuse". **Approved.**
- `rule_ba_identifiable_persons_review`: AMBER when realistic media of identifiable persons is generated and neither documented prevention nor documented, demonstrable consent is in place. **Approved.**
- **Panel note:** "adequate" is self-asserted through the `safeguards` flags. Recital 12 lists the kinds of measures expected (data cleaning, refusal training, safe prompt design, output controls, prompt guardrails, content classifiers and filters, usage restrictions, abuse detection, notice and action). The rules cannot verify that a declared measure meets the state of the art. The amber rule exists so that an undocumented claim still reaches a reviewer.
- **Panel note:** realism. Recital 12 limits the prohibition to realistic depictions of a person's face, voice or body and excludes cartoonish or physically impossible depictions. The `realistic_media_generation` flag carries that distinction; the rules do not inspect outputs.

### 5.1.bb: Child sexual abuse material (3 rules, new)

- `rule_bb_minors_sexual_material`: RED when realistic media can show sexual content, can depict children, no prevention measure is in place, and the use is not law enforcement. Encodes Art. 5(1a)(a). No consent dimension: consent is not a carve-out of point (bb). **Approved.**
- `rule_bb_without_right_defence_review`: AMBER instead of RED for the same facts in law-enforcement use, because point (bb) excepts cases "where a 'without right' defence applies under national law" and recital 13 names criminal proceedings, crime prevention and red-teaming for compliance evaluation. The rule never clears such a system; a reviewer decides. **Approved.**
- `rule_bb_no_csam_safeguards`: AMBER for any realistic-media generator without documented prevention measures. Conservative by design, in line with the v1.0 amber rules. **Approved.**
- **Panel note:** identifiability is not an element of point (bb). Fully synthetic depictions of children are in scope. The rules therefore do not require `identifiable_persons`.
- **Panel note:** "material or performance within the meaning of Article 2, points (c) and (e), of Directive 2011/93/EU" is carried by the `minors_depictions_possible` flag together with `intimate_depictions_possible`. The panel did not read Directive 2011/93/EU for this record; the citation points the reviewer to it.

### 5.1.c: Social scoring (1 rule modified, litmusai#25)

- `rule_c_social_scoring` v2: RED when individual scores are produced from `social_behaviour_data`, or when `detrimental_treatment_unrelated_context` holds. Article 5(1)(c) requires evaluation or classification "based on their social behaviour or known, inferred or predicted personal or personality characteristics" and detrimental treatment in an unrelated context or disproportionate to the behaviour. Behaviour history alone (repayment records, usage logs in the same service) is not that. **Approved.**
- `rule_c_scoring_general` (unchanged): AMBER for any individual scoring, so a credit score still reaches a reviewer and the Annex III high-risk question is raised. **Unchanged.**
- **Panel note:** the two new fields are self-declared. A deployer who scores from social media data and declares `social_behaviour_data: false` gets Amber instead of Red. Self-declaration dependency is weakness 1 of the v1.0 record and still applies.

### Rules carried over unchanged (19 rules)

See `internal-review-record-2024-1689-v1.0.md`. The three description-only edits do not change any verdict; `litmus diff-ruleset` between the two bundled files shows them as modified on the `description` field only, and the test suite pins that.

---

## `applies_from`

The six new rules carry `applies_from: 2026-12-02`. The screener appends "The prohibition applies from 2 December 2026." to the rationale of a triggered 5.1.ba or 5.1.bb category, and every citation list includes "Art. 113(a), as amended by Regulation (EU) 2026/1744 (applies from 2 December 2026)". A report run before that date therefore states the date; the verdict is not suppressed, because the facts it reports are the facts a provider must fix before the date.

---

## Known Interpretive Weaknesses

1. **Self-declaration dependency** (unchanged from v1.0): the rules read `system.yaml` and cannot detect an undeclared capability or an overstated safeguard.
2. **"Reasonable and adequate" is not measured.** The `safeguards` flags say a measure exists and is documented, not that it meets the state of the art or reliably prevents the output. External review of a provider's safety case is outside the tool.
3. **Provider and deployer are not distinguished in the rules.** The `intimate_depictions_intended` flag covers both the provider's intended purpose (Art. 5(1a)(a)(i)) and the deployer's purpose (Art. 5(1a)(b)). A deployer using a lawful, safeguarded system for an unlawful purpose must declare that purpose for the rule to fire.
4. **Directive 2011/93/EU not read.** The (bb) rules rely on the plain meaning of "child sexual abuse material"; the Directive's definitions and the national "without right" defences were not reviewed.
5. **No semantic analysis of `purpose` or `system_description`** (unchanged). `--describe` keyword inference is heuristic.
6. **Medical and try-on cases.** Recital 12 excludes applications where intimate parts are not exposed or exposure is consented (try-on, medical simulation) and allows exceptional medical use without consent. The rules reach the consented case through `consent_demonstrable` and the no-exposure case through `intimate_depictions_possible: false`; the emergency medical exception is not modelled and would read Red. A reviewer must handle it.

---

## Acknowledgment

This review was conducted by AiExponent's internal compliance panel. **It is not legal advice. It has not been reviewed by a qualified EU AI Act lawyer. It does not constitute a certification of any kind.** Organisations requiring legal certainty should have qualified counsel review the ruleset via the BYO-ruleset path documented in `docs/ruleset-authoring.md`.

---

*Signed off by AiExponent Internal Panel (v2), 2026-10-31*
