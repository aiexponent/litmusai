# LitmusAI 1.2.0

Questions for points (a) and (b), and the exceptions written in Article 5(1). Reference ruleset `ruleset-2024-1689-v1.2` (UNREVIEWED: internal panel authored, no external lawyer review). Apache 2.0, AS IS. Not legal advice. Not a notified body.

## Why

The independent test of 1.1.2 and 1.1.3 on 175 worked examples from the Commission's guidelines (`verification/REPORT.md`) found two gaps:

- **6 missed prohibitions, all on points (a) and (b).** `system.yaml` had no field for their legal elements.
- **32 false alarms out of 113 permitted cases.** Most came from exceptions and limits the declaration could not express.

## Added

- **`influence` block for points (a) and (b).** One question per legal element:
  - a subliminal, or purposefully manipulative or deceptive, technique;
  - exploitation of a vulnerability due to age, disability or a specific social or economic situation;
  - material distortion of behaviour;
  - likely significant harm.

  Answer `yes`, `no` or `not_sure`. For each point, all `yes` is RED; a `not_sure` on any element, with no element answered `no`, is AMBER; a `no` on any element clears it.
- **`scope` block for the exceptions and limits in points (d) to (h).** A fact that takes a system outside a point clears it:
  - only customers' or patients' emotions;
  - targeted collection;
  - not for law enforcement;
  - not remote;
  - selling the system without using it.

  A claimed exception that needs evidence gives AMBER for a reviewer:
  - human assessment on verifiable facts;
  - medical or safety reasons;
  - dataset labelling;
  - the (h)(i) to (iii) objectives.
- `older_persons` as a population category.

## Your existing files

A `system.yaml` written for 1.1.x keeps every verdict. Its (a) and (b) results now report low confidence and say that the questions are unanswered. Run `litmus init -o new.yaml` to see the new blocks, then add the answers that apply to your system. `litmus verify` still verifies reports written by 1.0.x and 1.1.x.

## Limits

Every answer is self-declared, and LitmusAI cannot check that a claimed exception holds. These cases are still not modelled:
- (c) proportionality;
- (ba) and (bb) accidental generation, emergency medical use and the red-teaming defence;
- emotion recognition used only for a person's own training.

The quick screen (`--describe`) does not answer the new questions.

The independent test will be re-run on 1.2.0 and published in `verification/`. The rules author saw the earlier results, so that re-test is weaker evidence than the first run.

## Upgrade

```bash
pip install --upgrade litmus-screener==1.2.0
litmus --version
```

Requires Python 3.11 or newer. Installing needs a package index; screening makes no network calls. Full details in `CHANGELOG.md`.
