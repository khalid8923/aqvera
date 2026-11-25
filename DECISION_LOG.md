# DECISION_LOG.md

# AQVERA — Decision Log

All architectural decisions are recorded here with a status:
- **DECIDED** — committed, implementation-ready
- **PROPOSED** — recommended but not yet committed
- **OPEN** — requires user input or further analysis
- **DEFERRED** — intentionally postponed to a later phase

---

## 1. Architectural Direction

**Decision:** Modular Monolith  
**Status:** DECIDED  
**Rationale:** Suitable for solo developer, private operation, clear module boundaries, allows future extraction into services if needed. No microservices, Kubernetes, or complex event-driven infrastructure without demonstrated requirement.

---

## 2. Frontend Stack

**Decision:** Next.js + TypeScript + React  
**Status:** PROPOSED  
**Rationale:** Strong documentation, AI-assisted development friendly, full-stack capability, React ecosystem for visualization libraries.  
**Alternatives considered:** Vue, Svelte, plain React + Vite.

---

## 3. Backend Stack

**Decision:** Python + FastAPI  
**Status:** PROPOSED  
**Rationale:** Strong AI/ML library ecosystem, FastAPI is productive and well-documented, good for AI orchestration and document processing.  
**Alternatives considered:** Node.js/Express, Go, Java Spring.

---

## 4. Database

**Decision:** SQLite (Phase 1), PostgreSQL (target)  
**Status:** PROPOSED (Phase 1) / PROPOSED (target)  
**Rationale:** PostgreSQL is not installed in the environment and Docker is unavailable, so PostgreSQL cannot be provisioned for Phase 1. SQLite is used via SQLAlchemy 2.x with Alembic migrations to keep the same ORM and migration approach. The modular monolith design allows migration to PostgreSQL in Phase F without changing application code.  
**Deviation from docs:** docs/engineering/TECHNOLOGY_DECISIONS.md lists PostgreSQL as PROPOSED; this is a Phase 1 substitution documented here.

---

## 5. Vector Search

**Decision:** pgvector (initially)  
**Status:** PROPOSED  
**Rationale:** Keeps vector search within PostgreSQL, avoids introducing a separate vector database, suitable for initial scale.  
**Alternatives considered:** Pinecone, Weaviate, Milvus, Qdrant.

---

## 6. Background Processing

**Decision:** Redis + worker queue (e.g., RQ or Celery)  
**Status:** PROPOSED  
**Rationale:** Separates long-running document processing and AI tasks from HTTP request handling.  
**Alternatives considered:** In-process background tasks, database-backed queue.

---

## 7. File Storage

**Decision:** S3-compatible object storage  
**Status:** PROPOSED  
**Rationale:** Standard for file uploads, works with MinIO for local development.  
**Alternatives considered:** Local filesystem, Azure Blob, Google Cloud Storage.

---

## 8. AI Provider Strategy

**Decision:** Provider Abstraction Layer with multiple adapters  
**Status:** DECIDED  
**Rationale:** AQVERA must not depend on a single commercial AI API. Providers are replaceable without rewriting teaching methodology or core business logic.  
**Initial providers:** TBD (OPEN — to be selected).

---

## 9. Teaching Methodology

**Decision:** Versioned, testable, provider-independent standard teaching methodology  
**Status:** DECIDED  
**Rationale:** Core requirement — teaching quality must not rely exclusively on prompt instructions. Structured workflows, output contracts, validation rules, and evaluation criteria required.

---

## 10. Knowledge Tracing (Initial Algorithm)

**Decision:** Rule-based mastery estimation (replaceable)  
**Status:** PROPOSED  
**Rationale:** Do not implement unnecessarily complex algorithms before enough meaningful data. Rule-based is explainable and practical initially; Bayesian Knowledge Tracing is a possible later enhancement.  
**Alternatives considered:** Bayesian Knowledge Tracing, Deep Knowledge Tracing.

---

## 11. Initial Academic Domain

**Decision:** Mathematics  
**Status:** OPEN (recommended)  
**Rationale:** High academic usefulness, strong visual learning opportunities (graphing, equations), deterministic validation possible for numerical answers, representative materials available.  
**Alternatives:** Computer Science, Physics, Languages.

---

## 12. Smallest Coherent Vertical Slice (MVP)

**Decision:** Single course in Mathematics → content upload → course generation → lesson → assessment → learner model update → adaptive recommendation  
**Status:** PROPOSED  
**Rationale:** Proves the complete academic workflow end-to-end.

---

## 13. Visualization Strategy

**Decision:** Deterministic rendering preferred for mathematical/scientific content; AI-generated descriptions only where correctness is not critical  
**Status:** PROPOSED  
**Initial capability:** Function graphing / equation visualization (Mathematics)  
**Status:** PROPOSED

