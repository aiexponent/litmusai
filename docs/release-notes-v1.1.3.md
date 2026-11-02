# LitmusAI 1.1.3

Citation corrections. Reference ruleset `ruleset-2024-1689-v1.1.1` (UNREVIEWED: internal panel authored, no external lawyer review). Apache 2.0, AS IS. Not legal advice. Not a notified body.

## Fixed

- Eleven rules cited a recital of Regulation (EU) 2024/1689 that is about a different Article 5 point. Points (a), (b), (c), (e) and (g) now cite the recital that explains them: 29 for (a) and (b), 31 for (c), 43 for (e) and 30 for (g). The independent verification run found the errors, and each recital was read against the Regulation at the Publications Office on 2 November 2026. The same citations were wrong in 1.0.x and 1.1.0 to 1.1.2.
- No published package so far contained the internal review records, because a `.gitignore` pattern for internal notes matched them and the wheel build applies `.gitignore`. 1.1.3 ships the v1.0, v1.1 and v1.1.1 records under `litmusai/_data/ruleset/`.
- A new test maps each Article 5(1) point to its recitals and fails the build if a rule cites one outside the map.

No verdict changes. Rule expressions, verdicts, report schema and CLI surface are those of 1.1.2. Reports now name `ruleset-2024-1689-v1.1.1`. A report written by 1.1.2 and one written by 1.1.3 for the same file differ in `ruleset_version`, the ruleset provenance block, the citations, `litmusai_version` and `generated_at`. No verdict or confidence differs. The v1.1 and v1.0 rulesets stay in the package; `litmus diff-ruleset` shows the change.

## Upgrade

```bash
pip install --upgrade litmus-screener==1.1.3
litmus --version
```

Requires Python 3.11 or newer. Installing needs a package index; screening makes no network calls. Full details in `CHANGELOG.md`.
