# Internal Ruleset Review Record

**Ruleset version:** `ruleset-2024-1689-v1.2`
**Regulation:** Regulation (EU) 2024/1689 (EU AI Act), as amended by Regulation (EU) 2026/1744 (Digital Omnibus on AI)
**Review date:** 2026-11-03
**Status:** Internal panel review, NOT external legal review
**Supersedes:** `internal-review-record-2024-1689-v1.1.1.md` for the rules listed below. The v1.0, v1.1 and v1.1.1 records stay in the package and remain the record for every rule not listed here.

---

## Why this revision

The independent test of litmus-screener 1.1.2 and 1.1.3 (`verification/REPORT.md` in the source repository) found two gaps.

- Points (a) and (b) could not be detected from their legal elements: 6 of 51 expected prohibitions screened clear.
- The exceptions and limits written in Article 5(1), points (d) to (h), were not modelled, and they caused most of the 32 false alarms.

This revision adds a question for each missing element. The panel saw the test results before writing the rules. The questions were written from the Article text, not tuned case by case, but a re-test of this revision is weaker evidence than the first run.

## Source

Regulation (EU) 2024/1689, Article 5(1), read at the Publications Office Cellar on 2026-11-03. The English XHTML copy is byte-identical to the copy read on 2026-11-02. Every claim below about what the Regulation says was checked against that text on that date. The rule expressions are the panel's interpretation and have not been checked by a lawyer.

## Design decisions (founder, 2026-11-03)

1. **Answers.** Each question is answered `yes`, `no`, `not_sure` or `not_answered` (the default). An unquoted YAML `yes` or `no` is accepted.
2. **Old files keep their verdicts.** Every existing rule keeps its whole v1.1.1 condition and gains only a condition on a new field. A file that leaves the new fields at `not_answered` gets exactly the v1.1.1 verdict on every point. This was checked on 195 declarations (the 175 test cases, the examples and the test fixtures): 0 verdict changes. Points (a) and (b) report low confidence while their questions are unanswered.
3. **Facts versus claims.** A fact that takes a system outside a prohibition clears it. An exception that needs evidence gives AMBER, so a reviewer checks it.

## What changed from v1.1.1

| Change | Rules |
|--------|-------|
| Added (a) | `rule_a_elements_declared` (RED), `rule_a_elements_not_sure` (AMBER), `rule_a_questions_not_answered` (CLEAR, low confidence) |
| Added (b) | `rule_b_elements_declared` (RED), `rule_b_elements_not_sure` (AMBER), `rule_b_questions_not_answered` (CLEAR, low confidence) |
| Added (d), (f), (g), (h) | `rule_d_human_assessment_claimed`, `rule_f_medical_or_safety_claimed`, `rule_g_labelling_claimed`, `rule_h_objective_claimed` (all AMBER) |
| Condition added | the six (a) and (b) proxy rules: apply only while their questions are unanswered |
| Condition added | `rule_d_criminal_risk`; both (e) rules; all four (f) rules; the two RED (g) rules; all three (h) rules |
| Metadata | `ruleset_version` |

Every added or changed rule carries `reviewed_by: aiexponent-internal-panel-v2` and `reviewed_date: 2026-11-03`; each changed rule's `version` goes up by one.

---

## Per-category sign-off

### 5.1.a: Harmful manipulation

Article 5(1)(a) requires all of these:
- an AI system that "deploys subliminal techniques beyond a person's consciousness or purposefully manipulative or deceptive techniques";
- "with the objective, or the effect of materially distorting the behaviour" of a person or group, "by appreciably impairing their ability to make an informed decision";
- "in a manner that causes or is reasonably likely to cause ... significant harm".

The questions follow those three elements. `subliminal_techniques` and `manipulative_or_deceptive_techniques` are alternatives.

- `rule_a_elements_declared`: RED when a technique, material distortion and significant harm are all `yes`. **Approved.**
- `rule_a_elements_not_sure`: AMBER when a technique is `yes` or `not_sure` and neither distortion nor harm is `no`. **Approved.**
- `rule_a_questions_not_answered`: CLEAR with low confidence when both technique questions are `not_answered`. It states the gap and does not change the verdict. **Approved.**
- **Panel note:** the 1.1 proxy rules (emotional-state inference with behaviour prediction) stay for unanswered files only, so answering the questions replaces them.

### 5.1.b: Exploitation of vulnerabilities

