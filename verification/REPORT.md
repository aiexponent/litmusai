# LitmusAI independent test: report

**Package tested:** litmus-screener 1.2.0, installed from PyPI by version and hash
**Reference ruleset:** `ruleset-2024-1689-v1.2`
**Date of the run:** 3 November 2026
**Cases:** the same 175 worked examples as the first run, with expected answers written before any screen ran
**Earlier result:** litmus-screener 1.1.2 and 1.1.3, 2 November 2026, in `history/1.1.3/` (report, results and scorecard)

LitmusAI is a screening aid. Neither the tool nor this test is a legal opinion, a conformity assessment or a certification. The expected answers come from the European Commission's Guidelines on prohibited AI practices, which say of themselves: "These Guidelines are non-binding. Any authoritative interpretation of the AI Act may ultimately only be given by the Court of Justice of the European Union" (C(2025) 5052 final, page 1, paragraph 5).

## Summary

Full screen of each `system.yaml`:

| | 1.2.0 | 1.1.x |
|---|---|---|
| Expected prohibitions found (red) | 49 of 51 | 44 of 51 |
| Flagged for review (amber) | 2 of 51 | 1 of 51 |
| Missed (clear) | 0 of 51 | 6 of 51 |
| Permitted cases screened red (false alarms) | 9 of 113 | 32 of 113 |
| Permitted cases screened amber (over-caution) | 29 of 113 | 23 of 113 |
| Permitted cases screened clear | 75 of 113 | 58 of 113 |

What changed for a user:

- **Points (a) and (b) are now screened from their legal elements.** Version 1.2.0 asks one question per element. With the tester's answers, no expected prohibition screened clear.
- **Most false alarms became clear or amber.** The new `scope` questions carry the exceptions and limits written in Article 5(1). Facts that put a case outside a point clear it. Claimed exceptions that need evidence give amber, which is why over-caution rose from 23 to 29.
- **Nine false alarms remain,** and each has a stated cause below. A red verdict still means "a reviewer must look", not "prohibited".

**Read these results with three cautions** (details under "How this run differs from the first"):
- the author of the 1.2.0 rules saw the first run's results;
- the template's comments tell a user what each answer does to the verdict;
- the answers depend on how one tester read short descriptions.

## Method

The first run's method is unchanged (`README.md`, `SELECTION.md`, `history/1.1.3/REPORT.md`): the same cases, the same expected answers and the same declarations.

For this run, a tester in a separate session added answers to the two new blocks, `influence` and `scope`, to each declaration. The tester worked from each case's "Description" and "Source" sections and the template that `litmus init` writes. The tester was told not to open:
- the rules or the code;
- the first run's report, results and scorecard;
- the README sections that describe the rules;
- the expected labels.

The answers were committed (`06e66d2`) before any screen ran, and the run was committed after (`b098aee`). No existing field of any declaration changed. The tester's raw output and notes are in `retest-1.2.0/`.

### How amber counts

Unchanged from the first run:
- **Expected red, got amber:** flagged for review, counted apart from hits and misses.
- **Expected clear, got amber:** over-caution.
- **Expected amber:** the 11 cases where the source leaves the answer open appear only in the per-point table.

### How this run differs from the first

- **The rules author saw the first results.** The 1.2.0 questions were written from the Article text, not tuned case by case, but this run is weaker evidence than the first.
- **The template states what each answer does.** Comments such as "no: clears" and "yes: amber" tell a user what each answer does to the verdict. The tester named this as a finding: it could steer how people answer.
- **The tester saw the release commit message.** After the answers were written and checked, but before they were committed, the tester saw the message of the 1.2.0 release commit, which summarises the release. The answers were not changed (`retest-1.2.0/NOTES.md`).
- **Most non-(a)/(b) cases left `influence` unanswered.** The brief asked for all five `influence` questions on every case. For cases outside points (a) and (b), the tester left the technique questions at `not_answered`, so those cases report low confidence on (a) and (b). No verdict depends on this.

