# PRODUCT_REQUIREMENTS.md

# AQVERA — Product Requirements

## Functional Requirements

### FR-1: Teaching Methodology (Section 4)
- A versioned, provider-independent teaching methodology applies across all domains.
- Domain-specific teaching profiles add instructional behavior without changing the core standard.
- Structured teaching workflows, output contracts, validation rules, and evaluation criteria exist.
- Teaching quality does not rely exclusively on prompt instructions.

### FR-2: Learner Model (Section 5.A)
- Student knowledge represented at course, module, topic, subtopic, learning objective, and skill levels.
- Per-objective representation includes: estimated mastery, confidence, evidence count, assessment history, recent performance, repeated misconceptions, last interaction timestamp, retention review status, prerequisites.
- No single correct answer proves mastery.
- No fixed learning-style categories (visual/auditory).
- Evidence-based preferences and interaction patterns identified over time.

### FR-3: Learning Evidence Collection (Section 5.B)
- Direct assessment evidence and weaker behavioral signals distinguished.
- Interactions producing evidence: correct/incorrect answers, answer confidence, time spent, hint usage, attempts, repeated mistakes, activity completion, delayed assessments, application in new context.

### FR-4: Knowledge Tracing (Section 5.C)
- Initial explainable knowledge-tracking approach (rule-based mastery estimation).
- Bayesian Knowledge Tracing as a possible later enhancement.
- Considers item difficulty, assessment reliability, evidence confidence, knowledge decay and retention.
- Algorithm is replaceable.

### FR-5: Adaptive Decision Engine (Section 5.D)
- Deterministic decision pipeline with explicit inputs, outputs, and fallback behavior.
- Determines: what to learn next, which prerequisite needs attention, review vs. advance, difficulty level, whether to provide another explanation, which instructional activity, when retention review occurs.
- AI interprets errors and generates content but never invents mastery scores or silently modifies the learner model.

### FR-6: Personalized Learning Path (Section 5.E)
- Generated from course structure, objectives, prerequisites, student mastery, goals, available study time, assessment evidence.
- Student can understand why an activity is recommended.

### FR-7: Adaptive Feedback (Section 5.F)
- Communicates: what is understood, what remains weak, why a recommendation was selected, what to do next, whether enough evidence exists for reliable judgment.
- Avoids misleading precision.

### FR-8: Data Integrity (Section 5.G)
- Learning evidence traceable; records immutable; corrections as new records; learner-model calculations reproducible.
- Never silently rewrites historical assessment results.

### FR-9: AI Provider Abstraction (Section 6)
- Provider configuration, model selection, credentials management, request/response normalization, structured output, streaming, token/usage tracking, cost estimation, timeouts, retries, rate limiting, error classification, availability handling, fallback policies, capability metadata.

### FR-10: AI Responsibility Separation (Section 6)
- AI Orchestration, Teaching Engine, Knowledge Retrieval, Evaluation Engine, Adaptive Engine, Content Generation — separated responsibilities.

### FR-11: Structured AI Contracts (Section 6)
- Schema validation for: course structure, topic extraction, learning objectives, lesson generation, question generation, error classification, explanation generation, source attribution.
- Safe handling for malformed JSON, incomplete responses, unsupported capabilities, provider failures.

### FR-12: Assessment Types (Section 7)
- Multiple Choice, Multiple Select, True/False, Short Answer, Numerical Problems, Mathematical Expressions, Programming Exercises, Language Exercises, Conceptual Questions.

### FR-13: Assessment Lifecycle (Section 7)
- Generation → Question Validation → Difficulty Classification → Student Attempt → Answer Evaluation → Feedback Generation → Evidence Recording → Learner Model Update.

### FR-14: Assessment Quality (Section 7)
- Questions linked to course content and learning objectives.
- Traceable source references where possible.
- Answer keys and scoring criteria stored independently from question presentation.
- Deterministic validation for numerical/mathematical answers.
- Programming assessment does not execute untrusted code in the main application process.
- Subjective evaluation exposes criteria and confidence.
- Incorrect/ambiguous questions identifiable and reportable.
- Students do not receive correct answers before completing unless activity permits.

