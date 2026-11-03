# Article 5 Category Coverage

LitmusAI screens against all ten prohibited-practice categories of Article 5(1) of Regulation (EU) 2024/1689: the original eight, points (a) to (h), and the two inserted by Regulation (EU) 2026/1744, points (ba) and (bb). The reference ruleset is `ruleset-2024-1689-v1.2` (38 rules). Each question in the `influence` and `scope` blocks is answered `yes`, `no`, `not_sure` or `not_answered`, except `scope.role`, which is `provider_only`, `deployer` or `both`. A question left at `not_answered` keeps the 1.1 behaviour.

Report order follows the regulation: a, b, ba, bb, c, d, e, f, g, h.

## Categories

### 5.1.a: Harmful manipulation
AI systems that deploy subliminal or manipulative techniques to materially distort behaviour causing significant harm.

**Declared in:** `influence`: `subliminal_techniques`, `manipulative_or_deceptive_techniques`, `materially_distorts_behaviour`, `significant_harm_likely`
**Triggers:** a technique + material distortion + significant harm, all `yes` (RED); any of them `not_sure` and none `no` (AMBER)
**Not answered:** the 1.1 proxies apply (behaviour predictions + emotional inference RED; behaviour predictions AMBER), with low confidence
**Penalty:** Up to EUR 35M or 7% global turnover

### 5.1.b: Exploitation of vulnerabilities
AI systems that exploit vulnerabilities due to age, disability, or socioeconomic status.

**Declared in:** `influence`: `exploits_vulnerability`, `materially_distorts_behaviour`, `significant_harm_likely`
**Triggers:** exploitation + material distortion + significant harm, all `yes` (RED); any of them `not_sure` and none `no` (AMBER)
**Not answered:** the 1.1 proxies apply (minors + behaviour predictions RED; minors + freetext output or vulnerable economic situation AMBER), with low confidence

### 5.1.ba: Non-consensual intimate material of identifiable persons
Applies from 2 December 2026 (Article 113(a), as amended by Regulation (EU) 2026/1744).

AI systems that generate or manipulate realistic images, videos, audio or similar material of an identifiable natural person's intimate parts, or of that person engaged in sexually explicit activities, without that person's freely given, specific, informed, unambiguous and explicit consent.

Article 5(1a) limits the provider-side prohibition to two cases: the generation or manipulation is the system's intended purpose, or it is a reasonably foreseeable and reproducible outcome without significant technical modification and the system lacks reasonable and adequate technical safety measures and other safeguards to reliably prevent it and to correct misuse. The deployer-side prohibition covers use for that purpose. Article 5(1b) says that manipulating material in a way that does not increase the exposure of depicted intimate parts or alter the nature of depicted sexual activity is not manipulation.

**Declared in:** the `generative_media` block of `system.yaml`
**Triggers:** intended purpose + identifiable persons + no demonstrable consent (RED); realistic media + identifiable persons + intimate depictions possible + no consent + no adequate documented safeguards (RED); realistic media of identifiable persons with safeguards or consent undocumented (AMBER)
**Carve-outs:** demonstrable consent of the depicted person; edits within Article 5(1b) (never RED)

### 5.1.bb: Child sexual abuse material
Applies from 2 December 2026 (Article 113(a), as amended by Regulation (EU) 2026/1744).

AI systems that generate or manipulate material or performance within the meaning of Article 2, points (c) and (e), of Directive 2011/93/EU, except where a "without right" defence applies under national law. The same Article 5(1a) intended-purpose and foreseeable-outcome tests apply. There is no consent carve-out.

**Declared in:** the `generative_media` block of `system.yaml`
**Triggers:** realistic media + intimate depictions possible + minors depictions possible + no prevention measures (RED); the same in law-enforcement use (AMBER, a "without right" defence may apply); any realistic-media generator without documented prevention (AMBER)

### 5.1.c: Social scoring
Individual scoring based on social behaviour or personal characteristics, leading to detrimental treatment in unrelated contexts or disproportionate to the behaviour.

**Triggers:** individual scores + social behaviour data, or individual scores + detrimental treatment in an unrelated context, or individual scores + scraped internet data (RED); any other individual scoring (AMBER)
**Note:** credit scoring from repayment history in its own context is AMBER, not RED. It is high-risk under Annex III, point 5(b), which RiskForge covers, not a prohibited practice (fixed in ruleset v1.1, litmusai#25).

### 5.1.d: Criminal risk prediction
Predicting individual criminal risk based solely on profiling.

**Triggers:** criminal risk predictions output (RED)
**Exclusion:** `scope.human_assessment_on_verifiable_facts: yes`, a system that supports a human assessment already based on objective and verifiable facts directly linked to a criminal activity, gives AMBER for review

### 5.1.e: Untargeted facial image scraping
Building or expanding facial recognition databases from untargeted internet or CCTV scraping.

**Triggers:** facial images + scraped internet data (RED); facial images + public space (AMBER)
**Outside the point:** `scope.untargeted_collection: no` (a targeted search) or `scope.builds_facial_recognition_database: no` clears it

### 5.1.f: Emotion inference in workplace/education
Inferring emotions in workplace or educational settings.

**Triggers:** emotion inferences + workplace or education context (RED); emotion inference elsewhere, including healthcare (AMBER)
**Outside the point:** `scope.emotions_of_workers_or_students: no` (only customers, patients or the public) clears it
**Exception:** `scope.medical_or_safety_reasons: yes` gives AMBER for review

### 5.1.g: Biometric categorisation of sensitive attributes
Using biometric data to categorise individuals by race, political opinions, religion, sexual orientation.

**Triggers:** biometric/facial inputs + sensitive attribute classifications (RED)
**Carve-out:** `scope.dataset_labelling_or_filtering_only: yes` (labelling or filtering lawfully acquired biometric datasets) gives AMBER for review

### 5.1.h: Real-time remote biometric identification in public spaces
Real-time biometric identification in publicly accessible spaces.

**Triggers:** biometric/facial inputs + public space + real-time operation (RED)
**Outside the point:** `scope.role: provider_only` (point (h) prohibits use only), `scope.remote_identification: no`, or `scope.law_enforcement_purpose: no` clears it
**Exception:** `scope.article_5_1_h_objective: yes` (Art. 5(1)(h)(i) to (iii)) gives AMBER; Art. 5(2) and (3) add authorisation, a fundamental rights impact assessment and registration

## Categories a ruleset does not cover

The report always lists all ten categories. When the active ruleset has no rule for a category (for example a bring-your-own ruleset written before points (ba) and (bb) existed), that row stays Clear, its confidence is `low`, and its rationale says the category was not screened.

## Regulatory References

Citations refer to Regulation (EU) 2024/1689 as published in the Official Journal of the European Union on 12 July 2024, and to Regulation (EU) 2026/1744 (Digital Omnibus on AI), published on 24 July 2026. Article 5 has applied since 2 February 2025 per Article 113(a); points (ba) and (bb) and paragraphs (1a) and (1b) apply from 2 December 2026 per the amended Article 113(a). The amending text was read at the Publications Office Cellar (CELEX 32026R1744) on 31 October 2026.

---

*Not legal advice. Not a notified body.*
