# ADAPTIVE_LEARNING_SPECIFICATION.md

# AQVERA — Adaptive Learning Specification

## Status: DECIDED (Core Architecture)

Adaptive Learning is AQVERA's central intelligence capability. It is designed as a real application subsystem, not as a collection of AI-generated recommendations. The system maintains a continuously updated model of the student's demonstrated academic knowledge.

## A. Learner Model

### Knowledge Levels (DECIDED)

The student's knowledge is represented at six levels:

1. **Course** — overall course mastery.
2. **Module** — module-level mastery.
3. **Topic** — topic-level mastery.
4. **Subtopic** — subtopic-level mastery (where applicable).
5. **Learning Objective** — individual objective mastery.
6. **Skill** — specific skill mastery (where applicable).

### Per-Objective Knowledge State (DECIDED)

Each `KnowledgeState` record includes:

| Field | Type | Description |
|-------|------|-------------|
| estimated_mastery | decimal(3,2) | 0.0–1.0 estimate of mastery |
| confidence | decimal(3,2) | 0.0–1.0 confidence in the estimate |
| evidence_count | integer | Number of evidence records |
| assessment_history | JSONB | Recent assessment attempts and outcomes |
| recent_performance | JSONB | Rolling window of scores |
| repeated_misconceptions | JSONB | Misconceptions observed multiple times |
| last_interaction_at | timestamp | Last interaction timestamp |
| retention_review_status | varchar | none, due, completed, overdue |
| prerequisites | JSONB | Prerequisite objective IDs with mastery levels |

### Mastery Rules (DECIDED)

- **No single correct answer proves mastery.** Mastery requires multiple evidence points across attempts and contexts.
- Mastery is updated incrementally as new evidence arrives, not recomputed from scratch each time.
- Confidence increases with evidence count and consistency; low confidence triggers more evidence collection.
- Retention reviews verify that mastery persists over time (knowledge decay).

## B. Learning Evidence Collection

### Evidence-Producing Interactions (DECIDED)

| Interaction | Evidence Type | Strength |
|-------------|--------------|----------|
| Correct answer | correct_answer | Direct |
| Incorrect answer | incorrect_answer | Direct |
| Answer confidence | confidence | Direct (self-reported) |
| Time spent (where meaningful) | time_spent | Behavioral |
| Hint usage | hint_usage | Behavioral |
| Number of attempts | attempts | Behavioral |
| Repeated mistakes | repeated_mistake | Direct |
| Activity completion | activity_completion | Direct |
| Delayed assessment performance | delayed_assessment | Direct |
| Application in new context | new_context_application | Direct |

### Direct vs. Behavioral Evidence (DECIDED)

- **Direct assessment evidence** — answers, delayed assessments, application in new context. Weighted higher in mastery estimation.
- **Weaker behavioral signals** — time spent, hint usage, attempts. Used as supporting signals, not primary mastery determinants.

### Evidence Collection Rules

- Every interaction that produces evidence creates a `LearningEvidence` record.
- Evidence records are immutable (see Data Integrity section).
- Evidence is linked to a `KnowledgeState` (objective level) and optionally to an `AssessmentAttempt`.
- Evidence strength (direct vs. behavioral) is stored and used in weighting.

## C. Knowledge Tracing

### Initial Algorithm: Rule-Based Mastery Estimation (PROPOSED)

A practical, explainable, rule-based approach is used initially. Bayesian Knowledge Tracing is a possible later enhancement (DEFERRED).

#### Algorithm Overview

For each knowledge state, mastery is estimated from evidence using weighted rules:

```
mastery_new = mastery_current + learning_rate * (evidence_signal - mastery_current)
```

Where:
- `evidence_signal` is derived from direct evidence (correct=1.0, incorrect=0.0, partial=0.5).
- Behavioral signals modulate the learning rate (e.g., many hints → lower confidence gain).
- `learning_rate` decreases as evidence_count increases (diminishing returns).
- Confidence increases with evidence_count and consistency of signal.

#### Factors Considered

| Factor | How It's Used |
|--------|---------------|
| Item difficulty | Harder items correct → stronger mastery signal; easier items incorrect → stronger negative signal |
| Assessment reliability | More reliable assessments (more questions, validated) → higher weight |
| Evidence confidence | Student self-reported confidence modulates weight |
| Knowledge decay | Mastery decays slowly over time without interaction |
| Retention | Delayed assessments verify mastery persists |

#### Assumptions (Documented, PROPOSED)

1. Evidence is conditionally independent given mastery (simplifying assumption).
2. Mastery is bounded [0, 1.0].
3. One correct answer suggests but does not prove mastery.
4. Incorrect answers on difficult items are weaker negative signals than incorrect answers on easy items.
5. Decay is exponential with a configurable half-life.
6. Behavioral signals are noisy and weighted lower than direct evidence.

#### Replaceability (DECIDED)

The knowledge tracing algorithm is behind an interface (`KnowledgeTracer`). It can be replaced with Bayesian Knowledge Tracing or another approach without changing the Adaptive Engine or Learner Model API.

## D. Adaptive Decision Engine

### Decision Pipeline (DECIDED)

A deterministic pipeline with explicit inputs, outputs, and fallback behavior.

#### Inputs
- Learner model (all knowledge states).
- Recent assessment evidence.
- Course structure and prerequisites.
- Student goals.
- Available study time (if configured).
- Current topic/objective.

#### Pipeline Steps

