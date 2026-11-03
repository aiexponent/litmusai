"""litmus init: create a starter system.yaml template (FR-3, US-13)."""

from __future__ import annotations

from pathlib import Path

import typer

from litmusai.cli.main import app

_TEMPLATE = """\
# LitmusAI System Description
# Edit the fields below to describe your AI system.
# Then run: litmus screen system.yaml

name: "My AI System"
version: "1.0.0"
provider: "My Organisation"
deployer: "My Organisation"
purpose: "Describe what the system does in one sentence."
system_description: |
  A more detailed description of the system: what inputs it takes,
  what outputs it produces, and how those outputs are used.

deployment_jurisdictions:
  - EU

output_consumed_in_eu: true

subject_population:
  categories:
    - general_public
  notes: null

inputs:
  biometric: false
  facial_images: false
  emotional_state_inference: false
  behaviour_history: false
  social_behaviour_data: false        # conduct outside the service: social media, associations
  scraped_internet_data: false
  freetext_prompts: false
  other: null

outputs:
  individual_scores: false
  behaviour_predictions: false
  criminal_risk_predictions: false
  emotion_inferences: false
  sensitive_attribute_classifications: false
  freetext_generations: false
  detrimental_treatment_unrelated_context: false   # score used against the person elsewhere
  other: null

deployment_context:
  workplace: false
  education: false
  public_space: false
  real_time_operation: false
  law_enforcement_use: false
  healthcare: false
  financial_services: false
  other: null

# Article 5(1)(ba) and (bb), inserted by Regulation (EU) 2026/1744 and
# applicable from 2 December 2026. Leave everything false for a system
# that does not generate or manipulate realistic images, video or audio.
generative_media:
  realistic_media_generation: false   # realistic images, video, audio or similar material
  identifiable_persons: false         # outputs can depict identifiable real people
  intimate_depictions_possible: false # intimate parts or sexual activity, without major modification
  intimate_depictions_intended: false # that output is the system's purpose
  minors_depictions_possible: false   # outputs can depict children in such material
  manipulation_within_1b_only: false  # edits that neither increase exposure nor change the activity
  safeguards:                         # each one: in place, in force and verifiable
    consent_demonstrable: false       # explicit consent of each depicted person, collected and provable
    intimate_output_prevention: false # filters, refusal training, guardrails against intimate outputs
    csam_prevention: false            # measures against child sexual abuse material
    misuse_correction: false          # abuse detection, notice and action, follow-up on circumvention
    documented: false                 # the measures above are written down and testable

# Article 5(1)(a) and (b). Answer each question "yes", "no" or "not_sure".
# A technique (or exploitation) question left at "not_answered" keeps the
# screen on capability proxies, with low confidence. For each point: all yes
# is RED; any not_sure with no element answered "no" is AMBER; a "no" on any
# element clears it.
influence:
  subliminal_techniques: not_answered                # (a) stimuli a person cannot perceive
  manipulative_or_deceptive_techniques: not_answered # (a) purposefully manipulative or deceptive
  exploits_vulnerability: not_answered               # (b) due to age, disability or social or economic situation
  materially_distorts_behaviour: not_answered        # (a, b) people decide what they would not otherwise
  significant_harm_likely: not_answered              # (a, b) physical, psychological or financial harm

# Exceptions and limits in Article 5(1), points (d) to (h). Answer only those
# that apply; leave the rest at "not_answered". A "no" marked "clears" takes
# the system outside that point; a "yes" marked "amber" claims an exception
# a reviewer must check.
scope:
  role: both                                         # provider_only, deployer or both; (h) prohibits use only
  human_assessment_on_verifiable_facts: not_answered # (d) yes: amber
  untargeted_collection: not_answered                # (e) no (a targeted search): clears
  builds_facial_recognition_database: not_answered   # (e) no: clears
  emotions_of_workers_or_students: not_answered      # (f) no (customers, patients, public): clears
  medical_or_safety_reasons: not_answered            # (f) yes: amber
  dataset_labelling_or_filtering_only: not_answered  # (g) yes: amber
  remote_identification: not_answered                # (h) no (person steps up to a sensor): clears
  law_enforcement_purpose: not_answered              # (h) no: clears
  article_5_1_h_objective: not_answered              # (h) yes, one of (i) to (iii): amber

mitigations: []

metadata:
  last_reviewed: null
  owner: null
  reviewed_by: null
"""


@app.command()
def init(
    output: Path = typer.Option(
        Path("system.yaml"),
        "--output",
        "-o",
        help="Path for the generated system description file.",
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite if file exists."),
) -> None:
    """Create a starter system.yaml template."""
    if output.exists() and not force:
        typer.echo(f"File already exists: {output}. Use --force to overwrite.", err=True)
        raise typer.Exit(code=2)

    output.write_text(_TEMPLATE)
    typer.echo(f"Created {output}. Edit it, then run: litmus screen {output}")
