# Changelog

All notable changes to LitmusAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-01

> **LitmusAI 1.1.0 ships with reference ruleset `ruleset-2024-1689-v1.1` (UNREVIEWED: internal panel authored, no external lawyer review). Apache 2.0, AS IS.**

### Added

- **Article 5(1)(ba) and (bb) screening (PRD-411).** Regulation (EU) 2026/1744 (Digital Omnibus on AI) inserts two prohibitions into Article 5(1), applicable from 2 December 2026: non-consensual intimate material of identifiable persons, and child sexual abuse material. The report now lists ten categories in regulation order (a, b, ba, bb, c to h). Six new rules encode the Article 5(1a) intended-purpose and foreseeable-outcome tests, the safeguards test, the consent carve-out of point (ba), the Article 5(1b) manipulation carve-out, and the "without right" defence of point (bb). Source text read at the Publications Office Cellar (CELEX 32026R1744) on 2026-10-31.
- **`generative_media` declaration block** in `system.yaml`: six capability flags and a nested `safeguards` block (`consent_demonstrable`, `intimate_output_prevention`, `csam_prevention`, `misuse_correction`, `documented`). Every field defaults to false, so existing files stay valid. `litmus init` writes the block with comments.
- **`applies_from` on rules** (optional ISO date). Rules for points (ba) and (bb) carry `2026-12-02`; the rationale of a triggered category says "The prohibition applies from 2 December 2026". `litmus ruleset-info` lists the dates. `litmus diff-ruleset` reports changes to the field.
- **"Not screened" rows.** When the active ruleset has no rule for a category (for example a BYO ruleset written for v1.0), that row stays Clear with `low` confidence and a rationale that says the category was not screened.
- **Examples** `example-ba-red.yaml`, `example-bb-red.yaml` and `example-generative-clear.yaml`, and four portfolio fixtures, all covered by tests.
- **`--describe` keywords** for generative media (deepfake, face swap, voice clone, undress, text-to-image, content filter, consent) and for social scoring (social media, social credit).
- `litmusai.categories`: one registry of the ten categories, their labels and the default ruleset path, used by the engine, the models and every command.

### Changed