## Results by point

Full screen of `system.yaml` on 1.2.0.

| Point | Expected red: found / flagged / missed | Expected clear: clear / amber / red | Expected amber: got red / amber / clear |
|---|---|---|---|
| (a) | 2 / 1 / 0 | 12 / 0 / 0 | 0 / 2 / 0 |
| (b) | 4 / 0 / 0 | 10 / 1 / 0 | 0 / 1 / 0 |
| (ba) | 5 / 0 / 0 | 5 / 4 / 2 | none |
| (bb) | 3 / 1 / 0 | 1 / 2 / 2 | none |
| (c) | 10 / 0 / 0 | 4 / 7 / 1 | 1 / 3 / 0 |
| (d) | 3 / 0 / 0 | 7 / 6 / 1 | 2 / 0 / 0 |
| (e) | 2 / 0 / 0 | 6 / 0 / 0 | none |
| (f) | 14 / 0 / 0 | 16 / 3 / 2 | none |
| (g) | 4 / 0 / 0 | 7 / 2 / 1 | none |
| (h) | 2 / 0 / 0 | 7 / 4 / 0 | 0 / 1 / 1 |
| All | 49 / 2 / 0 | 75 / 29 / 9 | 3 / 7 / 1 |

## Missed prohibitions

None. The six cases missed by 1.1.x (a-01, a-06, a-08, b-01, b-03, b-04) now screen red, except a-08, which is flagged.

## Flagged for review

| Case | Source | What the case describes | Why amber, not red |
|---|---|---|---|
| a-08 | Guidelines p. 26, para. 84 | A well-being chatbot pushes users into dangerous habits | The tester answered `not_sure` to "purposefully manipulative or deceptive techniques", because the harm was not intended. Point (a) also covers techniques that have the effect of distorting behaviour, and the template does not say so (finding 2 below). |
| bb-05 | Reg. 2026/1744, recital 12 | A user works around the safeguards of a general-purpose image generator to make sexual images of a child | Unchanged from 1.1.x. There is no field for a deployer who circumvents safeguards. |

## Every false alarm

| Case | Source | What the case describes | Condition the rules do not test, or the answer that kept it red |
|---|---|---|---|
| ba-07 | Reg. 2026/1744, recital 12 | An ordinary image request accidentally returns an intimate depiction of an identifiable person | Accidental generation. Not modelled (stated limit). |
| ba-14 | Reg. 2026/1744, recital 12 | Emergency medical imaging of an unconscious patient | The medical exception without consent. Not modelled (stated limit). |
| bb-07 | Reg. 2026/1744, recital 12 | An ordinary image request accidentally returns material that could involve a child | Accidental generation. Not modelled (stated limit). |
| bb-09 | Reg. 2026/1744, recital 13 | Legitimate red-teaming under a national "without right" defence | Reachable only through `law_enforcement_use`. Not modelled (stated limit). |
| c-26 | Guidelines p. 60, para. 177 | Police score individuals with crime-relevant data, proportionately under criminal law | Relevance and proportionality under sectoral law. Not modelled (stated limit). |
| d-13 | Guidelines p. 70, para. 214 | A risk tool supporting a judge at a pre-trial detention hearing | The tester answered `not_sure` to the human-assessment question, because the tool also uses social behaviour and income. A `not_sure` keeps (d) red. |
| f-07 | Guidelines p. 81, para. 254 | Employees use emotion recognition only for their own training | Use with no effect on the work relationship. Not modelled (stated limit). |
| f-19 | Guidelines p. 82, para. 255 | Role-play training with no effect on evaluation | The same, for education. Not modelled (stated limit). |
| g-11 | Guidelines p. 89, para. 283 | DNA analysis of crime victims to determine their origin | The guidelines' reason this is not prohibited. Not modelled (stated limit). |

## Over-caution and off-target findings

**Over-caution (29 cases).** Each is a permitted case that screened amber:

