# AQVERA — Baseline Audit (Phase 0 — Repository Intelligence)

## Repository Overview

- **Path:** `D:\AQVERA`
- **Git:** Initialized but no commits exist. All files untracked.
- **Write access:** Available (the executing user can create/modify files in D:\AQVERA).
- **State:** Partially implemented. Documentation is extensive; application code exists but is incomplete.

## Existing Architecture

### High Level (per docs/architecture/SYSTEM_ARCHITECTURE.md)
- Modular monolith: single deployable application with clear module boundaries.
- Frontend: Next.js 16.4.6 + TypeScript + React 19 + Tailwind CSS 4.
- Backend: Python 3.14 + FastAPI + SQLAlchemy 2.x + Alembic.
- Database: SQLite file `backend/aqvera.db` (Phase 1), PostgreSQL target.
- No Redis, no message broker, no separate vector database introduced yet (deferred).
- AI Provider Abstraction Layer designed but not implemented (no `ai/` directory existed).

### Module Boundaries (per docs/architecture/DOMAIN_BOUNDARIES.md)
9 domains: Identity & Access, Academic Structure, Content Processing, Teaching, AI Infrastructure, Assessment, Adaptive Learning, Visual Learning, Application (Cross-Cutting).

### Database Schema (current, in code)
Tables: `users`, `courses`, `conversations`, `messages`. No tables for materials, processing jobs, chunks, embeddings, assessments, learner model, etc. The Alembic initial migration `9e1dbcc7064c_initial_schema.py` is empty; tables are created via SQLAlchemy `create_all()` at startup.

### Auth (current)
Local dev access mode: `get_current_user()` returns/gets-or-creates a dev user (`dev@aqvera.local`). No real registration, login, logout, password hashing in API routes, or session tokens. `bcrypt` is available in `core/security.py` but unused by routes.

### Frontend Routes (current)
- `/` — Landing page (working)
- `/dashboard` — Dashboard with real courses/chats from API (working, loading/empty/error states)
- `/courses` — Course library with CRUD (working against real API)
- `/courses/[id]` — Course workspace with conversations (working against real API)
- `/chat/[id]` — Chat page; persists user messages; AI responses unavailable (provider not configured); honest "AI provider not configured" banner
- `/sections`, `/sections/[section]` — Academic sections explorer (static data)
- `/learning` — "Coming in Phase 2" placeholder
- `/resources` — "Coming in Phase 2" placeholder
- `/settings` — Settings page (dev account info, auth note)

### Backend API (current)
- `GET /health`
- `POST/GET /courses`, `GET/PUT/PATCH/DELETE /courses/{id}`
- `GET/POST /conversations`, `GET/PATCH/DELETE /conversations/{id}`
- `POST/GET /conversations/{id}/messages`
- `GET /conversations/ai-status` → returns `configured: false`

### Frontend Components
`Shell`, `Navigation` (TopNav, Sidebar, MobileTopBar), `Dialog`, `AQVERALogo` (brand mark + horizontal wordmark).