---

## 14. Deployment

**Decision:** Private, self-hosted (Docker Compose recommended)  
**Status:** PROPOSED  
**Rationale:** Suitable for solo developer and private operation, avoids cloud complexity.  
**Alternatives considered:** Managed cloud services, Kubernetes.

---

## 15. Authentication

**Decision:** Password-based with secure hashing (bcrypt/argon2) + session management  
**Status:** PROPOSED  
**Alternatives considered:** OAuth only, magic links.

---

## 16. Knowledge Tracing Evidence

**Decision:** Distinguish direct assessment evidence from weaker behavioral signals  
**Status:** DECIDED

---

## 17. Evidence Immutability

**Decision:** Learning evidence records are immutable; corrections represented as new records; never silently rewrite historical assessment results  
**Status:** DECIDED

---

## 18. AI Output Validation

**Decision:** All important AI outputs validated against structured contracts (JSON schema); never bypass application validation  
**Status:** DECIDED

---

## OPEN Decisions Requiring User Input

| # | Decision | Why It Matters |
|---|----------|----------------|
| O2 | Initial AI provider(s) | Determines which adapters to build first |
| O3 | Initial academic domain | Mathematics recommended, but user may prefer another |
| O4 | Database hosting (local vs managed) | Deployment detail |

---

## DEFERRED Decisions

| # | Decision | Reason |
|---|----------|--------|
| D1 | Multi-tenancy / organization support | Not needed for private operation |
| D2 | Mobile native apps | Desktop + mobile browser layouts only |
| D3 | Public SaaS launch requirements | Future consideration |
| D4 | Bayesian Knowledge Tracing | Later enhancement after sufficient data |

---

## Phase 1 Implementation Decisions

| # | Decision | Status | Rationale |
|---|----------|--------|-----------|
| P1-1 | Frontend: Next.js + TypeScript + Tailwind CSS | DECIDED | Node.js v26 available; matches docs recommendation |
| P1-2 | Backend: Python + FastAPI + SQLAlchemy 2.x | DECIDED | Python 3.14 available; matches docs recommendation |
| P1-3 | Database: SQLite (Phase 1), PostgreSQL (target) | DECIDED | PostgreSQL/Docker unavailable; SQLite via SQLAlchemy keeps same ORM/migration path |
| P1-4 | Migrations: Alembic | DECIDED | Matches docs; works with SQLite and PostgreSQL |
| P1-5 | Auth: Local dev access mode (server-side identity, not production auth) | SUPERSEDED | Dev-user fallback removed; all protected routes require valid JWT |
| P1-6 | API: REST with typed Pydantic schemas | DECIDED | Matches FastAPI convention |
| P1-7 | Testing: pytest (backend), Playwright (E2E) | DECIDED | Matches docs; pytest available via pip |

---

## Phase 2 Implementation Decisions (This Continuation)

| # | Decision | Status | Rationale |
|---|----------|--------|-----------|
| P2-1 | Auth: Remove development-user fallback from `get_current_user()` | DECIDED | Critical security fix. No silent default user. All protected routes require valid JWT bearer token; unauthenticated requests receive 401. `get_or_create_dev_user()` removed from auth and course services. |
| P2-2 | Frontend: Migrate all protected API calls from raw `fetch` to `apiFetch` | DECIDED | Dashboard, courses, course workspace, and resources pages now use the auth-aware `apiFetch` client with automatic bearer token injection. Sign-in-required gating added for unauthenticated users. |
| P2-3 | Migrations: Write complete initial Alembic migration with all table definitions | DECIDED | Replaces empty migration that relied on `create_all()`. `alembic check` passes. Migrations are additive only (no table/column drops). |
| P2-4 | Email: Expose honest configuration state via `/auth/email/config` | DECIDED | SMTP settings added to `.env.example` and `Settings`. `EmailService` raises `EmailNotConfiguredError` when SMTP is absent. No fake email-sending claims. |
| P2-5 | Background processing: In-process daemon threads instead of Redis/Celery | DECIDED | Redis/Docker unavailable. Material processing runs in a daemon thread; clients poll `/materials/{id}/status`. Thread registry prevents duplicate processing. Revisit for production scale. |
| P2-6 | Spaced repetition: SM-2 algorithm for flashcard reviews | DECIDED | Simple, explainable, deterministic. Tracks interval, ease factor, repeat count, lapses, next review date. Bayesian KT deferred (D4). |
| P2-7 | Topic mastery: Evidence-based deterministic learning-rate update | DECIDED | Mastery estimated from actual assessment results (not predictions). Updates via `mastery += lr * (signal - mastery)` with evidence-count-based confidence. |