### FR-15: Visual Learning Framework (Section 8)
- Domain-specific tools: Mathematics/Statistics, Computer Science, Physics/Natural Sciences, Languages, Humanities.
- Distinguishes deterministic visualizations, AI-generated visual descriptions, static assets, interactive simulations.
- Deterministic rendering preferred for mathematical/scientific correctness.
- Reusable visualization interface receiving current learning context.
- Most valuable initial capability identified and justified.

### FR-16: Unified Learning Context (Section 9)
- Learning Context model: student identity, active course, module, topic, objectives, uploaded sources, current lesson, mastery evidence, recent assessment results, active learning path, teaching profile.
- Context passed through controlled application services.
- No tool independently reconstructs student knowledge from chat history.

### FR-17: Product Areas (Section 10)
- Authentication, Student Dashboard, Academic Course Workspace, Material Upload Center, Course Review/Editing, Course Learning Interface, AI Tutor Interface, Assessment Interface, Visual Learning Interface, Progress/Analytics, Settings.

### FR-18: Design System (Section 10)
- Typography, color tokens, spacing, layout principles, component conventions, navigation patterns, form behavior, feedback/notifications.
- Desktop and mobile browser layouts.
- Clarity over visual complexity.

### FR-19: Technology Stack (Section 11)
- Modular monolith default. Frontend Next.js/TypeScript/React (proposed). Backend Python/FastAPI (proposed). Database PostgreSQL (proposed). pgvector (proposed). Redis + worker (proposed). S3-compatible storage (proposed).

### FR-20: Data Model (Section 12)
- Relational data model with entities for Identity, Academic Structure, Content, Teaching, AI, Assessment, Adaptation, Application.
- Primary keys, foreign keys, unique constraints, indexing, soft deletion, migration strategy, transaction boundaries.
- Entity relationship diagram (Mermaid).

### FR-21: Security (Section 13)
- Authentication, authorization, file security, AI security (prompt injection, data leakage), data privacy, operational security.

### FR-22: Reliability & Observability (Section 14)
- Subsystem failure behavior, long-running job statuses/progress/retries/failure reasons/idempotency, structured logging, no sensitive content in logs.

### FR-23: Testing (Section 15)
- Unit, integration, end-to-end, AI evaluation, regression testing for every important subsystem.

### FR-24: Implementation Phases (Section 16)
- Core Functional Foundation, Complete Academic Content Pipeline, Teaching and AI Capabilities, Assessment and Adaptive Learning, Visual Learning Tools, Hardening and Private Deployment.

### FR-25: Engineering Workflow (Section 17)
- Agent roles, task assignment, AGENTS.md, coding conventions, testing expectations, security rules, documentation requirements, prohibited shortcuts.

### FR-26: Documentation (Section 18)
- All documents in docs/product, docs/architecture, docs/academic, docs/engineering, plus root files. DECIDED/PROPOSED/OPEN/DEFERRED marking.

## Non-Functional Requirements

### NFR-1: Privacy
- Minimize PII sent to external AI providers.
- Define which content is transmitted to AI providers.
- Clear deletion behavior and retention policies.
- Avoid logging private document content unnecessarily.

### NFR-2: Security
- Secure password handling, session management, token expiration.
- Server-side permission validation, protection against IDOR.
- File type validation, size limits, secure storage.

### NFR-3: Reliability
- Long-running jobs have explicit statuses, progress, retry policies, failure reasons, idempotency.
- No duplicate course generation or assessment submissions from repeated requests.

### NFR-4: Observability
- Structured logging for request failures, job failures, AI latency, usage/cost, processing duration, retrieval quality, evaluation errors.

### NFR-5: Accessibility
- WCAG-compliant interface; keyboard navigation; screen reader support.

### NFR-6: Performance
- Responsive desktop and mobile browser layouts.
- Background processing for long-running document/AI tasks.

## Acceptance Criteria (Core Workflow)

1. A student can create an account and log in.
2. A student can upload academic material.
3. A course can be generated from uploaded material linked to learning objectives.
4. A student can view a lesson and complete an assessment.
5. Assessment results update the learner model.
6. The adaptive engine recommends the next activity with rationale.
7. All AI outputs pass schema validation before use.
8. Evidence records are immutable and traceable.
