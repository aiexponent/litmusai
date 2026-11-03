# LitmusAI independent test: report

**Date of the runs:** 2 November 2026
**Package tested:** litmus-screener 1.1.2 (first run) and 1.1.3 (re-run), installed from PyPI by version and hash
**Reference ruleset:** `ruleset-2024-1689-v1.1` (1.1.2) and `ruleset-2024-1689-v1.1.1` (1.1.3). The two differ only in recital citations, and every verdict is the same on both.
**Cases:** 175 worked examples, each with an expected answer written down before the first screen ran

LitmusAI is a screening aid. Neither the tool nor this test is a legal opinion, a conformity assessment or a certification. The expected answers come from the European Commission's Guidelines on prohibited AI practices, which say of themselves: "These Guidelines are non-binding. Any authoritative interpretation of the AI Act may ultimately only be given by the Court of Justice of the European Union" (C(2025) 5052 final, page 1, paragraph 5).

## Summary

Full screen of each `system.yaml`:

| | Count |
|---|---|
| Expected prohibitions found (red) | 44 of 51 |
| Flagged for review (amber) | 1 of 51 |
| Missed (clear) | 6 of 51, all on points (a) and (b) |
| Permitted cases screened red (false alarms) | 32 of 113 |
| Permitted cases screened amber (over-caution) | 23 of 113 |
| Permitted cases screened clear | 58 of 113 |

What this means for a user:

- **Points (a) and (b) cannot be screened from their legal elements.** `system.yaml` has no field for manipulative, deceptive or subliminal techniques, for significant harm, or for exploiting a vulnerability other than being a minor. Check those two points yourself.
- **Exceptions and scope limits are mostly not modelled.** 32 permitted cases screened red because a rule tests the capability (emotion inference at work, real-time biometric identification in a public space, crime risk prediction) and not the condition that takes the case outside the prohibition. A red verdict means "a reviewer must look", not "prohibited".
- **On points (c) to (h), (ba) and (bb), no expected prohibition screened clear.** One (bb) case screened amber.

## Method

The full method is in `README.md` and `SELECTION.md` in this folder. In short:

1. `SELECTION.md` fixed the rule for choosing cases before any case was written. It takes every worked example in chapters 3 to 9 of the guidelines that states a conclusion, plus every example in recitals 12 to 14 of Regulation (EU) 2026/1744 for points (ba) and (bb). The guidelines were published in July 2025, before those two points existed.
2. A tester who had not read the ruleset wrote each case, its expected answer and its `system.yaml`, in that order, and committed each stage before the next. The git history shows the order. The separation is procedural: the package on PyPI contains the ruleset, and the tester agreed not to open it.
3. `run.sh` installs the released package in a clean container, screens every declaration twice, exports SARIF and scores the verdicts. Anyone can repeat it with one command.

Expected answers have not been changed since they were committed.

### How amber counts

These rules were fixed before any result existed.

- **Flagged for review:** expected red, got amber. Counted apart from hits and misses, because amber tells the user to get a review but does not say "prohibited".
- **Over-caution:** expected clear, got amber. The ruleset prefers amber when a declaration leaves a question open, so some of this is by design. It is reported, not hidden.
- **Expected amber:** 11 cases where the guidelines say the answer depends on facts the example does not give. They are in the per-point table only and are not counted as hits, misses or alarms.

## Results by point

Full screen of `system.yaml`.

| Point | Expected red: found / flagged / missed | Expected clear: clear / amber / red | Expected amber: got red / amber / clear |
|---|---|---|---|
| (a) | 0 / 0 / 3 | 12 / 0 / 0 | 0 / 0 / 2 |
| (b) | 1 / 0 / 3 | 9 / 2 / 0 | 0 / 0 / 1 |
| (ba) | 5 / 0 / 0 | 5 / 4 / 2 | none |
| (bb) | 3 / 1 / 0 | 1 / 2 / 2 | none |
| (c) | 10 / 0 / 0 | 4 / 7 / 1 | 1 / 3 / 0 |
| (d) | 3 / 0 / 0 | 7 / 0 / 7 | 2 / 0 / 0 |
| (e) | 2 / 0 / 0 | 3 / 0 / 3 | none |
| (f) | 14 / 0 / 0 | 7 / 6 / 8 | none |
| (g) | 4 / 0 / 0 | 7 / 1 / 2 | none |
| (h) | 2 / 0 / 0 | 3 / 1 / 7 | 1 / 0 / 1 |
| All | 44 / 1 / 6 | 58 / 23 / 32 | 4 / 3 / 4 |

## Every missed prohibition