1. **Evidence sufficiency check** — Is there enough evidence to make a reliable judgment? If no → recommend more assessment/practice; report low confidence.
2. **Prerequisite check** — Are required prerequisites mastered? If no → recommend prerequisite review.
3. **Mastery threshold check** — Is current objective mastered (mastery ≥ threshold, confidence ≥ threshold)? If yes → advance; if no → review.
4. **Difficulty selection** — Select difficulty based on estimated mastery and recent performance.
5. **Activity selection** — Choose the most useful instructional activity (lesson, practice, explanation, visualization).
6. **Explanation decision** — Provide another explanation if misconceptions detected or confidence low.
7. **Retention review** — Schedule retention review if mastery was recently achieved and decay is a risk.

#### Outputs

| Output | Description |
|--------|-------------|
| next_objective | The learning objective to study next |
| prerequisite_attention | Prerequisite needing attention (if any) |
| review_or_advance | Whether to review or advance |
| difficulty_level | Appropriate difficulty level |
| provide_explanation | Whether to provide another explanation |
| instructional_activity | Most useful activity type |
| retention_review | When a retention review should occur |
| rationale | Text explanation of why this decision was made |
| evidence_confidence | Confidence in the decision |

#### Fallback Behavior

| Situation | Fallback |
|-----------|----------|
| Insufficient evidence | Recommend assessment/practice; report "not enough evidence" |
| Prerequisite data missing | Assume prerequisite not mastered; recommend review |
| AI unavailable | Use cached learner model; rule-based decision only |
| No clear recommendation | Default to review of current weakest objective |

### AI Boundaries (DECIDED)

- AI may help interpret errors and generate educational content.
- AI must **not** independently invent mastery scores.
- AI must **not** silently modify the learner model.
- The Adaptive Engine makes final decisions; AI provides input only.

## E. Personalized Learning Path

### Generation Inputs (DECIDED)

- Course structure (modules, lessons, topics, objectives).
- Learning objectives and their descriptions.
- Prerequisite relationships.
- Student mastery (from learner model).
- Student goals (target objectives, target date).
- Available study time (if configured).
- Assessment evidence (from learner model).

### Path Structure

```
LearningPath {
  id: UUID
  learner_model_id: UUID
  course_id: UUID
  path_data: JSONB {
    activities: [
      {
        objective_id: UUID
        activity_type: "lesson" | "practice" | "assessment" | "visualization" | "review"
        rationale: string
        estimated_minutes: integer
        order: integer
      }
    ]
    total_estimated_minutes: integer
    target_completion_date: date?
  }
  status: "active" | "completed" | "abandoned"
}
```

### Explainability (DECIDED)

The student must understand why an activity is recommended. Each activity in the path includes a `rationale` field explaining:
- Which objective it serves.
- What mastery gap it addresses.
- Why this activity type was selected.
- What evidence supports the recommendation.

### Prerequisite Enforcement

The path respects the prerequisite graph: an objective is not recommended until its prerequisites are mastered (or the student overrides with acknowledgment).

## F. Adaptive Feedback

### Feedback Content (DECIDED)

Adaptive feedback communicates:

| Element | Description |
|---------|-------------|
| What the student understands | Mastered objectives with evidence summary |
| What remains weak | Objectives below mastery threshold |
| Why a recommendation was selected | Rationale tied to evidence and decision pipeline |
| What to do next | Specific next activity with rationale |
| Evidence sufficiency | Whether the system has enough evidence for a reliable judgment |

### Avoiding Misleading Precision (DECIDED)

- Mastery estimates are presented as ranges or qualitative levels (beginning, developing, proficient, mastered) rather than false precision (e.g., "0.734").
- Confidence levels are communicated honestly.
- When evidence is insufficient, the system states this explicitly rather than guessing.

### Feedback Delivery

Feedback is delivered through:
- The AI Tutor Interface (context-aware).
- The Learning Progress and Analytics page.
- Adaptive recommendations after each assessment.
- Retention review reminders.

## G. Data Integrity

### Evidence Immutability (DECIDED)

- Learning evidence records are **immutable** once created.
- Corrections are represented as **new records** with `correction_of_id` pointing to the original.
- The original record is never modified or deleted.
- `is_immutable = true` on all evidence records; `correction_of_id` is nullable.

### Reproducibility (DECIDED)

- Learner-model calculations are reproducible from the evidence log.
- Given the same `LearningEvidence` records and the same algorithm version, the same `KnowledgeState` results.
- Algorithm version is stored with each `KnowledgeState` update (via `methodology_version_id` on `LearnerModels`).

### No Silent Rewrites (DECIDED)

- The adaptive system must never silently rewrite historical assessment results.
- `AssessmentAttempts`, `StudentResponses`, and `EvaluationResults` are immutable once completed.
- Any correction creates a new record, not an update.

### Audit Trail

- All changes to learner model, knowledge states, and evidence are recorded in `AuditEvents`.
- Each audit event captures: user, event type, entity type, entity ID, old values, new values, timestamp.

## Summary of Adaptive Decisions (DECIDED)

| Question | Who Decides | Basis |
|----------|-------------|-------|
| What should the student learn next? | Adaptive Engine | Learner model + prerequisites + evidence |
| Which prerequisite needs attention? | Adaptive Engine | Prerequisite graph + mastery states |
| Should the student review or advance? | Adaptive Engine | Mastery threshold + confidence |
| What difficulty level is appropriate? | Adaptive Engine | Estimated mastery + recent performance |
| Should the system provide another explanation? | Adaptive Engine | Misconceptions + low confidence |
| Which instructional activity is most useful? | Adaptive Engine | Objective + activity type + evidence |
| When should a retention review occur? | Adaptive Engine | Decay model + last review date |
| AI generates content? | AI (via Teaching Engine) | Structured contracts, validated |
| AI assigns mastery? | Never | Adaptive Engine only |
