# TECHNOLOGY_DECISIONS.md

# AQVERA — Technology Decisions

## Evaluation Criteria

Developer productivity, integration complexity, reliability, maintainability, cost, documentation quality, compatibility with AI-assisted development, suitability for a solo developer.

## Recommended Stack (PROPOSED)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | Next.js, TypeScript, React | Strong documentation, AI-assisted development friendly, full-stack, rich visualization library ecosystem |
| Backend | Python, FastAPI | Strong AI/ML ecosystem, productive, well-documented, good for AI orchestration and document processing |
| Database | PostgreSQL | Relational fit for academic data, pgvector for vector search, mature |
| Vector Search | pgvector | Keeps vector search in PostgreSQL; no separate vector DB needed initially |
| Background Queue | Redis + RQ/Celery | Separates long-running document/AI tasks from HTTP |
| Object Storage | S3-compatible (MinIO local) | Standard for file uploads; MinIO for local dev |
| AI | Provider Abstraction Layer + adapters | Provider independence; replaceable without rewriting business logic |
| Document Processing | Python extraction/OCR libraries | Python ecosystem strong for PDF/text extraction |
| Testing | pytest (backend), Jest/Playwright (frontend) | Standard, well-documented |
| Deployment | Docker Compose | Simple private operation; suitable for solo developer |

## Alternatives Considered

| Concern | Alternatives | Why Not Selected |
|---------|-------------|-----------------|
| Frontend | Vue, Svelte, plain React + Vite | Next.js offers better full-stack integration and documentation |
| Backend | Node.js/Express, Go, Java Spring | Python has stronger AI/ML and document processing libraries |
| Database | MySQL, MongoDB, SQLite | PostgreSQL + pgvector best fits relational academic data + vector search |
| Vector DB | Pinecone, Weaviate, Milvus, Qdrant | pgvector avoids extra infrastructure; sufficient for initial scale |
| Background | In-process tasks, DB-backed queue | Redis + worker is standard and reliable for long-running jobs |
| Storage | Local filesystem, Azure Blob, GCS | S3-compatible is standard; MinIO works locally |
| Deployment | Kubernetes, managed cloud | Too complex for solo developer; Docker Compose sufficient for private operation |

## Architecture Direction

**Modular Monolith (DECIDED)** — Single deployable with clear module boundaries. No microservices, Kubernetes, or complex event-driven infrastructure without demonstrated requirement. Allows future service extraction.

## Long-Running Task Separation (DECIDED)

Document processing, OCR, embedding generation, and AI generation are separated from normal HTTP handling via a background worker queue.

## AI-Assisted Development Compatibility

The stack is chosen to work well with AI coding agents:
- TypeScript provides type safety for AI-generated frontend code.
- Python/FastAPI is well-documented and commonly used in AI-generated code.
- PostgreSQL has extensive documentation and examples.
- Clear module boundaries reduce the risk of AI agents creating tangled code.

## Solo Developer Suitability

- Simple deployment (Docker Compose).
- Few moving parts.
- Strong documentation for all chosen technologies.
- No need for DevOps specialization.

## Unresolved (OPEN)

- Initial AI provider(s) — OpenAI, Anthropic, Ollama, Azure OpenAI to be selected.
- Embedding model — provider-dependent.
- Database hosting — local PostgreSQL vs. managed service.
