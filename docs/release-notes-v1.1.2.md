# LitmusAI 1.1.2

Documentation and GitHub Action corrections. Ruleset `ruleset-2024-1689-v1.1`, unchanged (UNREVIEWED: internal panel authored, no external lawyer review). Apache 2.0, AS IS. Not legal advice. Not a notified body.

## Fixed

- The README and the PyPI description no longer offer PDF export. `litmus export --format pdf` has always exited 2 with "PDF export is not supported", and no WeasyPrint extra exists. The 1.0.0 changelog lines that described a PDF exporter, an override mechanism and an `override-file` Action input now say that none of the three shipped.
- The Action example in the README pointed at `@v1`, a tag that was never created. It now pins `@v1.1.2`.
- The GitHub Action's `output-format: sarif` wrote the JSON screen report under a `.sarif` name. It now runs `litmus export --format sarif` after the screen. The repository's CI runs the Action on the shipped examples on every push, so the published package and the Action are exercised on a real runner.

Nothing else changed: package code, rules, verdicts, report schema and CLI surface are those of 1.1.1.

## Upgrade

```bash
pip install --upgrade litmus-screener==1.1.2
litmus --version
```

Requires Python 3.11 or newer. No network access at any point. Full details in `CHANGELOG.md`.