Article 5(1)(b) requires all of these:
- an AI system that "exploits any of the vulnerabilities of a natural person or a specific group of persons due to their age, disability or a specific social or economic situation";
- with the objective or effect of materially distorting behaviour;
- likely to cause significant harm.

`exploits_vulnerability` carries the first element. The other two are shared with (a). The new population category `older_persons` records older age, which the 1.1 categories lacked.

- `rule_b_elements_declared` (RED), `rule_b_elements_not_sure` (AMBER), `rule_b_questions_not_answered` (CLEAR, low confidence): the same pattern as (a). **Approved.**

### 5.1.d: Criminal risk prediction

The second half of point (d) reads: "this prohibition shall not apply to AI systems used to support the human assessment of the involvement of a person in a criminal activity, which is already based on objective and verifiable facts directly linked to a criminal activity". The exclusion needs evidence.

- `rule_d_human_assessment_claimed`: AMBER when it is declared `yes`. `rule_d_criminal_risk` stays RED otherwise, including for `not_sure`. **Approved.**

### 5.1.e: Untargeted facial image scraping

Point (e) covers systems "that create or expand facial recognition databases through the untargeted scraping of facial images from the internet or CCTV footage". Targeted collection, and collection that builds no recognition database, are outside the point.

- Both (e) rules apply only when neither `untargeted_collection` nor `builds_facial_recognition_database` is `no`. **Approved.**

### 5.1.f: Emotion inference in workplace and education

Point (f) covers inferring "emotions of a natural person in the areas of workplace and education institutions, except where the use of the AI system is intended to be put in place or into the market for medical or safety reasons". The Commission guidelines (C(2025) 5052, paras. 254 and 255, read 2026-11-03) treat employees and job candidates in the workplace, and pupils and students in education institutions, as within the point, and say that tracking customers' emotions in a call centre is not prohibited by point (f).

- All four (f) rules apply only when `emotions_of_workers_or_students` is not `no`.
- The two RED rules also step aside when `medical_or_safety_reasons` is `yes`. `rule_f_medical_or_safety_claimed` then gives AMBER.
- **Approved.**
- **Panel note:** `deployment_context.workplace` keeps its 1.1 meaning: where the system runs.

### 5.1.g: Biometric categorisation of sensitive attributes

Point (g) "does not cover any labelling or filtering of lawfully acquired biometric datasets ... or categorizing of biometric data in the area of law enforcement".

- The two RED rules step aside when `dataset_labelling_or_filtering_only` is `yes`. `rule_g_labelling_claimed` gives AMBER. **Approved.**

### 5.1.h: Real-time remote biometric identification

Point (h) prohibits "the use of 'real-time' remote biometric identification systems in publicly accessible spaces for the purposes of law enforcement, unless and in so far as such use is strictly necessary" for one of the objectives in (i) to (iii). It covers use only.

- The three (h) rules apply only when all of these hold:
  - `role` is not `provider_only`;
  - `remote_identification` is not `no`;
  - `law_enforcement_purpose` is not `no`.
- The RED rules also step aside when `article_5_1_h_objective` is `yes`. `rule_h_objective_claimed` then gives AMBER and cites Article 5(2) and 5(3) (authorisation, fundamental rights impact assessment, registration).
- **Approved.**
- **Panel note:** the new `law_enforcement_purpose` is used instead of `deployment_context.law_enforcement_use`, because the latter defaults to false in every existing file and would have cleared them.

---

## Known Interpretive Weaknesses

1. **Self-declaration dependency** (unchanged): every answer, including a claimed exception, is the declarant's. The tool cannot check it, so claimed exceptions give AMBER, not CLEAR.
2. **Not modelled in v1.2:**
   - (c) relevance and proportionality under sectoral law;
   - (ba) and (bb) accidental generation, emergency medical use and the "without right" defence for red-teaming, which appear in the recitals of Regulation (EU) 2026/1744;
   - (f) emotion recognition used only for a person's own training.
3. **Overfitting risk:** the panel saw the 1.1.x test results. The questions follow the Article text, and the re-test report must say so.
4. **Quick screen:** `--describe` does not answer the new questions, so it keeps the 1.1 behaviour with low confidence on (a) and (b).

---

## Acknowledgment

This review was conducted by AiExponent's internal compliance panel. **It is not legal advice. It has not been reviewed by a qualified EU AI Act lawyer. It does not constitute a certification of any kind.**

---

*Signed off by AiExponent Internal Panel (v2), 2026-11-03*
