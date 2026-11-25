# TESTING_STRATEGY.md

# AQVERA — Testing Strategy

## Testing Pyramid

Unit → Integration → End-to-End → AI Evaluation → Regression.

## A. Unit Testing

**Domains:** Domain logic, adaptive decisions, scoring, validation, teaching workflow rules.

**What to test:**
- Password hashing and verification.
- Session validation and expiration.
- Rule-based mastery estimation (knowledge tracer).
- Adaptive decision pipeline (each step + fallback).
- Scoring (deterministic for MCQ, numerical, math).
- Question validation (deduplication, ambiguity flags).
- Teaching workflow rules (no single answer = mastery; no fixed learning styles).
- Schema validation for structured AI outputs.
- Visualization data transformation.
- Content chunking and extraction logic.

**Location:** Backend unit tests (pytest).

---

## B. Integration Testing

**Domains:** Database interactions, file storage, document processing, AI provider adapters, retrieval, background jobs.

**What to test:**
- PostgreSQL schema and migrations.
- File upload → storage → processing job flow.
- Document extraction → sections → chunks → embeddings → vector index.
- AI provider adapters (normalization, retries, fallbacks, error classification).
- Vector search retrieval (pgvector similarity).
- Background job status/progress/retry/failure reasons.
- Assessment lifecycle (attempt → evaluation → evidence → learner model update).
- Learning context service (set/read/clear).

**Location:** Backend integration tests (pytest + test database).

---

## C. End-to-End Testing

**Domains:** Account creation, course creation, file upload, course generation, course review, learning activities, assessment, learner model update.

**Critical E2E workflows:**
1. Register → Login → Dashboard (empty state).
2. Upload document → Processing status → Course generated → Review/Edit → Publish.
3. Open course → View lesson → Complete assessment → Learner model updated → Adaptive recommendation with rationale.
4. Open AI Tutor with context → Tutor understands recent mistakes → Explanation generated with sources.
5. View mathematical visualization → Associated with learning objective.

**Location:** Playwright (frontend E2E).

**Acceptance criteria per workflow** defined in MVP_SCOPE.md per phase.

---

## D. AI Evaluation

**Domains:** Teaching quality, groundedness, citation correctness, question quality, mathematical correctness, structured output validity, prompt injection resistance.

**Approach:**
- Representative academic test cases (not hand-picked examples).
- Versioned evaluation datasets.
- Repeatable test cases.
- Automated checks where possible; human review for subjective quality.

**Test categories:**
- Teaching quality: Does generated lesson follow methodology? Are validation rules met?
- Groundedness: Are claims traceable to source material?
- Citation correctness: Do source attributions reference real sections/pages?
- Question quality: Are questions aligned to objectives? Unambiguous? Appropriate difficulty?
- Mathematical correctness: Are numerical/math answers validated deterministically?
- Structured output validity: Do all AI outputs pass JSON schema validation?
- Prompt injection resistance: Can uploaded document content override system instructions? (Must be no.)

**Location:** AI evaluation test suite (pytest + LLM judges where appropriate).

---

## E. Regression Testing

**Approach:**
- Versioned evaluation datasets stored in repository.
- Repeatable test cases for every core workflow.
- Detection of quality degradation after prompt or model changes.
- Run regression suite on any AI provider or model change.

---

## Test Coverage Targets

| Layer | Target |
|-------|--------|
| Unit | 80%+ of domain logic |
| Integration | All database, storage, processing, AI adapter paths |
| E2E | All core workflows (register, upload, course, assessment, adaptive) |
| AI Evaluation | Representative academic cases per domain |

---

## Test Execution

- Unit tests: run on every change (fast).
- Integration tests: run on PR/commit.
- E2E tests: run before release.
- AI evaluation: run on model/prompt changes.

**Never claim tests passed without running them.** (AGENTS.md rule)
