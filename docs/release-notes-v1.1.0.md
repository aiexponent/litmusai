# LitmusAI 1.1.0

Ruleset `ruleset-2024-1689-v1.1` (UNREVIEWED: internal panel authored, no external lawyer review). Apache 2.0, AS IS. Not legal advice. Not a notified body.

## Ten Article 5 categories

Regulation (EU) 2026/1744 (Digital Omnibus on AI) inserts two prohibitions into Article 5(1) of the EU AI Act, applicable from 2 December 2026:

- **5.1.ba** Non-consensual intimate material of identifiable persons.
- **5.1.bb** Child sexual abuse material.

`litmus screen` now returns a Red / Amber / Clear verdict for both, next to the original eight. Six new rules encode the Article 5(1a) intended-purpose and foreseeable-outcome tests, the safeguards test, the consent carve-out of point (ba), the Article 5(1b) manipulation carve-out, and the "without right" defence of point (bb). A report run before 2 December 2026 says that the prohibition applies from that date.

Declare the facts in the new `generative_media` block of `system.yaml` (`litmus init` writes it). Every field defaults to false, so existing files keep working.

## Social scoring fix (litmusai#25)

A credit score built from repayment history no longer reads Red for social scoring. `rule_c_social_scoring` now needs social behaviour data or detrimental treatment in an unrelated context, two new declaration fields. Plain individual scoring stays Amber for review.

## Also in this release

- Optional `applies_from` date on rules, shown by `litmus ruleset-info` and tracked by `litmus diff-ruleset`.
- A category the active ruleset has no rules for shows Clear with low confidence and a "not screened" rationale.
- Three new example files and four new portfolio fixtures.
- Report version 1.1. The provenance line and the Markdown export title no longer contain em-dashes.

## Upgrade

```bash
pip install --upgrade litmus-screener==1.1.0
litmus --version
litmus diff-ruleset <site-packages>/litmusai/_data/ruleset/ruleset-2024-1689-v1.0.json <site-packages>/litmusai/_data/ruleset/ruleset-2024-1689-v1.1.json
```

Requires Python 3.11 or newer. No network access at any point.

Source text for the new rules: Regulation (EU) 2026/1744, Article 1, points (7) and (40), read at the Publications Office Cellar (CELEX 32026R1744) on 31 October 2026. Full details in `CHANGELOG.md`.