| Case | Source | What the case describes | Why LitmusAI screened it clear |
|---|---|---|---|
| a-01 | Guidelines p. 20, para. 66 | A game uses a brain-computer interface to draw sensitive data out of players without their knowledge | The declaration has no field for covert, manipulative or subliminal techniques. The one red rule for (a) needs both emotional-state inference and behaviour prediction, and this system does neither. |
| a-06 | Guidelines p. 25, para. 82 | A chatbot shows ads with subliminal visual and audio cues to steer purchases | Same as a-01 |
| a-08 | Guidelines p. 26, para. 84 | A well-being chatbot pushes users into dangerous habits | Same as a-01. There is also no field for significant harm. |
| b-01 | Guidelines p. 33, para. 105 | A toy urges children into risky physical challenges for rewards | The red rule for (b) needs minors together with behaviour prediction. The declaration names minors but has no behaviour prediction, and no field says the system exploits them. |
| b-03 | Guidelines p. 34, para. 106 | A system targets older people with deceptive offers and scams | Older age is not a population category, and there is no field for exploiting a vulnerability |
| b-04 | Guidelines p. 34, para. 106 | An assistive robot forces older people into activities against their will | Same as b-03 |

## Flagged for review

| Case | Source | What the case describes | What LitmusAI did |
|---|---|---|---|
| bb-05 | Reg. 2026/1744, recital 12 | A user works around the safeguards of a general-purpose image generator to make sexual images of a child | Amber from `rule_bb_no_csam_safeguards`. The declaration describes the generator, which has safeguards. There is no field for a deployer who circumvents them, which recital 12 places inside the prohibition. |

## Every false alarm

Expected clear, screened red. The cause is the condition the guidelines or recital rely on to clear the case, which no rule tests.

| Case | Source | What the case describes | Condition the rules do not test |
|---|---|---|---|
| ba-07 | Reg. 2026/1744, recital 12 | An ordinary image request accidentally returns an intimate depiction of an identifiable person | Accidental generation is excluded from the prohibition on use. The rules screen the system's capability and safeguards, not one output. |
| ba-14 | Reg. 2026/1744, recital 12 | Emergency medical imaging of an unconscious patient | The medical exception without consent. This was listed as a known weakness in the v1.1 review record. |
| bb-07 | Reg. 2026/1744, recital 12 | An ordinary image request accidentally returns material that could involve a child | Accidental generation, as in ba-07 |
| bb-09 | Reg. 2026/1744, recital 13 | Legitimate red-teaming of an image model under a national "without right" defence | The defence is reachable only through `law_enforcement_use`. Red-teaming has no field. |
| c-26 | Guidelines p. 60, para. 177 | Police score individuals with crime-relevant data, proportionately under criminal law | Relevance and proportionality of the data to the purpose |
| d-05 | Guidelines p. 68, para. 209 | A bank's anti-money-laundering profiling as required by EU law | `rule_d_criminal_risk` fires on any crime risk prediction. It does not test the exclusion for systems that support a human assessment based on objective, verifiable facts, or use under a specific law. |
| d-10 | Guidelines p. 70, para. 214 | Flagging suspicious behaviour in a crowd, each flag assessed by a human | Same as d-05 |
| d-11 | Guidelines p. 70, para. 214 | Police combine data on two suspects identified from verifiable facts | Same as d-05 |
| d-12 | Guidelines p. 70, para. 214 | Support for an early-release decision based on verifiable facts | Same as d-05 |
| d-13 | Guidelines p. 70, para. 214 | A risk tool supporting a judge at a pre-trial detention hearing | Same as d-05 |
| d-14 | Guidelines p. 71, para. 214 | Support for a probation officer's assessment | Same as d-05 |
| d-15 | Guidelines p. 71, para. 214 | Customs risk assessment of goods and traders | Same as d-05 |
| e-01 | Guidelines p. 75, para. 230 | Crawlers collect images of one class of trafficking victims | "Untargeted": the red rule fires on facial images plus scraped internet data |
| e-04 | Guidelines p. 75, para. 233 | A reverse image search for one person's face | "Untargeted", and whether a database is created or expanded |
| e-08 | Guidelines p. 76, para. 235 | Scraped faces used to train a generator of fictitious people | Purpose: the prohibition covers facial recognition databases, and this system recognises no one |
| f-07 | Guidelines p. 81, para. 254 | Employees use emotion recognition for their own training, with no effect on their assessment | `rule_f_workplace_emotion` fires on emotion inference in any workplace. It does not test whose emotions are inferred, or whether the result can affect the work relationship. |
| f-08 | Guidelines p. 81, para. 254 | A call centre tracks customers' emotions, not employees' | Same as f-07 |
| f-13 | Guidelines p. 82, para. 254 | Shop or bank cameras watch customers, with no employee tracked | Same as f-07 |
| f-19 | Guidelines p. 82, para. 255 | Role-play training with no effect on evaluation or certification | Same as f-07, for education |
| f-25 | Guidelines p. 84, para. 263 | Emotion recognition for medical reasons, to assist people with autism or sensory impairments | The exception for medical or safety reasons. `rule_f_emotion_healthcare_exception` gives amber, but the workplace and education rules give red, and red wins. |
| f-28 | Guidelines p. 84, para. 263 | Stress monitoring of workers at dangerous machines, used only for safety | The exception for medical or safety reasons. No rule tests a safety purpose. |
| f-33 | Guidelines p. 85, para. 269 | A doctor uses emotion recognition on a patient during an examination | Same as f-25. The practice is a workplace, but the person analysed is the patient. |
| f-35 | Guidelines p. 86, para. 270 | Crowd aggression detection at a stadium, with safeguards so staff are not screened | Same as f-07 |
| g-11 | Guidelines p. 89, para. 283 | DNA analysis of crime victims to determine their origin | The guidelines' reason this is not prohibited. The rule fires on biometric input plus a sensitive-attribute output. |
| g-12 | Guidelines p. 90, para. 285 | Labelling biometric training data by ethnic group to correct bias | The exception for labelling or filtering lawfully acquired biometric datasets |
| h-01 | Guidelines p. 91, para. 291 | A provider places a real-time identification system on the market and does not use it | Point (h) prohibits use only. The rules do not distinguish provider from deployer. |
| h-05 | Guidelines p. 95, para. 306 | Passengers knowingly use a biometric gate | Remoteness |
| h-08 | Guidelines p. 99, para. 324 | A bank uses remote identification on its own behalf against fraud | Law-enforcement purpose. The red rules for (h) do not read `law_enforcement_use`. |
| h-10 | Guidelines p. 101, para. 332 | Police search for a kidnapped child in a defined area and time | The exceptions in Article 5(1)(h)(i) to (iii). The amber exception rule fires too, but red wins. |
| h-11 | Guidelines p. 101, para. 336 | An administrative search for a missing vulnerable person | Law-enforcement purpose, as in h-08 |
| h-14 | Guidelines p. 106, para. 354 | Police look for one person wanted on a European Arrest Warrant | Same as h-10 |
| h-15 | Guidelines p. 106, para. 354 | Police track the attacker after a terror attack | Same as h-10 |

