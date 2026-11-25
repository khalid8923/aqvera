# ASSESSMENT_SYSTEM.md

# AQVERA — Assessment System

## Purpose

Design an assessment subsystem that produces meaningful academic evidence for the learner model and adaptive engine.

## Supported Assessment Types (DECIDED)

| Type | Description | Validation |
|------|-------------|------------|
| Multiple Choice Questions | Single correct option | Deterministic (option key match) |
| Multiple Select Questions | Multiple correct options | Deterministic (set match) |
| True/False | Binary choice | Deterministic |
| Short Answer | Text response | Deterministic (exact/normalized) or subjective (criteria + confidence) |
| Numerical Problems | Numeric answer | Deterministic (with tolerance) |
| Mathematical Expressions | Symbolic math answer | Deterministic (expression equivalence) |
| Programming Exercises | Code solution | Not executed in main process; evaluated by criteria or external sandbox (deferred) |
| Language Exercises | Language-specific response | Subjective (criteria + confidence) |
| Conceptual Questions | Open-ended conceptual response | Subjective (criteria + confidence) |

## Assessment Lifecycle (DECIDED)

1. **Assessment Generation** — Questions generated linked to course content and learning objectives.
2. **Question Validation** — Questions checked for ambiguity, duplication, and alignment.
3. **Difficulty Classification** — Questions classified by difficulty (linked to objectives).
4. **Student Attempt** — Student answers questions; no correct answers shown before completion (unless activity permits).
5. **Answer Evaluation** — Deterministic for numerical/math; criteria + confidence for subjective.
6. **Feedback Generation** — Feedback generated with rationale.
7. **Evidence Recording** — Learning evidence recorded (immutable).
8. **Learner Model Update** — Adaptive engine updates knowledge states.

## Key Requirements (DECIDED)

### Traceability
- Question generation is linked to course content and learning objectives.
- Questions store `source_reference_id` where possible (traceable to source material).
- Answer keys and scoring criteria stored independently from question presentation (`AnswerKeys` table separate from `Questions`).

### Deterministic Validation
- Numerical and mathematical answers use deterministic validation when possible.
- `AnswerKeys.validation_method` indicates the method: `deterministic`, `subjective`, `regex`, `numeric_tolerance`.
- `AnswerKeys.tolerance` for numerical answers.

### Programming Assessment Security
- Programming assessment must not execute untrusted code directly inside the main application process.
- Code evaluation deferred to external sandbox or criteria-based evaluation (not in MVP).

### Subjective Evaluation
- Subjective evaluation exposes its criteria and confidence.
- `EvaluationResults.confidence` = system confidence in the evaluation.
- `EvaluationResults.criteria_met` = which criteria were satisfied.

### Question Quality
- Incorrect or ambiguous questions identifiable and reportable (`Questions.is_ambiguous`, `Questions.is_reported`).
- Question deduplication supported.
- Coverage analysis: ensure all learning objectives have adequate question coverage.

### Answer Security
- Students must not receive the correct answer before completing an assessment unless the activity explicitly permits it (`Assessments.show_answers_after`).

## Data Flow

```
Question Generation (AI + validated contract)
       ↓
Question Validation (deterministic rules + AI review)
       ↓
Difficulty Classification (based on objective + historical performance)
       ↓
Student Attempt (answers collected; no answer key revealed)
       ↓
Answer Evaluation (deterministic for math/numerical; criteria+confidence for subjective)
       ↓
Feedback Generation (with rationale; sources attributed)
       ↓
Evidence Recording (immutable LearningEvidence records)
       ↓
Learner Model Update (Adaptive Engine updates KnowledgeStates)
```

## Quality Checks

| Check | Description |
|-------|-------------|
| Question deduplication | Detect duplicate or near-duplicate questions |
| Difficulty estimation | Classify easy/medium/hard based on objective level + historical data |
| Coverage analysis | Ensure each learning objective has sufficient question coverage |
| Ambiguity detection | Flag questions reported as ambiguous by students |
| Source traceability | Verify questions link to source material where possible |

## Storage

- `Assessments` — assessment metadata.
- `Questions` — question stem, type, difficulty, source reference.
- `QuestionOptions` — options for MCQ/multiple select.
- `AnswerKeys` — correct answers, scoring criteria, validation method, tolerance (independent from question presentation).
- `AssessmentAttempts` — attempt records with idempotency key.
- `StudentResponses` — student answers, confidence, time spent, attempt number.
- `EvaluationResults` — correctness, score, confidence, method, feedback, criteria met.

## Immutable Records

- `AssessmentAttempts`, `StudentResponses`, `EvaluationResults` are immutable once completed.
- Corrections create new records; originals are never modified.
