# MVP_SCOPE.md

# AQVERA — MVP Scope

## Objective

The smallest coherent vertical slice that proves the complete academic workflow:
**Upload material → Generate course → Review lesson → Complete assessment → Update learner model → Receive adaptive recommendation.**

## Initial Domain: Mathematics (PROPOSED)

Mathematics is recommended as the first domain because it offers:
- High academic usefulness.
- Deterministic validation for numerical and mathematical answers.
- Strong visual learning opportunities (function graphing, equation visualization).
- Representative materials readily available.
- Clear learning objectives and prerequisite relationships.

## Phase A — Core Functional Foundation

### Objective
Establish the application skeleton, authentication, database, and core module boundaries.

### Required Modules
- Identity (users, profiles, preferences, sessions).
- Authentication (password hashing, session management, token expiration).
- Database layer (PostgreSQL, migrations, transactions).
- Configuration and secret management.
- Logging and observability foundation.

### Dependencies
- None (foundation phase).

### Deliverables
- Running Next.js frontend + FastAPI backend.
- PostgreSQL database with core schema.
- Authentication flow (register, login, logout).
- AGENTS.md and engineering workflow in place.

### Acceptance Criteria
- User can register, log in, and log out.
- Session expires after configured timeout.
- Database migrations apply cleanly.
- Structured logging is active.

### Automated Tests
- Unit tests for password hashing, session validation.
- Integration tests for database connections and migrations.

### Known Limitations
- No academic content yet.
- No AI integration.
- No adaptive engine.

### Completion Conditions
- Authentication works end-to-end.
- Database schema is versioned via migrations.

---

## Phase B — Complete Academic Content Pipeline

### Objective
Enable material upload, document processing, course generation, and course review/editing.

### Required Modules
- Material Upload and Processing Center (file validation, storage, processing jobs).
- Document extraction and OCR (Python libraries).
- Content chunking and embedding generation.
- Vector search (pgvector).
- Course structure generation (linked to learning objectives).
- Generated Course Review and Editing.

### Dependencies
- Phase A (authentication, database, storage).
- AI Provider Abstraction Layer (initial provider adapter).

### Deliverables
- File upload with validation (type, size, malicious file considerations).
- Document processing jobs with status/progress/retry/failure reasons.
- Extracted sections, content chunks, embeddings, source references.
- Proposed course structure from uploaded material.
- Course review and editing interface.

### Acceptance Criteria
- Student can upload a document and see processing status.
- System extracts sections and generates embeddings.
- System proposes a course structure with learning objectives.
- Student can review and edit the proposed course.
- Processing failures have explicit statuses and retry behavior.

### Automated Tests
- Integration tests for file upload, document processing, vector indexing.
- Unit tests for content chunking, extraction logic.
- AI evaluation for course structure quality and groundedness.

### Known Limitations
- Single domain (mathematics).
- Limited visual tools.
- No assessment or adaptive engine yet.

### Completion Conditions
- A course can be generated from uploaded material and saved.

---

## Phase C — Teaching and AI Capabilities

### Objective
Implement the teaching methodology, AI orchestration, provider abstraction, retrieval, and content generation.

### Required Modules
- AI Provider Abstraction Layer (configuration, model selection, credentials, normalization, structured output, streaming, token/usage tracking, cost estimation, timeouts, retries, rate limiting, error classification, availability, fallbacks, capability metadata).
- AI Orchestration (model, tool, workflow selection).
- Teaching Engine (applies versioned teaching methodology).
- Knowledge Retrieval (retrieves academic evidence).
- Content Generation (lessons, examples, explanations, practice materials).
- Structured output contracts with schema validation.

### Dependencies
- Phase B (content pipeline, vector search).
- Initial AI provider selected.

### Deliverables
- Provider abstraction layer with at least one working adapter.
- Structured contracts for course structure, topic extraction, learning objectives, lesson generation, question generation, error classification, explanation generation, source attribution.
- Teaching workflow rules applied consistently.
- Safe handling for malformed JSON, incomplete responses, unsupported capabilities, provider failures.

### Acceptance Criteria
- AI outputs validated against structured contracts before use.
- Provider fallback works when primary provider is unavailable.
- Teaching methodology applied consistently across generated content.
- No AI output bypasses application validation.

### Automated Tests
- Unit tests for provider adapters, structured output validation.
- Integration tests for AI orchestration, retrieval, content generation.
- AI evaluation for teaching quality, groundedness, citation correctness, prompt injection resistance.

### Known Limitations
- Assessment and adaptive engine not yet implemented.
- Visual tools limited.

### Completion Conditions
- Content can be generated and validated through the teaching engine with a working AI provider.

---

## Phase D — Assessment and Adaptive Learning

