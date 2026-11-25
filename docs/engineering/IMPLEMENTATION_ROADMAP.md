# IMPLEMENTATION_ROADMAP.md

# AQVERA — Implementation Roadmap

## Overview

Six phases (A–F) deliver a functional, private, self-hosted academic learning application. Phase 0 (documentation/architecture) is complete.

## Phase A — Core Functional Foundation

**Objective:** Establish the application skeleton, authentication, database, and core module boundaries.

**Required Modules:** Identity, Authentication, Database layer, Configuration, Logging.

**Dependencies:** None.

**Deliverables:** Next.js + FastAPI running; PostgreSQL schema; register/login/logout; AGENTS.md; structured logging.

**Acceptance Criteria:** User can register/login/logout; session expires; migrations apply cleanly; structured logging active.

**Tests:** Unit (password hashing, session validation); Integration (database connections, migrations).

**Limitations:** No academic content, no AI, no adaptive engine.

**Completion:** Authentication works end-to-end; schema versioned via migrations.

---

## Phase B — Complete Academic Content Pipeline

**Objective:** Material upload, document processing, course generation, course review/editing.

**Required Modules:** Material Upload, Document Extraction/OCR, Chunking, Embedding, Vector Search (pgvector), Course Structure Generation, Course Review/Editing.

**Dependencies:** Phase A; AI Provider Abstraction Layer (layer defined; no provider adapter required yet).

**Deliverables:** File upload with validation; processing jobs with status/progress/retry; extracted sections/chunks/embeddings/source references; proposed course structure; course review UI.

**Acceptance Criteria:** Student uploads document and sees processing status; system extracts sections and embeddings; system proposes course with objectives; student reviews/edits; failures have explicit status and retry.

**Tests:** Integration (file upload, processing, vector indexing); Unit (chunking, extraction); AI evaluation (course structure quality, groundedness).

**Limitations:** Single domain (mathematics); no assessment/adaptive yet; limited visual tools.

**Completion:** A course can be generated from uploaded material and saved.

---

## Phase C — Teaching and AI Capabilities

**Objective:** Teaching methodology, AI orchestration, provider abstraction, retrieval, content generation.

**Required Modules:** AI Provider Abstraction Layer, AI Orchestration, Teaching Engine, Knowledge Retrieval, Content Generation, Structured Output Contracts.

**Dependencies:** Phase B; initial AI provider selected.

**Deliverables:** Provider abstraction with ≥1 adapter; structured contracts (course structure, topic extraction, objectives, lesson, questions, error classification, explanation, source attribution); teaching workflow rules; safe handling for malformed JSON/incomplete responses/unsupported capabilities/provider failures.

**Acceptance Criteria:** AI outputs validated against contracts before use; provider fallback works; teaching methodology applied consistently; no AI output bypasses validation.

**Tests:** Unit (providers, schema validation); Integration (orchestration, retrieval, generation); AI evaluation (teaching quality, groundedness, citations, prompt injection resistance).

**Limitations:** No assessment/adaptive yet; visual tools limited.

**Completion:** Content generated and validated through teaching engine with working AI provider.

---

## Phase D — Assessment and Adaptive Learning

**Objective:** Assessments, evaluation, learner model, knowledge tracing, adaptive engine, learning paths, feedback.

**Required Modules:** Assessments/Questions/AnswerKeys, Attempts/Responses/Evaluation, Question Validation, Difficulty Classification, Deterministic Validation (numerical/math), Subjective Evaluation (criteria+confidence), Learner Models/Knowledge States/Learning Evidence, Rule-Based Knowledge Tracing, Adaptive Decision Engine, Learning Paths, Retention Reviews, Adaptive Feedback.

**Dependencies:** Phase C; learner model data model.

**Deliverables:** 9 assessment types; full assessment lifecycle; learner model at 6 levels; rule-based knowledge tracing; adaptive decision pipeline; personalized learning path with rationale; adaptive feedback.

**Acceptance Criteria:** Assessment results update learner model; recommendations include rationale and evidence confidence; evidence immutable; no single correct answer proves mastery; no fixed learning styles; deterministic validation for math/numerical.

**Tests:** Unit (scoring, adaptive decisions, knowledge tracing, validation); Integration (assessment lifecycle, learner model updates); E2E (assessment → evidence → learner model → recommendation); AI evaluation (question quality, math correctness, structured output validity).

**Limitations:** Bayesian Knowledge Tracing deferred; programming code execution sandbox deferred.

**Completion:** Student completes assessment and receives adaptive recommendation with rationale.

---

## Phase E — Visual Learning Tools

**Objective:** Visual Learning Framework with most valuable initial capability.

**Required Modules:** Visual Learning Interface, Deterministic Visualization Rendering (function graphing/equation visualization), Reusable Visualization Interface, Learning Context integration.

**Dependencies:** Phase D; frontend visualization library.

**Deliverables:** Function graphing/equation visualization (mathematics); distinction between deterministic/AI-generated/static/interactive; visual activities linked to objectives.

**Acceptance Criteria:** Mathematical visualization renders deterministically; associated with learning objective; visualization types clearly distinguished.

**Tests:** Unit (visualization data transformation); Integration (visual activity → objective association).

**Limitations:** Only initial capability; other domains deferred.

**Completion:** Student views deterministic mathematical visualization linked to objective.

---

## Phase F — Hardening and Private Deployment

**Objective:** Security hardening, observability, testing completeness, private deployment.

**Required Modules:** Security (auth, authorization, file, AI, privacy), Observability (logging, metrics, AI cost tracking), Complete Test Suite, Docker Compose Deployment.

**Dependencies:** All previous phases.

**Deliverables:** Security review passed; structured logging; full regression suite; Docker Compose deployment; updated DECISION_LOG.

**Acceptance Criteria:** All core workflows have passing E2E tests; security applied to all modules; logging excludes sensitive content; app deployable privately via Docker Compose.

**Tests:** Full regression; AI evaluation with representative academic cases; Security tests (auth, authorization, file upload, prompt injection).

**Limitations:** Private operation only; no multi-tenancy; no public SaaS.

**Completion:** Application runnable privately; all acceptance criteria pass.

---

## Phase Dependencies Summary

```
A → B → C → D → E → F
  ↑         ↑
  └── AI Provider Abstraction (B→C)
```

## Smallest Coherent Vertical Slice (MVP)

Phases A + B + C (partial) + D (assessment → learner model → recommendation) for a single mathematics course proves the complete academic workflow.