- **Social scoring false positive (litmusai#25).** `rule_c_social_scoring` no longer fires Red on any individual score built from behaviour history. It now needs `inputs.social_behaviour_data` (conduct outside the service) or `outputs.detrimental_treatment_unrelated_context`, both new fields. A credit score from repayment history reads Amber through `rule_c_scoring_general`, which matches its Annex III high-risk status.
- **Ruleset `regulation` field** now reads "Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744". Three v1.0 rule descriptions lost their em-dashes. `ruleset-2024-1689-v1.0.json` stays in the package so `litmus diff-ruleset` can show the change.
- **Report version** is `1.1` (ten categories, the new declaration block). Reports written by 1.0.x still parse.
- **Output wording.** The provenance line every run prints is now `(UNREVIEWED: internal panel authored, no external legal review)`; the Markdown export title, the `use-ruleset` and `ruleset-info` lines, the `diff-ruleset` placeholders and the GitHub release name no longer contain em-dashes. `litmus --help` names the ten categories. `litmus verify-ruleset` calls cryptographic verification "a planned feature" instead of "a v1.1 feature".
- **README.** Ten categories; the Article 5 table has rows for (ba), (bb) and a corrected (c); the legal-review status is tied to a signed provenance header rather than to a ruleset version number; "filing-ready" and "certify" removed.

## [1.0.1] - 2026-09-21

### Fixed

- **CLI Export Command Ergonomics (PRD-166)**: Fixed crash in `litmus export` when invoked without `--output`, making the flag optional and defaulting cleanly to stdout. Added explicit format validation for `json`, `markdown`, and `sarif`, with clear guidance when `pdf` is requested without optional WeasyPrint dependencies.
- **Windows Console Compatibility**: Replaced Unicode em-dash and arrow characters in `litmus debug` output with ASCII alternatives, preventing `UnicodeEncodeError` on Windows systems using `cp1252` encoding.
- **CI Test Runner on Windows**: Configured `shell: bash` for multi-line test steps in GitHub Actions CI to fix Windows matrix runner failures.
- **Organization and Action Paths (PRD-167)**: Updated all repository URLs, CI workflow references, and documentation to the canonical `aiexponent/litmusai` organization, removing deprecated redirects.

### Changed

- **Visual Badges (PRD-184)**: Standardized all README status badges to `style=flat-square` with brand teal `#0D5463`.
- **Licensing & Attribution**: Upgraded `LICENSE` to the full canonical Apache-2.0 text and added formal `NOTICE` file attributing `AI Exponent LLC`.
- **CI Actions Bump**: Updated GitHub Actions dependencies to Node.js 24 runtime (`checkout@v6`, `setup-python@v6`, `upload-artifact@v7`, `download-artifact@v8`).

### Added

- **Reciprocal Ecosystem Footer (PRD-184)**: Added reciprocal 5-tool open-source AI governance cross-linking footer in `README.md` referencing sibling tools (`license-compliance-checker`, `rag-benchmarking`, `riskforge`, and `agentic-document-analyser`).
- **Dependabot Configuration (PRD-184)**: Added `.github/dependabot.yml` configured for weekly security update scanning on `pip` and `github-actions`.
- **Self-Scan Workflow**: Added `license-compatibility.yml` workflow for automated license compliance policy checks.
- **Regression Test Suites**: Added automated assertions for Dependabot configuration, README ecosystem links, and organization naming integrity.

## [1.0.0] — 2026-04-28

> **LitmusAI 1.0.0 ships with the AiExponent reference ruleset (UNREVIEWED — internal panel authored, no external lawyer review). Apache 2.0, AS IS.**
>
> Package SemVer reflects API stability. The CLI surface, JSON / SARIF schema, and BYO-ruleset contract are stable for production integration. The `ruleset_legal_status: UNREVIEWED` line printed by `litmus version` separates the legal-review status from the package version — a future `ruleset-2024-1689-v1.1` release will land `legal_status: REVIEWED` once external lawyer review completes.

### Added — engine

- **Eight-category Article 5 screening engine.** Pure-Python, deterministic, all `system.*` field accesses go through a constrained expression language with no `eval` and no Python execution. 22 reference rules covering all eight Article 5 sub-points (5.1.a–h).
- **Conservative-by-default verdict logic.** Where the regulatory text is ambiguous, the ruleset prefers `amber` over `clear` so a qualified reviewer takes the final call.
- **Per-rule confidence band** (`high` / `medium` / `low`) on every verdict so reviewers can prioritise the soft calls.
- **SHA-256 input hash** on every report (`canonical_json` via RFC 8785 ordering, with `date` / `datetime` coercion to ISO strings).
- **Override mechanism** with full audit trail (`OverrideEntry`) — FR-10.

### Added — CLI commands

- `litmus screen [path|--describe]` — primary screening surface, rich console + multiple formats
- `litmus init` — scaffold a starter `system.yaml` (FR-7)
- `litmus export <report> --format {json|markdown|sarif|pdf}` — converters; PDF via optional WeasyPrint extra
- `litmus debug <report>` — full rule-firing trace per category (FR-33)
- `litmus verify <report>` — re-hash the input and confirm the report has not been tampered with
- `litmus portfolio <dir>` — bulk-screen every `system.yaml` in a directory
- `litmus use-ruleset <path>` — set a custom (BYO) ruleset as active (FR-34)
- `litmus verify-ruleset <path>` — validate a ruleset's structure + optional signature (FR-35)
- `litmus ruleset-info` — print provenance of the currently-active ruleset (FR-36)
- `litmus diff-ruleset <old> <new>` — structural diff between two rulesets, with `--format json` for CI (FR-26)
- `litmus --version` — multi-line: package version + ruleset version + ruleset legal status + signer

### Added — exporters

- **SARIF 2.1.0** output mapping each Article 5 sub-point to a SARIF rule ID — compatible with GitHub Advanced Security, GitLab SAST, Azure DevOps Advanced Security (FR-29)
- **Markdown** export for human-readable governance reports
- **PDF** export via WeasyPrint (optional extra: `pip install litmus-screener[pdf]`)

### Added — BYO-ruleset

- Optional `RulesetSignature` block on every `Ruleset`. Supported algorithms: `sha256`, `pgp-detached`, `x509-pkcs7`.
- Provenance header on every report (FR-36): `(SIGNED by: <signer> · <date>)` for signed rulesets, `(UNREVIEWED — internal panel authored, no external legal review)` for the default
- `docs/ruleset-authoring.md` walks through the schema, the signing format, and a worked example using the dummy-signed `tests/fixtures/rulesets/acme-corp-signed-v1.0.json`

### Added — distribution surface (G6 mitigations)

- README first-section blockquote carries the verbatim UNREVIEWED disclosure (renders on PyPI's project page via `long_description`)
- New badge: `ruleset_legal_status: UNREVIEWED`, anchored to the in-README "Legal review status" section
- `litmus version` output adds `ruleset_legal_status: …` and `ruleset_signer: …` lines so the legal status surfaces at the command line, not just in reports
- Pre-drafted GitHub release-note body at `docs/release-notes-v1.0.0.md` — used by the release-on-tag workflow
- Release-note title format: `v1.0.0 — Article 5 screener (UNREVIEWED ruleset, internal panel authored)`

### Added — developer experience

- **GitHub Action wrapper** at `aiexponent/litmusai/.github/actions/litmusai-screen@v1` — drop-in CI integration with `path`, `fail-on`, `output-format`, and `override-file` inputs (FR-27)
- **Conventional exit codes** (FR-28): 0 = clear / below-threshold, 1 = threshold exceeded, 2 = invalid input / schema error, 3 = tamper detected
- Three worked-example `system.yaml` files in `examples/` covering CLEAR (`example-clear.yaml`), AMBER (`example-amber.yaml`), and RED (`example-red.yaml`) verdicts. CI pin via `tests/integration/test_examples.py` ensures any future ruleset change that flips an example's verdict surfaces before release.

### Added — quality gates

- **257 tests passing** under `pytest --disable-socket` (NFR-8 zero-network gate)
- **87.39% coverage** across engine + models (PRD target: ≥ 80%)
- **`mypy --strict`** clean across 26 source files
- **`ruff check`** + **`ruff format --check`** clean across 45 files
- **`licensecheck`** clean — all 22 production dependencies are Apache / MIT / BSD compatible
- CI matrix: Ubuntu / macOS / Windows × Python 3.11 / 3.12 / 3.13

### Notes

- **Distribution name vs brand name.** The product brand is **LitmusAI**. The PyPI distribution is **`litmus-screener`** because `litmus-ai` and `litmusai` were already taken on PyPI by an unrelated AI project ("Litmus AI" hallucination-detection SDK). Install command: `pip install litmus-screener`. The CLI entry point is still `litmus`, the Python module is still `litmusai`, the GitHub repo is still `aiexponent/litmusai`. Same pattern as `pip install torch` for PyTorch.
- **Legal-review status: UNREVIEWED.** External lawyer review is **not** a release blocker per the project's published acceptance criteria (PRD §NFR-10). The package ships with conservative-by-default verdicts, prominent `UNREVIEWED` disclaimers on every distribution surface, and a Bring-Your-Own-Ruleset mechanism so customers with their own counsel can supply a signed ruleset today. A future `ruleset-2024-1689-v1.1` release will bump the ruleset's `legal_status` to `REVIEWED`; the LitmusAI package version (`1.0.x`) tracks API stability and will not bump for that change.
- **Not legal advice. Not a notified body.** Apache 2.0. AS IS.