## Over-caution and off-target findings

**Over-caution (23 cases):** b-10, b-15, ba-10, ba-12, ba-13, ba-15, bb-06, bb-08, c-06, c-18, c-19, c-20, c-22, c-24, c-25, f-05, f-14, f-29, f-31, f-32, f-34, g-01, h-06. These are permitted cases that screened amber. The amber rules fire on a capability, such as any individual scoring or any emotion inference, so that a reviewer sees it. That is the intended behaviour, but it adds review work.

**Off-target red (1 case):** d-03, a police tool that scores children's future criminality partly from their links to other children, with more police checks as a result. Point (d), the target, screened red as expected. Point (c) also screened red, because the declaration sets individual scores from social behaviour data. The guidelines discuss the case under point (d) only. It is listed here and not counted as a hit or an error.

## Quick screen (`--describe`)

The same 175 descriptions were screened with `litmus screen --describe`, which infers a declaration from keywords and marks its confidence as lower. Results:

- 27 of 51 expected prohibitions missed
- 6 flagged for review
- 20 false alarms
- 13 over-caution
- 5 off-target reds

The full lists are in `scorecard.md`. The quick screen is a first look, not a substitute for a `system.yaml`.

## Checks beyond verdicts

- **Repeatability.** Every case was screened twice in each run, and the two reports matched apart from `generated_at`. The 1.1.2 verdicts were the same in three environments: the tester's virtual environment, the CI container and a local run. The 1.1.3 verdicts matched them on every case.
- **SARIF.** Every report was exported to SARIF and validated against the structure of the OASIS SARIF 2.1.0 schema, pinned by SHA-256. String formats such as URIs and dates are not checked. All 175 passed.
- **Article citations.** Every `Art. 5(1)(x)` citation names the point it sits under, in both versions.
- **Recital citations.** Every recital cited was read against Regulation (EU) 2024/1689 at the Publications Office on 2 November 2026. In 1.1.2, eleven rules cited a recital about another point (42 citations across the 175 reports). 1.1.3 corrects them, and the harness and the package's tests now fail on any such citation.

## Limits of this test

- **The answers are the Commission's reading, not a court's.** The guidelines are non-binding.
- **One tester wrote every declaration.** Another person could set different flags for the same description. The results measure the tool on this reading of the `litmus init` template.
- **Worked examples are short and clean.** Real systems are described at more length and less clearly. The mix of cases (51 prohibited, 113 permitted, 11 open) follows the guidelines, not real-world use. The counts are therefore not detection rates for real deployments.
- **The two newest points rest on recitals alone.** For (ba) and (bb) the cases come from the recitals of Regulation (EU) 2026/1744, because the guidelines predate those points. Both points apply from 2 December 2026.
- **Expected labels follow the source's own words.** Where a passage said "likely" or "would normally", the case was read as red. Each case file gives the reason.

## What happens next

The missing fields for points (a) and (b), and the exceptions and scope limits listed above, are planned for a later minor release. When it ships, this test is re-run on it and this report is re-published. `run.sh` exits 1 whenever the verdicts differ from `results.csv`, so a changed result cannot go unnoticed.

## Reproduce

```bash
git clone https://github.com/aiexponent/litmusai.git
cd litmusai
verification/run.sh
```

Exit 0 means the verdicts match `results.csv`. `README.md` in this folder lists the options and exit codes.