### Design System
`design-system/aqvera/MASTER.md` — color tokens (ink #101D2B, navy #192C3A, paper #F6F5F0, white #FFFFFF, sage #C7E8DC, sage-dark #315C50, terracotta #D49B72, muted #77828A, border #E7E8E3, surface #EFEEE8), typography (Inter + Crimson Text), spacing scale, radii, borders, component variants, motion, responsive breakpoints.

## Existing Working Functionality

| Feature | Status | Evidence |
|---------|--------|----------|
| Landing page | WORKING | `/` renders; builds successfully |
| Dashboard (load courses + chats) | WORKING | Calls `/api/courses` and `/api/conversations`; empty/loading states |
| Course create | WORKING | `POST /courses` persists; 8 backend tests pass |
| Course list | WORKING | `GET /courses` with pagination + archived filter |
| Course get | WORKING | `GET /courses/{id}` with 404 for missing |
| Course update | WORKING | `PUT /courses/{id}` |
| Course archive | WORKING | `PATCH /courses/{id}/archive` |
| Course delete | WORKING | `DELETE /courses/{id}` |
| Conversation CRUD | WORKING | `/conversations` endpoints + service layer |
| Message create/list | WORKING | `/conversations/{id}/messages` |
| Health check | WORKING | `GET /health` |
| Backend tests | 8/8 PASS | `pytest tests/test_courses.py` |
| Frontend build (app source) | Type-checks | `next build` fails only on pre-existing test file type error |
| UI/UX audit screenshots | Captured | `artifacts/ux-audit/` (24 images, 8 pages × 3 breakpoints) |

## Missing Functionality

- User registration, login, logout, password-based auth (only dev user exists)
- Material upload (PDF, DOCX, PPTX, TXT, images, audio, video)
- Document processing pipeline (extraction, OCR, chunking, embedding, indexing)
- RAG system (retrieval, source attribution, prompt-injection defense)
- AI tutor (course-aware, lesson-aware, source-grounded)
- Adaptive learning engine (mastery tracking, recommendations)
- Assessment system (MCQ, short answer, problem-solving, grading)
- Learning progress / mastery tracking
- Course content organization (modules, lessons, topics)
- Notifications
- Settings beyond dev account info
- `ai/` subsystem (providers, orchestration, routing, agents, tutoring, rag, retrieval, memory, adaptive_learning, assessment, multimodal, prompts, evaluation, monitoring, cost_control, security, docs)
- `.env.example` with documented provider variables
- Accessibility audit and automated tests beyond existing axe-core spec
- E2E tests for full academic journeys (registration, upload, assessment, adaptive)

## Broken Functionality

| Issue | Detail |
|-------|--------|
| `tests/walkthrough-audit.spec.ts` type error | `context.on("pageerror", ...)` not assignable to `"weberror"`; `e` implicitly any. Blocks `next build` type-check. |
| `tests/academic-experience.spec.ts` references nonexistent route | `/chat/general-calculus` doesn't exist (only `/chat/[id]`); expects AI welcome message that is never sent. |
| Chat AI response | Simulated/unavailable; no provider adapter; honest unavailable state only. |
| Alembic initial migration | Empty (no DDL); relies on `create_all()` at startup. |

## Existing Technical Debt

1. **No `ai/` directory** — required by the mission; must be created with the full subsystem structure.
2. **No auth API** — registration/login/logout missing; dev user is a placeholder.
3. **Empty Alembic migration** — schema not versioned via migrations; `create_all()` used instead.
4. **Pydantic v1-style `Config` classes** — deprecated in Pydantic v2 (warnings only).
5. **No `.env.example`** — only `.env` with a dev secret key.
6. **No content/material models** — courses exist but no materials, chunks, embeddings, assessments, learner models.
7. **Frontend `walkthrough-audit.spec.ts`** — type error blocks production build type-check.
8. **No AI provider configured** — all AI features are unavailable by design (honestly communicated).

## Baseline Test Results

**Backend:** `python -m pytest tests/` → **8 passed**, 0 failed. Warnings: Pydantic v1 `Config` deprecation, `httpx` TestClient deprecation, pytest-asyncio loop scope.

**Frontend:** `npx next build` → app source compiles; type-check fails on `tests/walkthrough-audit.spec.ts` (pre-existing TS error). E2E tests were not executed (require dev servers running).

## Proposed Execution Sequence

| Phase | Objective | Key Deliverables |
|-------|-----------|------------------|
| 1 | Baseline audit + fix build/type errors | BASELINE_AUDIT.md, fix walkthrough-audit.spec.ts |
| 2 | `ai/` subsystem foundation | providers/, orchestration/, routing/, contracts, adapters (mock/contract-tested) |
| 3 | Backend auth + content pipeline | register/login, material upload, processing jobs, extraction, chunking |
| 4 | RAG + tutor + assessment + adaptive | retrieval, source-grounded Q&A, assessments, learner model, recommendations |
| 5 | Frontend completion | upload UI, tutor chat, assessment UI, progress, settings |
| 6 | Testing | unit, integration, E2E, accessibility, RAG evaluation |
| 7 | Documentation + success gate | FINAL_REPORT.md, FINAL_ACCEPTANCE.json, MISSION_SUCCESS.txt |

## High-Risk Areas

1. **AI provider credentials** — No provider key is configured. Without one, tutor, RAG, assessment generation, and course generation cannot be live-tested. Mitigation: contract tests + mocks; clearly label NOT CONFIGURED.
2. **SQLite vs. PostgreSQL/vector** — pgvector not available on SQLite. Vector retrieval for RAG requires either PostgreSQL+pgvector or a lightweight pure-Python vector fallback. Decision needed.
3. **Document processing dependencies** — PDF/DOCX/PPTX extraction and OCR require Python libraries (pypdf, python-docx, python-pptx, pytesseract, etc.) that may not be installed. Must verify before building pipeline.
4. **Frontend/Backend API mismatch** — Frontend calls `/api/courses` and `/api/conversations` via Next.js rewrites to `http://127.0.0.1:8000`. New endpoints must follow the same prefix convention.
5. **No production auth** — Replacing dev-user auth with real registration/login must not break existing course/conversation ownership (`owner_id`).
