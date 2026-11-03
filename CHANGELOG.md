# Changelog

All notable changes to LitmusAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2026-11-03

> Wording only. Rules, ruleset `ruleset-2024-1689-v1.2`, verdicts and report schema are those of 1.2.0.

### Changed

- **The `litmus init` template asks factual questions only (PRD-464).** The comments no longer say what an answer does to a verdict ("no: clears", "yes: amber"). That is documented in the README's "Article 5 Categories Covered" table, so a user is not steered towards the answer that gives the verdict they want. The blind re-test of 1.2.0 reported this as a risk.
- **Every `influence` and `scope` question now has guidance,** from the ten points the re-test tester found unclear:
  - answer all `influence` questions from what the system does, intended or not, with `no` for a system that does not influence decisions, and keep `not_answered` for questions not considered;
  - manipulative or deceptive techniques count when nobody intended them, but not merely incidental behaviour the provider has measures against (Commission guidelines C(2025) 5052, para. 69);
  - intent is not needed for material distortion (para. 76);
  - weak points other than age, disability or a social or economic situation belong under the techniques question (para. 125);
  - significant harm is harm caused by the distorted behaviour;
  - `role` for a private person (`deployer`) and for build-and-use (`both`);
  - the (d) question requires a human assessment;
  - (f) covers job candidates, trainees and volunteers, and pupils and students (paras. 254 and 255);
  - examples for remote identification;
  - the definition of law enforcement (Art. 3(46));
  - the three (h) objectives written out.
- Tests check that the template carries no verdict effects, that every question has guidance, and that the README shows the template byte for byte.

## [1.2.0] - 2026-11-03

> **LitmusAI 1.2.0 ships with reference ruleset `ruleset-2024-1689-v1.2` (UNREVIEWED: internal panel authored, no external lawyer review). Apache 2.0, AS IS.** A `system.yaml` written for 1.1.x keeps every verdict.

### Added

- **Questions for Article 5(1)(a) and (b) (PRD-449).** A new `influence` block asks for each legal element:
  - subliminal techniques;
  - purposefully manipulative or deceptive techniques;
  - exploitation of a vulnerability due to age, disability or a specific social or economic situation;
  - material distortion of behaviour;
  - likely significant harm.

  Each answer is `yes`, `no`, `not_sure` or `not_answered` (the default). For each point, all `yes` gives RED; a `not_sure` on any element, with no element answered `no`, gives AMBER; a `no` on any element clears the point. While a technique (or exploitation) question stays unanswered and no element is `no`, the 1.1 proxy rules apply and (a) and (b) report low confidence, with a note in the rationale. The independent test found 6 expected prohibitions on (a) and (b) that 1.1.x screened clear (`verification/REPORT.md`).
- **The exceptions and limits written in Article 5(1), points (d) to (h).** A new `scope` block covers:
  - (d) human assessment on objective and verifiable facts;
  - (e) untargeted collection, and whether a facial recognition database is built;
  - (f) whether the emotions are those of workers or students, and medical or safety reasons;
  - (g) labelling or filtering of lawfully acquired biometric datasets;
  - (h) the role (`provider_only`, since point (h) prohibits use), remote identification, law-enforcement purpose and the objectives in (h)(i) to (iii).

  A fact that takes a system outside a point clears it. An exception that needs evidence gives AMBER for review. These gaps caused most of the 32 false alarms in the independent test.
- `older_persons` as a population category.
- `litmus init`, the README and `docs/article-5-coverage.md` document every new question.

### Changed

- Ruleset `ruleset-2024-1689-v1.2` (38 rules) is the default.
  - Ten rules are added.
  - Eighteen rules keep their whole v1.1.1 condition and gain only a condition on a new field.
  - On 195 declarations (the 175 test cases, the examples and the test fixtures), v1.1.1 and v1.2 give the same verdict on every point when the new questions are unanswered. Only the confidence on (a) and (b) changes.
- Report version 1.2. A report now includes the `influence` and `scope` blocks in its `system` and its input hash. `litmus verify <report> <system.yaml>` still verifies a 1.0 or 1.1 report against an unchanged file, and reports a mismatch when the file now answers questions the old report never covered.
- An answer written as an unquoted YAML `yes` or `no` is accepted as `"yes"` or `"no"`.

### Not changed

The quick screen (`--describe`) does not answer the new questions. These cases are still not modelled:
- (c) proportionality;
- (ba) and (bb) accidental generation, emergency medical use and the red-teaming defence;
- emotion recognition used only for a person's own training.

## [1.1.3] - 2026-11-02

> Citation corrections only. Rule expressions, verdicts and report schema are those of 1.1.2.

### Fixed

