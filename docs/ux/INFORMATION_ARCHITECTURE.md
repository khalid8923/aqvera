# INFORMATION_ARCHITECTURE.md

# AQVERA — Information Architecture

Status: DECIDED

## Application Sitemap

### Public (unauthenticated)

| Path | Purpose | Status |
|------|---------|--------|
| `/` | Landing page — value proposition, how it works, start learning | Implemented |
| `/dashboard` (redirect to auth) | Entry point for signed-in students | Implemented (shell) |

### Authenticated (student)

| Path | Purpose | Status |
|------|---------|--------|
| `/dashboard` | Student dashboard — courses, progress, quick actions | Implemented |
| `/courses` | Course library — create, edit, archive, delete courses | Implemented |
| `/courses/[id]` | Course workspace — course details, materials, learning activities, progress | Implemented (shell, Phase 2 content pending) |
| `/learning` | Learning progress — mastery across courses and topics | Implemented (placeholder, Phase 2) |
| `/resources` | Study resources — uploaded materials, source traceability | Implemented (placeholder, Phase 2) |
| `/settings` | Account and application preferences | Implemented |

### Future / not yet designed (no defined product purpose yet)

- Authentication pages (`/login`, `/register`, `/auth/...`) — not yet built; referenced in journeys only.
- Material upload center — not yet built.
- Course review/editing beyond basic metadata — not yet built.
- AI tutor interface — not yet built.
- Assessment interface — not yet built.
- Visual learning interface — not yet built.
- Progress/analytics beyond placeholder — not yet built.

Avoid designing navigation for features that have no defined product purpose.

## Public versus Authenticated Areas

- Public: landing page only. No student data, no courses.
- Authenticated: dashboard, courses, course workspace, learning, resources, settings. Requires an active session.
- Navigation links to authenticated areas from the landing page ("Start learning", "Explore AQVERA") navigate to `/dashboard`, which is the authenticated entry point.

## Primary and Secondary Navigation

### Primary navigation (sidebar, desktop; mobile top bar)

| Item | Path | Section |
|------|------|---------|
| Overview | `/dashboard` | Primary |
| My Courses | `/courses` | Primary |
| Learning Progress | `/learning` | Primary (placeholder) |
| Study Resources | `/resources` | Primary (placeholder) |
| Settings | `/settings` | Primary |

### Secondary / contextual

- Course actions (create, edit, archive, delete) appear on `/courses` and `/dashboard`.
- "Open course" navigates from course library to `/courses/[id]`.
- "Return to course library" appears on course workspace.
- Help is available in the top nav (not yet wired to a help page).

## Page Hierarchy

```
Dashboard
└── Create course (dialog)
Courses
├── Course list
├── Create course (dialog)
├── Edit course (dialog)
└── Course workspace [id]
    ├── Course details
    ├── Materials (Phase 2)
    ├── Learning activities (Phase 2)
    └── Progress (Phase 2)
Learning (placeholder)
Resources (placeholder)
Settings
```

## Course Organization

A course contains:
- Identity: title, course code, semester, subject domain, description, primary language, university, department.
- State: active or archived (soft delete).
- Owner: the student who created it.
- Timestamps: created_at, updated_at.
- Future: modules, topics, learning objectives, materials, lessons, assessments (not yet built).

## Learning Workspace Structure

The course workspace (`/courses/[id]`) presents:
- Course metadata (university, department, semester, language).
- Materials section (Phase 2 — document upload not yet built).
- Learning activities section (Phase 2 — lessons & assessments not yet built).
- Progress section (Phase 2 — learner model not yet built).

Each future section is currently represented as an honest "coming in Phase 2" empty state, never as functional UI with fake data.

## How Future Areas Fit

Future learning, materials, and assessment areas fit under the course workspace as nested sections:
- Materials → uploaded documents, processing status, source traceability.
- Learning → current module/topic, lessons, activities.
- Assessment → questions, attempts, feedback.
- Progress → mastery by objective, retention reviews, recommendations.

Navigation to these areas should be added only when the corresponding product capability has a defined purpose and implementation plan.
