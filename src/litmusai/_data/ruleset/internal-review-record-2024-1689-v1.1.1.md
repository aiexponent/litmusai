# Internal Ruleset Review Record

**Ruleset version:** `ruleset-2024-1689-v1.1.1`
**Regulation:** Regulation (EU) 2024/1689 (EU AI Act), as amended by Regulation (EU) 2026/1744 (Digital Omnibus on AI)
**Review date:** 2026-11-02
**Status:** Internal panel review, NOT external legal review
**Supersedes:** `internal-review-record-2024-1689-v1.1.md` (2026-10-31) for the citations listed below. That record and `internal-review-record-2024-1689-v1.0.md` stay in the package and remain the record for every rule expression and verdict.

---

## What changed from v1.1

Recital citations only. No expression, verdict, confidence or `applies_from` changed, so no screening verdict can differ from v1.1. `litmus diff-ruleset` between the two bundled files shows the eleven rules below as modified on `citations`, `version`, `reviewed_by` and `reviewed_date`, and the test suite pins that.

| Rule | v1.1 cited | v1.1.1 cites | Why |
|------|-----------|--------------|-----|
| `rule_a_subliminal_inputs` | Recitals 29, 30 | Recital 29 | Recital 30 is about biometric categorisation, point (g) |
| `rule_a_freetext_manipulation` | Recital 31 | Recital 29 | Recital 31 is about social scoring, point (c) |
| `rule_b_targets_minors` | Recitals 29, 32 | Recital 29 | Recital 32 is about real-time remote biometric identification, point (h). Recital 29 covers exploitation of vulnerabilities |
| `rule_b_vulnerable_population` | Recital 32 | Recital 29 | As above |
| `rule_b_targets_minors_freetext` | Recital 32 | Recital 29 | As above |
| `rule_c_social_scoring` | Recitals 31, 33 | Recital 31 | Recital 33 is about point (h) |
| `rule_c_scoring_from_scraped_data` | Recital 33 | Recital 31 | As above |
| `rule_e_untargeted_facial_scraping` | Recital 42 | Recital 43 | Recital 42 is about crime risk prediction, point (d). Recital 43 is the scraping recital |
| `rule_e_facial_from_cctv` | Recital 42 | Recital 43 | As above |
| `rule_g_biometric_sensitive_classification` | Recital 44 | Recital 30 | Recital 44 is about emotion recognition, point (f). Recital 30 is the biometric categorisation recital |
| `rule_g_facial_sensitive_classification` | Recital 44 | Recital 30 | As above |

The same citations were wrong in v1.0. Each changed rule's `version` goes up by one.

## How the error was found

The independent verification run of 2 November 2026 (PRD-274, `verification/` in the source repository) lists every citation in every report. Each recital cited was then read against the text of Regulation (EU) 2024/1689 (OJ L, 12.7.2024) at the Publications Office Cellar on 2026-11-02. Correct as cited, and unchanged: point (a) Recital 29, (c) Recital 31, (d) Recital 42, (f) Recital 44, (h) Recital 33 with Article 5(2) and 5(3), and the (ba) and (bb) citations of Regulation (EU) 2026/1744, recitals 12 and 13.

## Guard against a repeat

`tests/unit/test_ruleset_citations.py` holds a map from each Article 5(1) point to the recitals about it and fails if a shipped rule cites a recital outside that map, or an `Art. 5(1)(x)` point other than its own. Run against the v1.1 file, it fails on exactly the eleven rules above.

---

## Acknowledgment

This review was conducted by AiExponent's internal compliance panel. **It is not legal advice. It has not been reviewed by a qualified EU AI Act lawyer. It does not constitute a certification of any kind.**

---

*Signed off by AiExponent Internal Panel (v2), 2026-11-02*