| Cases | Why amber |
|---|---|
| d-05, d-10, d-11, d-12, d-14, d-15 | The (d) human-assessment exclusion was claimed. That needs evidence, so it is amber by design. |
| f-25, f-28 | Medical or safety reasons were claimed (amber by design). |
| g-12 | Dataset labelling was claimed (amber by design). |
| h-10, h-14, h-15 | An objective in Art. 5(1)(h)(i) to (iii) was claimed (amber by design). |
| b-07 | The tester answered `not_sure` to exploitation of a vulnerability. |
| ba-10, ba-12, ba-13, ba-15, bb-06, bb-08 | Unchanged from 1.1.x: generative-media review rules. |
| c-06, c-18, c-19, c-20, c-22, c-24, c-25 | Unchanged from 1.1.x: any individual scoring gives amber. |
| f-05 | Unchanged from 1.1.x: emotion inference outside work or education. |
| g-01 | Unchanged from 1.1.x: sensitive-attribute classification. |
| h-06 | Unchanged from 1.1.x: biometrics in a public space with law-enforcement use. |

**Off-target red (4 cases):**
- **b-01, b-02, b-03:** cases about children and older people, whose descriptions also describe manipulative techniques. The tester answered yes to them, so point (a) is red as well as the target (b). The guidelines discuss these cases under point (b) only.
- **d-03:** as in 1.1.x, (c) is also red.

These are listed, not counted as hits or errors.

## What the tester found unclear in the template

The tester reported ten points. They are open for a documentation fix in a later release:

1. The comment lists yes, no and not_sure, but not when to leave `not_answered`; and `influence` gives no guidance for systems unrelated to points (a) and (b).
2. "Purposefully" does not say that a technique counts when it has the effect, not only the objective, of distorting behaviour.
3. `exploits_vulnerability` does not say whether other weak points, such as emotional dependency, count.
4. `significant_harm_likely` does not say whether it means harm from distorted behaviour or any harm.
5. `role` has no value for a private person, and no guidance for an organisation that builds and uses a system.
6. `human_assessment_on_verifiable_facts` does not say whether a human must decide or only review.
7. `emotions_of_workers_or_students` does not say whether job candidates, applicants or trainees count, or what to answer when no emotion is inferred.
8. `remote_identification` gives one example only.
9. `article_5_1_h_objective` does not list the three objectives.
10. The "clears" and "amber" notes tell the user the effect of an answer, which can steer it.

## Quick screen (`--describe`)

The quick screen infers a declaration from the description's keywords and does not answer the new questions, so its result is unchanged from 1.1.x:
- 27 of 51 expected prohibitions missed;
- 6 flagged;
- 20 false alarms;
- 13 over-caution;
- 5 off-target reds.

## Checks beyond verdicts

- **Repeatability.** Every case was screened twice, and the two reports matched apart from `generated_at`. The run was repeated from `requirements.lock` (1.2.0, hash-pinned) in a separate environment and gave a byte-identical `results.csv`.
- **SARIF.** All 175 reports validated against the structure of the OASIS SARIF 2.1.0 schema.
- **Citations.** Every `Art. 5(1)(x)` citation names its own point. Every recital cited is about that point, checked against Regulation (EU) 2024/1689 as read on 2 November 2026.

## Limits of this test

- **The answers are the Commission's reading, not a court's.** The guidelines are non-binding.
- **One tester wrote every declaration and every answer.** The 1.2.0 answers depend on how that tester read short descriptions: a-08 and d-13 show a `not_sure` changing a result.
- **Worked examples are not real deployments.** The case mix follows the guidelines, so the counts are not detection rates for real systems.
- **(ba) and (bb) rest on recitals alone,** because the guidelines predate those points. Both apply from 2 December 2026.
- **Expected labels have not changed** since they were first committed.

## Reproduce

```bash
git clone https://github.com/aiexponent/litmusai.git
cd litmusai
verification/run.sh
```

Exit 0 means the verdicts match `results.csv`. `README.md` in this folder lists the options and exit codes.
