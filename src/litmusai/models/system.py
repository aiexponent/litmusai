"""Input models for LitmusAI screening: PRD §7.1."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, Field, field_validator

_POPULATION_CATEGORIES = frozenset(
    {
        "general_public",
        "minors",
        "workers",
        "students",
        "persons_with_disabilities",
        "persons_in_vulnerable_economic_situations",
        "older_persons",
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


# An answer to one legal question. "not_answered" is the default, so a file
# written before the question existed keeps the verdict it had (1.1.x files).
# "not_sure" screens amber: a reviewer decides.
# YAML 1.1 reads an unquoted yes or no as a boolean, so true and false are
# accepted and stored as "yes" and "no".


def _answer_from_yaml(value: Any) -> Any:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return value


Answer = Annotated[
    Literal["yes", "no", "not_sure", "not_answered"], BeforeValidator(_answer_from_yaml)
]


class Influence(BaseModel, extra="forbid"):
    """The elements of Art. 5(1)(a) and (b), one question each.

    Answer for the system as placed on the market, put into service or used.
    Point (a) needs a technique, material distortion and significant harm;
    point (b) needs exploitation of a vulnerability, material distortion and
    significant harm.
    """

    # (a) Subliminal techniques beyond a person's consciousness: stimuli a
    # person cannot perceive, such as flashed images or inaudible audio.
    subliminal_techniques: Answer = "not_answered"
    # (a) Purposefully manipulative or deceptive techniques: they subvert or
    # impair a person's autonomy, decision-making or free choice, or deceive.
    # Also when nobody intended it, such as behaviour learned in training;
    # not merely incidental behaviour the provider has measures against
    # (Commission guidelines C(2025) 5052, para. 69).
    manipulative_or_deceptive_techniques: Answer = "not_answered"
    # (b) Exploits a vulnerability of a person or group due to their age
    # (children or older people), a disability, or a specific social or
    # economic situation. Other weak points belong under (a) (para. 125).
    exploits_vulnerability: Answer = "not_answered"
    # (a), (b) Has the objective or the effect (intent is not needed,
    # para. 76) of materially distorting behaviour: people take a decision
    # they would not otherwise have taken.
    materially_distorts_behaviour: Answer = "not_answered"
    # (a), (b) Causes or is reasonably likely to cause significant harm to
    # that person, another person or a group: physical, psychological or
    # financial.
    significant_harm_likely: Answer = "not_answered"


class Scope(BaseModel, extra="forbid"):
    """Exceptions and limits written in Art. 5(1), points (d) to (h).

    A "no" that takes the system outside a prohibition clears that point.
    A "yes" to an exception that needs evidence gives amber for review.
    """

    # Who is screening. Point (h) prohibits use, not placing on the market:
    # a provider that only sells a system declares provider_only. A private
    # person using a tool declares deployer; build-and-use declares both.
    role: Literal["provider_only", "deployer", "both"] = "both"
    # (d) The system supports a human assessment of a person's involvement
    # in a criminal activity that is already based on objective and
    # verifiable facts directly linked to that activity. "yes" gives amber.
    human_assessment_on_verifiable_facts: Answer = "not_answered"
    # (e) Facial images are collected without a target: "no" for a search
    # for one person or one defined group (targeted). "no" clears (e).
    untargeted_collection: Answer = "not_answered"
    # (e) The system creates or expands a facial recognition database.
    # "no", for example training a generator of fictitious faces, clears (e).
    builds_facial_recognition_database: Answer = "not_answered"
    # (f) The emotions inferred are those of workers (employees, contractors,
    # trainees, volunteers, job candidates; guidelines para. 254) or of pupils
    # and students (para. 255). "no" (only customers, patients or the public)
    # clears (f).
    emotions_of_workers_or_students: Answer = "not_answered"
    # (f) The system is put in place for medical or safety reasons.
    # "yes" gives amber.
    medical_or_safety_reasons: Answer = "not_answered"
    # (g) The system only labels or filters lawfully acquired biometric
    # datasets, or categorises biometric data in the area of law
    # enforcement. "yes" gives amber.
    dataset_labelling_or_filtering_only: Answer = "not_answered"
    # (h) Identification happens at a distance without the person's active
    # involvement. "no" (a person steps up to a gate or sensor) clears (h).
    remote_identification: Answer = "not_answered"
    # (h) Used for the purposes of law enforcement as defined in Art. 3(46).
    # "no" clears (h).
    law_enforcement_purpose: Answer = "not_answered"
    # (h) Each use is strictly necessary for one of the objectives in
    # Art. 5(1)(h)(i) to (iii): a targeted search for victims or missing
    # persons, a specific imminent threat or terrorist attack, or a suspect
    # of a serious offence in Annex II. "yes" gives amber; Art. 5(2) and (3)
    # add authorisation and an impact assessment.
    article_5_1_h_objective: Answer = "not_answered"


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
    influence: Influence = Influence()
    scope: Scope = Scope()
    mitigations: list[str] = Field(default_factory=list)
    metadata: Metadata = Metadata()
