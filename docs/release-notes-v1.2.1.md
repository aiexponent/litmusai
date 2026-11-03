# LitmusAI 1.2.1

Clearer questions in `system.yaml`. Reference ruleset `ruleset-2024-1689-v1.2`, unchanged (UNREVIEWED: internal panel authored, no external lawyer review). Apache 2.0, AS IS. Not legal advice. Not a notified body.

## Changed

- **The template asks factual questions only.** The `litmus init` template no longer says what an answer does to a verdict. That is documented in the README, in the "Article 5 Categories Covered" table. The blind re-test of 1.2.0 found that the old notes could steer people towards the answer that gives the verdict they want.
- **Guidance for every new question,** following the Commission's guidelines (C(2025) 5052) and the Regulation's definitions:
  - manipulation counts even when nobody intended it;
  - intent is not needed for the distortion of behaviour;
  - other weak points belong under the techniques question;
  - which people count as workers or students for point (f);
  - what law enforcement means;
  - the three objectives of point (h), written out.

Nothing else changed. Rules, verdicts, report schema and CLI surface are those of 1.2.0, and existing `system.yaml` files need no change.

## Upgrade

```bash
pip install --upgrade litmus-screener==1.2.1
litmus --version
```

Requires Python 3.11 or newer. Installing needs a package index; screening makes no network calls. Full details in `CHANGELOG.md`.
