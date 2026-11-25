# STANDARD_TEACHING_METHODOLOGY.md

# AQVERA — Standard Teaching Methodology

## Status: DECIDED (Core Standard)

The Standard Teaching Methodology is the single, versioned instructional standard applied consistently across all academic domains. Domain-specific teaching profiles add instructional behavior without changing the core standard.

## Core Principle

The platform owns the learning experience. AI models provide capabilities, academic materials provide evidence, teaching methodology provides instructional consistency, and the adaptive engine determines the next useful learning step. No single AI model controls the entire academic experience.

## Methodology Versioning (DECIDED)

- Methodology versions are stored in `TeachingMethodologyVersions` with semantic versioning.
- Each course references a specific methodology version.
- Changes to the methodology create a new version; existing courses remain on their version until migrated.
- The active version per teaching profile is tracked in `TeachingProfiles.is_active`.

## Structured Teaching Workflows

The methodology defines explicit workflows for:

1. **Lesson delivery** — present concept → check understanding → provide practice → give feedback.
2. **Assessment administration** — generate questions → validate → attempt → evaluate → record evidence → update learner model.
3. **Adaptive decision** — read learner model → apply decision pipeline → produce recommendation → explain rationale.
4. **Error remediation** — identify misconception → provide targeted explanation → re-assess.
5. **Retention review** — schedule delayed assessment → evaluate retention → adjust mastery/confidence.

Each workflow has:
- Explicit inputs and outputs.
- Validation rules.
- Fallback behavior when evidence is insufficient.
- AI usage boundaries (AI generates content; methodology governs instruction).

## Output Contracts (DECIDED)

All teaching-relevant outputs conform to structured contracts validated by schema:

| Contract | Fields (representative) |
|----------|------------------------|
| Lesson | objective_id, concept, explanation, examples, practice_activities, sources, checks_for_understanding |
| Practice Activity | activity_type, prompt, expected_response, validation_rules, difficulty, hints |
| Explanation | concept, audience_level, steps, misconceptions_addressed, source_attribution, confidence |
| Feedback | what_understood, what_weak, why_recommended, next_steps, evidence_sufficiency |

## Validation Rules (DECIDED)

Teaching quality is enforced by rules, not exclusively by prompt instructions:

- **No single correct answer proves mastery.** Mastery requires multiple evidence points across attempts and contexts.
- **No fixed learning-style categories.** Preferences and patterns are observed over time, not assumed (no visual/auditory/kinesthetic labels).
- **Evidence strength distinguished.** Direct assessment evidence is weighted higher than behavioral signals (hint usage, time spent).
- **Confidence reported.** Every mastery estimate includes a confidence score; low confidence triggers more evidence collection.
- **Prerequisites checked.** A student cannot advance past an objective if required prerequisites are unmastered (unless override configured).
- **Misconceptions tracked.** Repeated errors on the same concept are recorded as misconceptions and trigger targeted remediation.
- **Retention reviews scheduled.** Delayed assessments verify retention; mastery decays without review.

## Evaluation Criteria (DECIDED)

Teaching output is evaluated on:

| Criterion | Description |
|-----------|-------------|
| Groundedness | Claims and examples traceable to source material. |
| Citation correctness | Source attributions reference real sections/pages. |
| Question quality | Questions aligned to learning objectives; unambiguous; difficulty appropriate. |
| Mathematical correctness | Numerical/math answers validated deterministically. |
| Structured output validity | All AI outputs pass JSON schema validation. |
| Prompt injection resistance | Uploaded document content cannot override system instructions. |

## Domain-Specific Instructional Behavior

Domain teaching profiles extend the standard with:

- Domain-specific terminology and concept ordering.
- Domain-appropriate activity types (e.g., code exercises for CS, diagrams for math, timelines for history).
- Domain-specific visualizations.
- Domain-specific misconception patterns.

The core methodology (mastery estimation, evidence rules, decision pipeline) remains unchanged across domains.

## AI Boundaries in Teaching (DECIDED)

| AI May | AI Must Not |
|--------|-------------|
| Generate lesson content, examples, explanations | Independently assign mastery scores |
| Suggest practice activities | Silently modify the learner model |
| Interpret student errors | Override validation rules |
| Generate assessment questions (validated) | Bypass output contracts/schema validation |
| Recommend next steps (as input to engine) | Make final adaptive decisions without engine |

The Adaptive Engine makes final learning decisions. AI provides input; the engine decides.

## Evidence-Based Preferences (DECIDED)

Instead of fixed learning styles, the system observes:

- Interaction patterns (time of day, session length, attempt patterns).
- Response to activity types (which activities lead to better outcomes).
- Hint usage patterns (when hints help vs. when they indicate confusion).
- Format preferences observed through engagement, not self-declaration.

These patterns are stored in `UserPreferences` and `LearnerModels` as derived data, not as fixed categories.