- **Recital citations that named the wrong Article 5 point.** Eleven rules in `ruleset-2024-1689-v1.1` (and the same rules in v1.0) cited a recital of Regulation (EU) 2024/1689 about another point: Recital 30 or 31 for point (a), Recital 32 for point (b), Recital 33 for point (c), Recital 42 for point (e) and Recital 44 for point (g). New ruleset `ruleset-2024-1689-v1.1.1` cites Recital 29 for (a) and (b), 31 for (c), 43 for (e) and 30 for (g), and is the default. Found by the independent verification run (`verification/`, PRD-274); each recital was read against the Regulation at the Publications Office Cellar on 2026-11-02. The internal review record for v1.1.1 lists every change. `tests/unit/test_ruleset_citations.py` maps each point to its recitals and fails on a citation outside the map; on the v1.1 file it fails on exactly these eleven rules.
- **The internal review records were missing from the package.** A `.gitignore` pattern for internal notes matched `internal-review-record-2024-1689-v1.1.md`, and the wheel build applies `.gitignore`, so no published package so far contained a review record, although the README says the records ship under `litmusai/_data/ruleset/`. The pattern now exempts the review records, 1.1.3 ships the v1.0, v1.1 and v1.1.1 records, and a test fails if a bundled ruleset has no record next to it.

### Changed

- Reports name `ruleset-2024-1689-v1.1.1`. The v1.1 and v1.0 files stay in the package, and `litmus diff-ruleset` between v1.1 and v1.1.1 shows citation, rule version and review-stamp changes only.

## [1.1.2] - 2026-11-02

> Documentation and GitHub Action corrections only. Package code, rules, verdicts and report schema are those of 1.1.1.

### Fixed

- **Documentation claims that outran the code.** The README no longer offers PDF export: `litmus export --format pdf` has always exited 2 with "PDF export is not supported", and no WeasyPrint extra exists. The 1.0.0 notes below describe a PDF exporter, an override mechanism and an `override-file` Action input; none of the three shipped, and each line now says so. The README's Action example pins `@v1.1.2`, this release's tag; a `v1` tag was never created.
- **GitHub Action `output-format: sarif` wrote JSON.** `litmus screen --output` always writes JSON, so the Action's SARIF option produced a JSON file with a `.sarif` name. The Action now runs `litmus export --format sarif` after the screen when SARIF is requested. CI runs the Action on the shipped examples on every push: the clear, amber and red examples, both report formats, and `fail-on` set to red, amber and none, so the published package and the Action are exercised on a real runner.

## [1.1.1] - 2026-11-01

### Fixed

- **`litmus verify <report> <system.yaml>` reported every pre-1.1.0 file as tampered.** The two-argument form hashed the raw YAML, while `litmus screen` hashes the validated declaration with its defaults filled in. The two only agreed for a file that spelt out every field; 1.0.1 already failed on `tests/fixtures/portfolio/calculator_clear.yaml`, and from 1.1.0 every file without the `generative_media` block failed, which is every file written before 1.1.0, including the shipped examples. `verify` now validates the file and hashes it the same way as `screen`. For a report with `report_version` 1.0 (written by 1.0.x) it hashes the system without the three fields added in 1.1, so an unchanged file still verifies; a file that now sets one of those fields reports a mismatch, because the old hash never covered them. Any read, parse or validation failure exits 2 instead of a traceback or a mismatch. The one-argument form was not affected. Found by the aiexponent.com evidence capture on release day; eight tests pin the behaviour, one of them against a report written by 1.0.1 itself.

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
> Package SemVer reflects API stability. The CLI surface, JSON / SARIF schema, and BYO-ruleset contract are stable for production integration. The `ruleset_legal_status: UNREVIEWED` line printed by `litmus version` separates the legal-review status from the package version — a future `ruleset-2024-1689-v1.1` release will land `legal_status: REVIEWED` once external lawyer review completes. [Update 2026-11-02: v1.1 shipped on 2026-11-01 with the UNREVIEWED label; external review has no date.]

### Added — engine

- **Eight-category Article 5 screening engine.** Pure-Python, deterministic, all `system.*` field accesses go through a constrained expression language with no `eval` and no Python execution. 22 reference rules covering all eight Article 5 sub-points (5.1.a–h).
- **Conservative-by-default verdict logic.** Where the regulatory text is ambiguous, the ruleset prefers `amber` over `clear` so a qualified reviewer takes the final call.
- **Per-rule confidence band** (`high` / `medium` / `low`) on every verdict so reviewers can prioritise the soft calls.
- **SHA-256 input hash** on every report (`canonical_json` via RFC 8785 ordering, with `date` / `datetime` coercion to ISO strings).
- **Override mechanism** with full audit trail (`OverrideEntry`) — FR-10. [Never shipped: the model exists, nothing applies it, and `overrides_applied` is always empty. Noted 2026-11-02.]

### Added — CLI commands

- `litmus screen [path|--describe]` — primary screening surface, rich console + multiple formats
- `litmus init` — scaffold a starter `system.yaml` (FR-7)
- `litmus export <report> --format {json|markdown|sarif|pdf}` — converters; PDF via optional WeasyPrint extra [PDF never shipped: the format exits 2 and no extra exists. Noted 2026-11-02.]
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
- **PDF** export via WeasyPrint (optional extra: `pip install litmus-screener[pdf]`) [Never shipped. Noted 2026-11-02.]

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

- **GitHub Action wrapper** at `aiexponent/litmusai/.github/actions/litmusai-screen@v1` — drop-in CI integration with `path`, `fail-on`, `output-format`, and `override-file` inputs (FR-27) [The inputs are `path`, `fail-on`, `output-format`, `ruleset` and `python-version`; `override-file` never existed. Noted 2026-11-02.]
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
