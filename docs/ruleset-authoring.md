# Bring Your Own Ruleset (BYO)

LitmusAI ships with a reference ruleset authored by AiExponent's internal panel. If your organisation needs a lawyer-signed interpretation, you can author your own.

## Ruleset Schema

A ruleset is a JSON file with this structure:

```json
{
  "ruleset_version": "your-org-v1.0",
  "regulation": "Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744",
  "effective_date": "2025-02-02",
  "rules": [...],
  "signature": { ... }  // optional
}
```

### Rule format

```json
{
  "id": "rule_a_your_rule_name",
  "category": "5.1.a",
  "version": "v1",
  "description": "Human-readable description of what this rule checks.",
  "expression": "system.inputs.biometric == true and system.outputs.behaviour_predictions == true",
  "verdict_if_triggered": "amber",
  "citations": ["Art. 5(1)(a)", "Recital 29"],
  "reviewed_by": "Your Law Firm LLP",
  "reviewed_date": "2026-05-01",
  "applies_from": null
}
```

`category` is one of the ten Article 5(1) points: `5.1.a`, `5.1.b`, `5.1.ba`, `5.1.bb`, `5.1.c`, `5.1.d`, `5.1.e`, `5.1.f`, `5.1.g`, `5.1.h`.

`applies_from` is optional. Set it to an ISO date (for example `"2026-12-02"` for points (ba) and (bb)) when the provision the rule encodes applies from a later date than the rest of the regulation. Reports then say "The prohibition applies from 2 December 2026" in the rationale. Leave it out, or `null`, for provisions that already apply.

A ruleset that has no rule for a category is still valid. The report lists every category; a category without rules shows Clear with `low` confidence and a "not screened" rationale, so nobody mistakes an unscreened point for a cleared one.

### Expression language

Rules use a constrained expression language (not Python). Supported:

- **Field access:** `system.inputs.biometric`, `system.outputs.individual_scores`, `system.generative_media.safeguards.documented`
- **Comparisons:** `==`, `!=`
- **Boolean:** `and`, `or`, `not`
- **Set membership:** `"value" in system.mitigations`
- **Functions:** `contains()`, `starts_with()`, `has_jurisdiction()`, `targets_population()`
- **Parentheses:** `(a or b) and c`

### Declaration fields for points (ba) and (bb)

The `generative_media` block of `system.yaml` carries the facts those rules test. Every field is a boolean that defaults to `false`, so a `system.yaml` written for an earlier version stays valid.

| Field | Meaning |
| --- | --- |
| `realistic_media_generation` | Generates or manipulates realistic images, video, audio or similar material (a face, voice or body in a credible real-life manner). |
| `identifiable_persons` | Outputs can depict identifiable natural persons. |
| `intimate_depictions_possible` | Intimate parts or sexually explicit activity are a reasonably foreseeable and reproducible outcome without significant technical modification. |
| `intimate_depictions_intended` | Producing such depictions of identifiable persons is the intended purpose, or the deployer's purpose. |
| `minors_depictions_possible` | Outputs can depict children in material within Directive 2011/93/EU, Article 2(c) and (e). |
| `manipulation_within_1b_only` | Only edits that neither increase exposure nor alter the nature of depicted activity (Art. 5(1b)). |
| `safeguards.consent_demonstrable` | Explicit consent of each depicted person is collected before generation and can be demonstrated. |
| `safeguards.intimate_output_prevention` | Measures that reliably prevent intimate outputs of identifiable persons. |
| `safeguards.csam_prevention` | Measures that reliably prevent child sexual abuse material. |
| `safeguards.misuse_correction` | Observed or reported misuse is detected and corrected. |
| `safeguards.documented` | The measures are written down, reviewed and testable. |

Two fields added for Article 5(1)(c) in the same release: `inputs.social_behaviour_data` (conduct outside the service that is scored) and `outputs.detrimental_treatment_unrelated_context` (the score is used against the person in an unrelated context).

### Signature block (optional)

```json
{
  "signer_name": "Smith & Co LLP",
  "signer_bar_number": "BAR-EU-12345",
  "signer_firm": "Smith & Co LLP",
  "signer_email": "partners@smithco.example",
  "signed_date": "2026-05-01",
  "signature_algorithm": "sha256",
  "signature_value": "hex-encoded-hash"
}
```

Supported algorithms: `sha256`, `pgp-detached`, `x509-pkcs7`.

## Worked example: `acme-corp-signed-v1.0.json`

A complete dummy-signed reference ruleset ships with the package at
[`tests/fixtures/rulesets/acme-corp-signed-v1.0.json`](../tests/fixtures/rulesets/acme-corp-signed-v1.0.json).
Use it as a paste-and-modify template when authoring your own.

It demonstrates every concept from the schema sections above:

- A complete `ruleset_version`, `regulation`, `effective_date` header
- One concrete rule for `5.1.a` with the canonical `id` / `version` /
  `description` / `expression` / `verdict_if_triggered` / `citations` /
  `reviewed_by` / `reviewed_date` fields
- A complete `signature` block signed by a hypothetical "Smith & Co LLP"
  with `signer_bar_number`, `signer_firm`, and `signer_email` populated
- The `sha256` signature algorithm

The signature in the fixture is a placeholder hex string for testing
purposes only; production rulesets must carry a real cryptographic
signature over the canonical JSON of the rules array. The signature
algorithm column tells LitmusAI how to verify; supported values are
`sha256` (HMAC-style), `pgp-detached`, and `x509-pkcs7`.

To try it end-to-end:

```bash
litmus verify-ruleset tests/fixtures/rulesets/acme-corp-signed-v1.0.json
litmus use-ruleset tests/fixtures/rulesets/acme-corp-signed-v1.0.json
litmus ruleset-info
litmus screen examples/example-clear.yaml
```

The report header will show `ruleset: acme-corp-v1.0 (SIGNED by: Smith
& Co LLP · 2026-05-01 · signature verified)` instead of the default
`UNREVIEWED` provenance.

## Using Your Ruleset

```bash
# Validate the ruleset
litmus verify-ruleset your-ruleset.json

# Set as active
litmus use-ruleset your-ruleset.json

# Screen with it
litmus screen system.yaml --ruleset your-ruleset.json

# Check what's active
litmus ruleset-info
```

## Provenance in Reports

When using a signed ruleset, every report header shows:

```
ruleset: your-org-v1.0 (SIGNED by: Smith & Co LLP · 2026-05-01 · signature verified)
```

When using the default reference ruleset:

```
ruleset: ruleset-2024-1689-v1.1.1 (UNREVIEWED: internal panel authored, no external legal review)
```

---

*Not legal advice. Not a notified body.*
