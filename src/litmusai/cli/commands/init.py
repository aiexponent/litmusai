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

# Article 5(1)(a) and (b). Answer every question for every system, "yes",
# "no" or "not_sure", from what the system does or can do, whether or not
# anyone intends it. A system that does not influence what people decide
# answers "no". "not_answered" means the question was not considered;
# the report then marks (a) and (b) as low confidence. What each answer does
# to a verdict is in the README, not here, so answer the facts.
influence:
  # Stimuli a person cannot consciously perceive: flashed images, inaudible audio.
  subliminal_techniques: not_answered
  # Techniques that subvert a person's autonomy or free choice, or deceive them
  # with false or misleading content. "yes" also when nobody intended it, for
  # example behaviour the system learned in training; not for merely
  # incidental behaviour that the provider has measures against.
  manipulative_or_deceptive_techniques: not_answered
  # Exploits a vulnerability due to age (children or older people), a
  # disability, or a specific social or economic situation (for example
  # extreme poverty). Other weak points, such as loneliness or emotional
  # dependency, belong under manipulative_or_deceptive_techniques.
  exploits_vulnerability: not_answered
  # Has the objective or the effect (intent is not needed) of appreciably
  # impairing people's ability to make an informed decision, so that they
  # decide what they would not otherwise have decided.
  materially_distorts_behaviour: not_answered
  # That behaviour causes, or is reasonably likely to cause, significant
  # physical, psychological or financial harm to them or to others.
  significant_harm_likely: not_answered

# Exceptions and limits in Article 5(1), points (d) to (h). Answer the
# questions about what your system does and leave the others at
# "not_answered". What each answer does to a verdict is in the README.
scope:
  # provider_only: you place the system on the market or put it into service
  # and do not use it. deployer: you use it (also a private person using a
  # tool). both: you build and use it, or you are not sure.
  role: both
  # (d) The system only supports a human's assessment of a person's
  # involvement in a criminal activity, and that assessment already rests on
  # objective and verifiable facts directly linked to the activity.
  human_assessment_on_verifiable_facts: not_answered
  # (e) Facial images are collected without a target. "no" when the system
  # looks for one specific person or a specific, defined group.
  untargeted_collection: not_answered
  # (e) The system creates or expands a database used to recognise faces.
  builds_facial_recognition_database: not_answered
  # (f) The emotions inferred are those of workers (employees, contractors,
  # trainees, volunteers, job candidates) or of pupils and students. "no"
  # when only customers, patients or the public are analysed.
  emotions_of_workers_or_students: not_answered
  # (f) The system is intended to be put in place for medical or safety
  # reasons, such as a therapy aid or fatigue detection at dangerous machines.
  medical_or_safety_reasons: not_answered
  # (g) The system only labels or filters lawfully acquired biometric
  # datasets, or categorises biometric data in the area of law enforcement.
  dataset_labelling_or_filtering_only: not_answered
  # (h) People are identified at a distance without their active
  # involvement, such as cameras in a street. "no" when each person takes
  # part, such as stepping up to a gate or presenting a document.
  remote_identification: not_answered
  # (h) Used by or for a law enforcement authority to prevent, investigate,
  # detect or prosecute crime or to execute criminal penalties (Art. 3(46)).
  law_enforcement_purpose: not_answered
  # (h) Each use is strictly necessary for one of: (i) a targeted search for
  # victims of abduction, trafficking or sexual exploitation, or for missing
  # persons; (ii) preventing a specific, substantial and imminent threat to
  # life or physical safety, or a terrorist attack; (iii) locating or
  # identifying a suspect of an Annex II offence punishable by at least
  # four years, for an investigation, prosecution or penalty.
  article_5_1_h_objective: not_answered

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
