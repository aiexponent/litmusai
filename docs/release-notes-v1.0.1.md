# LitmusAI v1.0.1 (UNREVIEWED — internal panel authored, no external lawyer review)

> **GitHub release title (verbatim):**  
> `v1.0.1 — Article 5 screener (UNREVIEWED ruleset, internal panel authored)`

> **One-line summary for X / LinkedIn / HN:**  
> LitmusAI 1.0.1 release: improved CLI export ergonomics, Windows console compatibility, cross-linked 5-tool open-source AI governance ecosystem, and automated Dependabot updates.

---

## Highlights of v1.0.1

- **CLI Export Usability (PRD-166)**: Fixed command crash when running `litmus export` without `--output`, making `--output` optional and defaulting to stdout. Added explicit format validation for `json`, `markdown`, and `sarif`, plus helpful guidance if `pdf` format is requested without WeasyPrint installed.
- **Windows Console Compatibility**: Replaced Unicode characters in `litmus debug` output with ASCII equivalents, resolving `UnicodeEncodeError` crashes on Windows systems running `cp1252` encoding.
- **Canonical Organization & Action Paths (PRD-167)**: All URLs, documentation snippets, and GitHub Action paths point to the canonical `aiexponent/litmusai` organization (`.github/actions/litmusai-screen@v1`), eliminating reliance on deprecated redirects.
- **5-Tool Open-Source Governance Ecosystem (PRD-184)**: Deployed reciprocal footer across the AiExponent compliance suite linking LitmusAI (Art. 5) with `license-compliance-checker` (Art. 53), `rag-benchmarking` (Art. 15), `riskforge` (Art. 9), and `agentic-document-analyser` (Art. 9 / Annex IV).
- **Automated Dependency Maintenance (PRD-184)**: Added `.github/dependabot.yml` configured for weekly security scanning on `pip` and `github-actions`.
- **Badge Styling**: Unified all repository status badges to `style=flat-square` using AiExponent brand teal (`#0D5463`).
- **Canonical Apache-2.0 License**: Added full Apache-2.0 text and formal `NOTICE` attribution file.
- **Test Suite Expansion**: 264 tests passing under `pytest --disable-socket` (NFR-8 zero-network gate).

---

## Legal review status — UNREVIEWED

**LitmusAI 1.0.1 continues to ship with the AiExponent reference ruleset (`ruleset-2024-1689-v1.0`) which is `legal_status: UNREVIEWED`.** The ruleset has been authored and reviewed by an internal AiExponent panel of six engineering and governance roles (see `src/litmusai/_data/ruleset/internal-review-record-2024-1689-v1.0.md`) but has **not** been reviewed by a qualified EU AI Act practising lawyer.

The package version (1.0.1) reflects API and CLI stability. The legal-review status rides on the ruleset version and the `ruleset_legal_status: UNREVIEWED` indicator. A future `ruleset-2024-1689-v1.1` release will land `legal_status: REVIEWED` once external lawyer review completes.

---

## Install & Upgrade

```bash
pip install --upgrade litmus-screener
```

Verify the installation:
```bash
litmus --version
```

Screen an AI system description:
```bash
litmus screen --describe "Customer service AI assistant summarizing support tickets"
```

Export screening results:
```bash
litmus screen system.yaml -o report.json
litmus export report.json -o report.sarif --format sarif
```

---

## Disclaimers

> Every screening is a screening, not a certification.  
> **Not legal advice. Not a notified body.**

Apache 2.0. AS IS. No warranty of legal compliance.

---

*LitmusAI v1.0.1 · Built by [AI Exponent LLC](https://aiexponent.com) · Apache 2.0*
