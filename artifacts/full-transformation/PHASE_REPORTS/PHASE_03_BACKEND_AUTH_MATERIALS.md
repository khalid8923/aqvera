# AQVERA — Phase Report: Phase 3 (Backend Auth + Content Pipeline)

## Phase Objective
Add user registration/login (JWT auth) and the academic materials upload pipeline (validation, storage, SHA-256 integrity, processing jobs, status tracking) to the backend, connecting to the existing course/conversation API.

## Completed Work

### Authentication (`/auth`)
- `POST /auth/register` — creates user with bcrypt-hashed password, rejects duplicates.
- `POST /auth/login` — verifies credentials, returns JWT access token.
- `app/schemas/auth.py`: UserRegister, UserLogin, UserRead, Token, ErrorResponse.
- `app/services/auth.py`: create_user, authenticate_user, get_user_by_email, get_or_create_dev_user, ensure_course_ownership.
- `app/api/auth.py`: register + login routes.
- `app/core/deps.py`: get_current_user now supports JWT bearer tokens; falls back to dev user when no token (backward compatible).

### Materials Pipeline (`/materials`)
- `POST /materials/upload` — validates file type/size, SHA-256 dedup, stores file, creates material + extraction job.
- `GET /materials` — list user's materials.
- `GET /materials/{id}` — get a material (ownership enforced).
- `GET /materials/{id}/status` — processing status + job list + progress.
- `GET /materials/{id}/jobs` — list processing jobs.
- `app/models/material.py`: UploadedMaterial, ProcessingJob.
- `app/schemas/material.py`: MaterialUploadResponse, MaterialRead, ProcessingJobRead, MaterialStatus, ErrorResponse.
- `app/services/material.py`: validate_file, store_file, compute_sha256, create_material, create_processing_job, get_material, list_materials, get_job, list_jobs_for_material.
- `app/api/materials.py`: all material routes.
- Supported types: PDF, DOCX, PPTX, TXT, PNG, JPG, MP3, WAV, MP4. Max 50 MB.
- Upload dir: `data/uploads/` (project-local).

### Models & Registration
- `app/models/__init__.py`: exports UploadedMaterial, ProcessingJob.
- `app/main.py`: registers auth and materials routers.
- `app/api/__init__.py`: exports all three routers.

### Tests (backend)
- 19 tests pass: 8 courses, 5 auth, 6 materials.
- Tests use unique emails to avoid cross-run DB conflicts.

## Test Results
- Backend (`backend/tests/`): 19/19 pass.
- AI (`ai/tests/`): 25/25 pass (unchanged).
- Frontend (`npx next build`): clean.

## Acceptance Criteria (Phase 3)
- [x] User registration works; duplicate email rejected.
- [x] Login returns JWT token; wrong password/unknown user rejected.
- [x] Material upload validates type/size; unsupported files rejected with 400.
- [x] Duplicate content (same SHA-256) returns existing material (idempotent).
- [x] Material list, get, status, jobs endpoints work with ownership enforcement.
- [x] Processing job created with status "pending" on upload.
- [x] Backward compatible: dev-user fallback still works for existing course/conversation APIs.

## Known Limitations
- Processing jobs remain "pending" — background extraction worker not yet implemented (Phase 4/5).
- No OCR/extraction logic connected yet (files stored but not extracted).
- No AI provider key → tutor/RAG unavailable live (NOT CONFIGURED).

## Next Actions
1. Frontend: material upload page, tutor chat integration with real backend.
2. Connect ai/ orchestration to backend chat endpoint (mock-based AI responses).
3. Add .env.example with provider variables.
4. Add E2E tests for full journeys.
5. Add accessibility audit report.
6. Write FINAL_REPORT.md, FINAL_ACCEPTANCE.json.
7. Success gate verification + MISSION_SUCCESS.txt.
