# LitmusAI 1.1.1

Patch release on the day of 1.1.0. Ruleset `ruleset-2024-1689-v1.1`, unchanged (UNREVIEWED: internal panel authored, no external lawyer review). Apache 2.0, AS IS. Not legal advice. Not a notified body.

## Fixed

`litmus verify report.json system.yaml` reported every file written before 1.1.0 as tampered. The two-argument form hashed the raw YAML, while `litmus screen` hashes the validated declaration with its defaults filled in. From 1.1.0 the two differed for any file without the `generative_media` block, including the shipped examples. `verify` now validates the file and hashes it exactly as `screen` does, so a report and its source file agree again. An unreadable or invalid file exits 2. The one-argument form, which checks the report against the system it embeds, was not affected.

Nothing else changed: rules, verdicts, report schema and CLI surface are those of 1.1.0.

## Upgrade

```bash
pip install --upgrade litmus-screener==1.1.1
litmus --version
```

Requires Python 3.11 or newer. No network access at any point. Full details in `CHANGELOG.md`.
