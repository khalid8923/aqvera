# Adaptive Learning

## Overview

The adaptive learning engine is evidence-based and deterministic. AI never
assigns mastery scores or silently modifies the learner model. Mastery comes
from deterministic rules applied to structured learning evidence.

## Knowledge Levels

1. Course — overall course mastery.
2. Module — module-level mastery.
3. Topic — topic-level mastery.
4. Subtopic — subtopic-level mastery.
5. Learning Objective — individual objective mastery.
6. Skill — specific skill mastery.

## Knowledge State

Each `KnowledgeState` tracks:
- `estimated_mastery` (0.0–1.0)
- `confidence` (0.0–1.0)
- `evidence_count`
- `recent_performance` (rolling window)
- `repeated_misconceptions`
- `last_interaction_at`
- `retention_review_status`

## Mastery Rules (Deterministic)

- No single correct answer proves mastery. Multiple evidence points required.
- `mastery_new = mastery + learning_rate * weight * (signal - mastery)`
- Learning rate decreases as evidence count increases (diminishing returns).
- Confidence grows with evidence count and consistency.
- Direct evidence weighted higher than behavioral signals.

## Adaptive Decision Pipeline

1. Evidence sufficiency check (≥ 3 evidence records for reliable judgment).
2. Prerequisite check (prerequisites must be mastered to advance).
3. Mastery threshold check (mastery ≥ 0.70 AND confidence ≥ 0.60 → advance).
4. Difficulty selection (easy/medium/hard based on estimated mastery).
5. Activity selection (lesson/practice/assessment/visualization/review).
6. Explanation decision (misconceptions or low confidence → explanation).
7. Retention review (schedule if recently mastered).

## Recommendation Outputs

- `next_objective`, `prerequisite_attention`, `review_or_advance`,
  `difficulty_level`, `provide_explanation`, `instructional_activity`,
  `retention_review`, `rationale`, `evidence_confidence`.

## AI Boundaries

- AI may interpret errors and generate content.
- AI must **not** invent mastery scores.
- AI must **not** silently modify the learner model.
- The Adaptive Engine makes final decisions; AI provides input only.

## Testing

Unit tests verify mastery updates, threshold checks, weak-topic detection, and
recommendation rationale — all deterministic, no AI required.

## Provider Status

No AI provider involved in core mastery calculations. Fully testable offline.