### Objective
Implement assessments, evaluation, learner model, knowledge tracing, adaptive decision engine, learning paths, and feedback.

### Required Modules
- Assessments, questions, options, answer keys.
- Assessment attempts, student responses, evaluation results.
- Question validation, difficulty classification.
- Deterministic validation for numerical/mathematical answers.
- Subjective evaluation with criteria and confidence.
- Learner models, knowledge states, learning evidence.
- Rule-based knowledge tracing (replaceable).
- Adaptive Decision Engine (deterministic pipeline).
- Learning Paths, Retention Reviews.
- Adaptive Feedback.

### Dependencies
- Phase C (teaching engine, content generation).
- Learner model data model.

### Deliverables
- Multiple assessment types (MCQ, multiple select, T/F, short answer, numerical, math expression, programming, language, conceptual).
- Full assessment lifecycle (generation → validation → difficulty → attempt → evaluation → feedback → evidence → learner model update).
- Learner model at course, module, topic, subtopic, objective, skill levels.
- Rule-based knowledge tracing with documented assumptions.
- Adaptive decision pipeline with inputs, outputs, fallback behavior.
- Personalized learning path with rationale.
- Adaptive feedback communicating understanding, weaknesses, rationale, next steps, evidence sufficiency.

### Acceptance Criteria
- Assessment results update the learner model.
- Adaptive recommendations include rationale and evidence confidence.
- Evidence records are immutable; corrections are new records.
- No single correct answer proves mastery.
- No fixed learning-style categories.
- Deterministic validation for numerical/math answers.

### Automated Tests
- Unit tests for scoring, adaptive decisions, knowledge tracing, validation.
- Integration tests for assessment lifecycle, learner model updates.
- End-to-end tests for assessment → evidence → learner model → recommendation.
- AI evaluation for question quality, mathematical correctness, structured output validity.

### Known Limitations
- Bayesian Knowledge Tracing deferred.
- Programming assessment does not execute untrusted code in main process (sandboxing deferred).

### Completion Conditions
- A student can complete an assessment and receive an adaptive recommendation with rationale.

---

## Phase E — Visual Learning Tools

### Objective
Implement the Visual Learning Framework with the most valuable initial capability.

### Required Modules
- Visual Learning Interface.
- Deterministic visualization rendering (function graphing / equation visualization for mathematics).
- Reusable visualization interface receiving learning context.
- Association of visual activities with learning objectives.

### Dependencies
- Phase D (learning context, learner model).
- Frontend visualization library.

### Deliverables
- Function graphing / equation visualization (mathematics).
- Distinction between deterministic visualizations, AI-generated descriptions, static assets, interactive simulations.
- Visual activities linked to learning objectives.

### Acceptance Criteria
- A mathematical visualization renders deterministically from structured data.
- The visualization is associated with a learning objective.
- The system distinguishes visualization types clearly.

### Automated Tests
- Unit tests for visualization data transformation.
- Integration tests for visual activity → learning objective association.

### Known Limitations
- Only the most valuable initial capability implemented; other domains deferred.

### Completion Conditions
- A student can view a deterministic mathematical visualization linked to a learning objective.

---

## Phase F — Hardening and Private Deployment

### Objective
Security hardening, observability, testing completeness, and private deployment readiness.

### Required Modules
- Security: authorization, file security, AI security, data privacy, operational security.
- Observability: structured logging, metrics, AI usage/cost tracking.
- Testing: full unit, integration, end-to-end, AI evaluation, regression suites.
- Deployment: Docker Compose for private operation.

### Dependencies
- All previous phases.

### Deliverables
- Security review passed (auth, authorization, file, AI, privacy).
- Observability logging for failures, AI latency, usage/cost.
- Complete test suite with acceptance criteria for every core workflow.
- Docker Compose deployment for private operation.
- DECISION_LOG updated with final production decisions.

### Acceptance Criteria
- All core workflows have passing end-to-end tests.
- Security requirements applied to all modules.
- Structured logging does not expose sensitive content.
- Application can be deployed privately via Docker Compose.

### Automated Tests
- Full regression suite.
- AI evaluation with representative academic test cases.
- Security tests (auth, authorization, file upload, prompt injection resistance).

### Known Limitations
- Not a public SaaS; private operation only.
- No multi-tenancy.

### Completion Conditions
- Application is runnable privately and all acceptance criteria pass.

---

## Out of Scope for MVP

- Multi-tenancy / organizations.
- Mobile native apps.
- Public SaaS.
- Microservices / Kubernetes.
- Bayesian Knowledge Tracing (deferred).
- Every visualization tool (only function graphing/equation visualization initially).
- Programming code execution sandbox (deferred; programming exercises presented without direct execution in main process).
