# SYSTEM_ARCHITECTURE.md

# AQVERA — System Architecture

## Architectural Direction: Modular Monolith (DECIDED)

AQVERA is a modular monolith: a single deployable application with clearly separated module boundaries and well-defined dependency direction. This is the default unless a strong technical reason exists otherwise. No microservices, Kubernetes, or complex event-driven infrastructure is introduced without a demonstrated requirement. The architecture allows future extraction of modules into independent services if necessary.

## High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Client (Next.js / React)               │
│  Dashboard · Course Workspace · Tutor · Assessment · Visual │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS / JSON
┌────────────────────▼────────────────────────────────────────┐
│                     API Gateway (FastAPI)                   │
│  Auth · Routing · Rate Limiting · Input Validation · CORS   │
└────────────────────┬────────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    ▼                ▼                ▼
┌─────────┐    ┌─────────┐    ┌──────────────┐
│  Auth   │    │  Course │    │   Teaching   │
│ Module  │    │ Module  │    │   Engine     │
└─────────┘    └─────────┘    └──────┬───────┘
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    ▼                               ▼                               ▼
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│ Adaptive     │            │ Assessment   │            │ Content Gen  │
│ Engine       │            │ Engine       │            │              │
└──────┬───────┘            └──────┬───────┘            └──────┬───────┘
       │                          │                          │
       ▼                          ▼                          ▼
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│ Learner      │            │ Questions    │            │ AI Providers │
│ Model        │            │ Answer Keys  │            │ (Abstraction)│
└──────────────┘            └──────────────┘            └──────┬───────┘
                                                              │
                                                              ▼
                                                       ┌──────────────┐
                                                       │ Knowledge    │
                                                       │ Retrieval    │
                                                       └──────┬───────┘
                                                              │
                                                              ▼
                                                       ┌──────────────┐
                                                       │ Vector Store │
                                                       │ (pgvector)   │
                                                       └──────────────┘

Shared Services (cross-cutting):
├── Database (PostgreSQL) — all modules
├── Object Storage (S3-compatible) — file uploads
├── Background Worker (Redis + queue) — document processing, AI tasks
├── Logging & Observability — all modules
└── Unified Learning Context Service — context ownership, persistence, retrieval
```

## Module Boundaries and Dependency Direction

| Module | Dependencies On | Dependents |
|--------|----------------|------------|
| Auth | Database, Config | All modules (via auth middleware) |
| Course | Database, Content Processing | Teaching Engine, Assessment |
| Content Processing | Database, Object Storage, Background Worker, AI Providers | Course |
| Teaching Engine | Database, AI Providers, Learning Context | Adaptive Engine |
| Assessment Engine | Database, Teaching Engine, Evaluation | Adaptive Engine |
| Adaptive Engine | Learner Model, Assessment Evidence | Teaching Engine (feedback), Learning Path |
| Content Generation | AI Providers, Teaching Engine, Knowledge Retrieval | Teaching Engine |
| AI Provider Abstraction | Config, Secrets | Teaching Engine, Content Generation, Evaluation |
| Knowledge Retrieval | Vector Store, Database | Teaching Engine, Content Generation |
| Learning Context Service | Database | All modules |
| Visual Learning | Database, Learning Context | Course Learning Interface |

**Dependency rule:** Modules depend only on lower-level or peer modules defined by interface. No circular dependencies. The AI Provider Abstraction Layer is an infrastructure concern that business modules depend on, but it does not depend on business logic.

## Separation of Concerns

### HTTP Layer (FastAPI)
- Request routing, authentication, authorization, input validation, rate limiting, CORS, error handling.
- Does not contain business logic.

### Business Logic Layer
- Teaching methodology, adaptive decisions, assessment evaluation, knowledge tracing, learning paths.
- Provider-independent; testable without AI.

### AI Layer
- Provider abstraction, orchestration, retrieval, content generation.
- All AI outputs validated against structured contracts before reaching business logic.

### Data Layer
- PostgreSQL (relational), pgvector (vector search), Object Storage (files), Background Worker (jobs).

## Long-Running Task Separation

Document processing, OCR, embedding generation, and AI generation tasks are separated from normal HTTP request handling via a background worker queue (Redis + worker). HTTP requests enqueue jobs and return job IDs; clients poll for status/progress.

## Data Flow: Core Workflow

1. **Upload:** Client → API → Object Storage → Processing Job (background) → Extraction → Chunks → Embeddings → Vector Store.
2. **Course Generation:** Course Module → AI Orchestration → Provider Abstraction → AI Provider → Structured Output → Validation → Course stored.
3. **Assessment:** Assessment Engine → Question Generation (validated) → Student Attempt → Evaluation Engine (deterministic + criteria) → Evidence Recorded → Learner Model Updated.
4. **Adaptive:** Adaptive Engine reads Learner Model + Evidence → Decision Pipeline → Recommendation → Teaching Engine generates feedback/content.

## Failure Boundaries

- **AI provider unavailable:** Fallback policy degrades to secondary provider or returns a degraded response; business logic continues with cached data.
- **Document extraction failure:** Job status = failed with reason; retry policy; user notified.
- **Vector indexing failure:** Degraded retrieval; keyword fallback; course generation continues with reduced context.
- **Database connectivity issue:** Requests fail fast with clear error; no partial writes (transactions).
- **Background worker interruption:** Jobs have explicit statuses, progress, retry policies, failure reasons, idempotency keys.

## Technology Mapping (PROPOSED)

| Concern | Technology |
|---------|------------|
| Frontend | Next.js, TypeScript, React |
| Backend API | Python, FastAPI |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Background Queue | Redis + RQ/Celery |
| Object Storage | S3-compatible (MinIO local) |
| AI Providers | Abstraction layer; initial provider TBD |

## Deployment View (PROPOSED)

Private, self-hosted via Docker Compose:
- Frontend container
- Backend API container
- PostgreSQL container
- Redis container
- Worker container
- MinIO (S3-compatible) container

Not Kubernetes. Not a public SaaS initially.
