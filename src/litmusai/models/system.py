"""Input models for LitmusAI screening: PRD §7.1."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field, field_validator

_POPULATION_CATEGORIES = frozenset(
    {
        "general_public",
        "minors",
        "workers",
        "students",
        "persons_with_disabilities",
        "persons_in_vulnerable_economic_situations",
        "other",
    }
)


class SubjectPopulation(BaseModel, extra="forbid"):
    categories: list[str] = Field(..., min_length=1)
    notes: str | None = None

    @field_validator("categories")
    @classmethod
    def _validate_categories(cls, v: list[str]) -> list[str]:
        for cat in v:
            if cat not in _POPULATION_CATEGORIES:
                msg = (
                    f"Unknown population category: {cat!r}. "
                    f"Allowed: {sorted(_POPULATION_CATEGORIES)}"
                )
                raise ValueError(msg)
        return v


class SystemInputs(BaseModel, extra="forbid"):
    biometric: bool = False
    facial_images: bool = False
    emotional_state_inference: bool = False
    behaviour_history: bool = False
    # Data about a person's conduct outside the service that scores them:
    # social media activity, associations, lifestyle, civic behaviour. The
    # Article 5(1)(c) test is about social behaviour, not any history
    # (litmusai#25). Repayment history for a credit score is not this.
    social_behaviour_data: bool = False
    scraped_internet_data: bool = False
    freetext_prompts: bool = False
    other: str | None = None


class SystemOutputs(BaseModel, extra="forbid"):
    individual_scores: bool = False
    behaviour_predictions: bool = False
    criminal_risk_predictions: bool = False
    emotion_inferences: bool = False
    sensitive_attribute_classifications: bool = False
    freetext_generations: bool = False
    # The score leads to detrimental or unfavourable treatment of the person
    # in a social context unrelated to where the data was collected, or
    # treatment that is disproportionate to the behaviour (Art. 5(1)(c)(i)
    # and (ii)). A loan decision based on repayment data is the same context.
    detrimental_treatment_unrelated_context: bool = False
    other: str | None = None


class GenerativeMediaSafeguards(BaseModel, extra="forbid"):
    """Technical safety measures and other safeguards, Art. 5(1a)(a)(ii).

    Every flag means "in place, in force and verifiable", not "planned".
    """

    # Freely given, specific, informed, unambiguous and explicit consent of
    # each depicted person is collected before generation or manipulation
    # and can be demonstrated afterwards (Art. 5(1)(ba)).
    consent_demonstrable: bool = False
    # Measures that reliably prevent intimate or sexually explicit outputs of
    # identifiable persons: data cleaning, refusal training, prompt
    # guardrails, output classifiers and filters, usage restrictions.
    intimate_output_prevention: bool = False
    # Measures that reliably prevent child sexual abuse material: the same
    # kinds of measures, plus known-material matching and age controls.
    csam_prevention: bool = False
    # Observed or reported misuse is detected and corrected: abuse
    # detection, notice and action, follow-up on circumvention.
    misuse_correction: bool = False
    # The measures above are written down, reviewed and testable.
    documented: bool = False


class GenerativeMedia(BaseModel, extra="forbid"):
    """Capabilities that Art. 5(1)(ba) and (bb) turn on, as inserted by
    Regulation (EU) 2026/1744 and read with Art. 5(1a) and (1b).

    Set a flag to true when it holds for the system as shipped, without
    significant technical modification (Art. 5(1a)(a)(ii)).
    """

    # Generates or manipulates realistic images, video, audio or similar
    # material. "Realistic" means a person's face, voice or body depicted in
    # a credible real-life manner; cartoonish or physically impossible
    # depictions do not count.
    realistic_media_generation: bool = False
    # Outputs can depict identifiable natural persons (a real face, voice or
    # body), whether from uploads, reference images, names or prompts.
    identifiable_persons: bool = False
    # Outputs can show intimate parts or sexually explicit activity, as a
    # reasonably foreseeable and reproducible outcome.
    intimate_depictions_possible: bool = False
    # Producing such depictions of identifiable persons is the system's
    # intended purpose (Art. 5(1a)(a)(i)), or the deployer uses it for that
    # purpose (Art. 5(1a)(b)).
    intimate_depictions_intended: bool = False
    # Outputs can depict children in material within the meaning of
    # Directive 2011/93/EU, Article 2, points (c) and (e).
    minors_depictions_possible: bool = False
    # The system only manipulates existing material in ways that neither
    # increase the exposure of depicted intimate parts nor alter the nature
    # of depicted sexually explicit activity (Art. 5(1b)): background
    # changes, captions, contrast or brightness. Not generation.
    manipulation_within_1b_only: bool = False
    safeguards: GenerativeMediaSafeguards = GenerativeMediaSafeguards()


class DeploymentContext(BaseModel, extra="forbid"):
    workplace: bool = False
    education: bool = False
    public_space: bool = False
    real_time_operation: bool = False
    law_enforcement_use: bool = False
    healthcare: bool = False
    financial_services: bool = False
    other: str | None = None


class Metadata(BaseModel, extra="forbid"):
    last_reviewed: date | None = None
    owner: str | None = None
    reviewed_by: str | None = None


class SystemDescription(BaseModel, extra="forbid"):
    name: str = Field(..., min_length=1)
    version: str = Field(..., min_length=1)
    provider: str = Field(..., min_length=1)
    deployer: str | None = None
    purpose: str = Field(..., min_length=1)
    system_description: str = Field(..., min_length=1)
    deployment_jurisdictions: list[str] = Field(..., min_length=1)
    output_consumed_in_eu: bool
    subject_population: SubjectPopulation
    inputs: SystemInputs = SystemInputs()
    outputs: SystemOutputs = SystemOutputs()
    deployment_context: DeploymentContext = DeploymentContext()
    generative_media: GenerativeMedia = GenerativeMedia()
    mitigations: list[str] = Field(default_factory=list)
    metadata: Metadata = Metadata()
