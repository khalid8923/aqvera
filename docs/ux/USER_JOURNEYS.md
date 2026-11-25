# USER_JOURNEYS.md

# AQVERA — User Journeys

Status: DECIDED (principles), with per-journey implementation status labels.

Capability labels used throughout:
- `Implemented` — code exists and is verified working.
- `Partially Implemented` — code exists but is incomplete or a shell.
- `Planned` — documented in product requirements; not yet built.
- `Not Designed` — no UX or product design exists yet.

---

## Journey 1: Discover AQVERA

**Actor:** Prospective student (unauthenticated)  
**Goal:** Understand what AQVERA is and decide to start.

### Starting condition
On the landing page (`/`), no account, no session.

### User goal
Learn the value proposition, how AQVERA works, and begin.

### User actions
1. Reads landing page headline and subhead.
2. Reads "How AQVERA works" (upload materials → structured courses → adaptive progress).
3. Clicks "Start learning" or "Explore AQVERA".

### System responses
- Renders landing page with product preview sections.
- On "Start learning", navigates to `/dashboard` (authenticated entry).

### Decisions and branches
- If unauthenticated, `/dashboard` requires sign-in (not yet built — authentication is Planned).

### Expected outcome
Student understands AQVERA's purpose and enters the application.

### Failure and recovery paths
- None on landing page (static).

### Relevant UI states
- Populated (landing content).

### Current implementation status
`Implemented` (landing page).

---

## Journey 2: Register and enter the application

**Actor:** New student  
**Goal:** Create an account and access the dashboard.

### Starting condition
Landing page, unauthenticated.

### User goal
Register and reach the student dashboard.

### User actions
1. Navigates to authentication page.
2. Registers with email and secure password.
3. System validates input, hashes password, creates profile and preferences.
4. System creates a session and issues a token with expiration.
5. Redirected to the Student Dashboard.

### System responses
- Validates email/password, returns errors for invalid/weak/duplicate.
- Creates session, redirects to `/dashboard`.

### Decisions and branches
- Invalid credentials → error message, remain on auth page.
- Email already registered → error, prompt to sign in.

### Expected outcome
Authenticated student on dashboard with empty course state.

### Failure and recovery paths
- Registration failure → inline error, retry.

### Relevant UI states
- Loading (auth in progress), Error (validation), Empty (no courses yet on dashboard).

### Current implementation status
`Planned` (authentication not yet built; dashboard shell exists, auth described in MVP_SCOPE Phase A).

---

## Journey 3: First-time onboarding

**Actor:** Newly registered student  
**Goal:** Understand the dashboard and create the first course.

### Starting condition
Authenticated, dashboard with no courses.

### User goal
Orient to the dashboard and create a first course.

### User actions
1. Views dashboard empty state ("No courses yet").
2. Reads guidance to create first course.
3. Clicks "Create your first course".
4. Fills course form (title, code, semester, subject domain, description).
5. Submits; course appears in list.

### System responses
- Shows empty state with primary action.
- Opens create-course dialog.
- On submit, calls API, adds course to list, closes dialog.

### Decisions and branches
- Invalid form → validation errors, remain in dialog.
- Cancel → dialog closes, no course created.

### Expected outcome
First course created and visible in the course library.

### Failure and recovery paths
- API failure → error banner, retry submit.

### Relevant UI states
- Empty, Loading, Validation error, Success, Populated.

### Current implementation status
`Partially Implemented` (course create dialog and API calls exist in `/courses` and `/dashboard`; backend endpoint required).

---

## Journey 4: Create the first course

**Actor:** Student  
**Goal:** Create a course for an academic subject.

### Starting condition
Authenticated, on `/courses` or `/dashboard`.

### User goal
Create a course with metadata.

### User actions
1. Clicks "Create course".
2. Opens create-course modal.
3. Fills required title; optional code, semester, subject domain, description, language.
4. Submits.

### System responses
- Validates title required.
- Creates course via API.
- Adds course to list.

### Decisions and branches
- Missing title → field error.
- API error → error banner.

### Expected outcome
New course appears in course library and dashboard.

### Failure and recovery paths
- Network failure → error, retry.

### Relevant UI states
- Empty (no courses), Loading (submitting), Validation error, Success, Populated.

### Current implementation status
`Partially Implemented` (frontend form + API calls present; backend required).

---

## Journey 5: Organize academic materials

**Actor:** Student  
**Goal:** Manage uploaded academic materials for a course.

### Starting condition
Course exists, on course workspace `/courses/[id]`.

### User goal
View and organize materials.

### User actions
1. Opens course workspace.
2. Views Materials section.
3. (Future) uploads, renames, deletes materials.

### System responses
- Shows Materials section (currently "Document upload — coming in Phase 2").

### Decisions and branches
- No materials → empty state with guidance.

### Expected outcome
Student knows where materials live and their status.

### Failure and recovery paths
- None yet (placeholder).

### Relevant UI states
- Empty (placeholder).

### Current implementation status
`Planned` (materials not yet built; honest placeholder present).

---

## Journey 6: Upload and process course materials

**Actor:** Student  
**Goal:** Upload a document and see it processed into a course structure.

### Starting condition
Course exists, on Materials section.

### User goal
Upload a PDF/document and monitor processing.

### User actions
1. Selects file(s) to upload.
2. System validates type/size, stores securely, starts processing job.
3. Views processing status (progress reporting).
4. System extracts text, sections, chunks, embeddings.

### System responses
- File validation errors (type, size, malicious).
- Processing job status: queued → processing → completed/failed.
- Extraction failure → explicit failure reason + retry.

### Decisions and branches
- Invalid file → error, no upload.
- Processing failure → retry or cancel.

### Expected outcome
Document processed; course structure proposed linked to learning objectives.

### Failure and recovery paths
- Upload failure → error message, retry.
- Extraction failure → explicit reason, retry or upload different file.

### Relevant UI states
- Empty, Loading (processing with progress), Partial data, Success, Server error.

### Current implementation status
`Planned` (Phase B; not built).

---

## Journey 7: Inspect the generated course structure

**Actor:** Student  
**Goal:** Review and edit the proposed course structure.

### Starting condition
Materials processed, course structure generated.

### User goal
Review modules, topics, learning objectives; edit before publishing.

### User actions
1. Opens Generated Course Review and Editing.
2. Views proposed course structure linked to learning objectives and source documents.
3. Edits title, objectives, module order.
4. Publishes to the Academic Course Workspace.

### System responses
- Presents proposed structure with source traceability.
- Saves edits.
- Publishes course.

### Decisions and branches
- Reject structure → edit or re-upload.
- Approve → publish.

### Expected outcome
Course published to workspace with editable structure.

### Failure and recovery paths
- Save failure → error, retry.

### Relevant UI states
- Populated, Loading, Validation error, Success.

### Current implementation status
`Planned` (Phase B/C; not built).

---

## Journey 8: Start a learning session

**Actor:** Student  
**Goal:** Begin studying a course.

### Starting condition
Published course in workspace.

### User goal
Start a lesson for the current topic/objective.

### User actions
1. Opens course workspace.
2. Selects active course.
3. Views current module, topic, learning objectives.
4. Starts a lesson.

### System responses
- Shows Course Learning Interface with current module/topic/objectives.
- Renders lesson (text, visualizations, activities).

### Decisions and branches
- No activities for objective → empty state.

### Expected outcome
Student is in a learning session with a clear current objective.

### Failure and recovery paths
- Lesson render failure → error, fallback.

### Relevant UI states
- Loading, Empty, Populated.

### Current implementation status
`Planned` (Phase C/D; not built).

---

## Journey 9: Receive an explanation

**Actor:** Student  
**Goal:** Understand a concept via lesson or AI tutor.

### Starting condition
In a learning session.

### User goal
Receive an explanation of the current topic.

### User actions
1. Views lesson content.
2. (Future) requests alternative explanation from AI Tutor.

### System responses
- Renders lesson with source attribution.
- AI Tutor passes Unified Learning Context, returns explanation with sources.

### Decisions and branches
- Provider failure → fallback to another provider or degraded response.

### Expected outcome
Student receives an attributable, validated explanation.

### Failure and recovery paths
- AI provider failure → fallback/degraded response with explanation.

### Relevant UI states
- Loading, Populated, Error.

### Current implementation status
`Planned` (Phase C; not built).

---

## Journey 10: Practice and answer questions

**Actor:** Student  
**Goal:** Complete an assessment for the current topic.

### Starting condition
In a learning session, assessment available.

### User goal
Answer questions and submit.

### User actions
1. Opens Assessment Interface.
2. Views questions linked to learning objectives (no correct answers shown before completion).
3. Answers questions.
4. Submits.

### System responses
- Presents questions, answer keys stored independently.
- Validates submission (deterministic for numerical/math; criteria+confidence for subjective).
- Does not reveal correct answers before completion unless activity permits.

### Decisions and branches
- Submit → evaluation.
- Incomplete → validation error.

### Expected outcome
Answers submitted for evaluation.

### Failure and recovery paths
- Evaluation failure → error, retry.

### Relevant UI states
- Loading, Populated, Validation error, Error.

### Current implementation status
`Planned` (Phase D; not built).

---

## Journey 11: Receive feedback

**Actor:** Student  
**Goal:** Understand what was correct/incorrect and why.

### Starting condition
Assessment submitted.

### User goal
Receive feedback and next steps.

### User actions
1. Views feedback (what understood, what weak, rationale, next steps).
2. Sees evidence sufficiency statement.

### System responses
- Generates feedback, records learning evidence, updates learner model.
- Communicates whether enough evidence exists for reliable judgment.

### Decisions and branches
- Insufficient evidence → explicit statement.

### Expected outcome
Student understands performance and next steps.

### Failure and recovery paths
- Feedback generation failure → error.

### Relevant UI states
- Populated, Error.

### Current implementation status
`Planned` (Phase D; not built).

---

## Journey 12: Follow an adaptive learning recommendation

**Actor:** Student  
**Goal:** Know what to study next and why.

### Starting condition
Assessment completed.

### User goal
Act on the adaptive recommendation.

### User actions
1. Receives recommendation (review, advance, difficulty adjustment, retention review).
2. Views rationale and evidence confidence.
3. Starts the recommended activity.

### System responses
- Computes next step via Adaptive Decision Engine.
- Presents recommendation with rationale and evidence confidence.
- Updates learner model and learning path.

### Decisions and branches
- Insufficient evidence → explicit "insufficient evidence for reliable judgment" message.

### Expected outcome
Student acts on an explainable recommendation.

### Failure and recovery paths
- Insufficient evidence → explicit message, student chooses review manually.

### Relevant UI states
- Empty (no recommendation), Populated, Error.

### Current implementation status
`Planned` (Phase D; not built).

---

## Journey 13: Review previous learning

**Actor:** Student  
**Goal:** Review mastery and what requires attention.

### Starting condition
Learning history exists.

### User goal
Review mastery by course/module/topic/objective.

### User actions
1. Opens Learning Progress and Analytics.
2. Views mastery levels, weak areas, retention reviews due.
3. Views assessment history and evidence counts.
4. Understands why each recommendation was made.

### System responses
- Displays mastery and analytics.
- Highlights weak areas and due reviews.

### Decisions and branches
- No data → empty state.

### Expected outcome
Student understands their learning status.

### Failure and recovery paths
- Analytics computation failure → loading/error.

### Relevant UI states
- Empty, Loading, Populated.

### Current implementation status
`Planned` (Phase D; `/learning` placeholder present).

---

## Journey 14: Return to an unfinished learning activity

**Actor:** Student  
**Goal:** Resume an interrupted activity.

### Starting condition
An in-progress lesson or assessment exists.

### User goal
Resume where they left off.

### User actions
1. Returns to course workspace or dashboard.
2. Finds "resume" entry point for the unfinished activity.
3. Resumes the activity.

### System responses
- Tracks current lesson/topic/objective in Unified Learning Context.
- Offers resume entry point.

### Decisions and branches
- No unfinished activity → normal course view.

### Expected outcome
Student resumes the unfinished activity.

### Failure and recovery paths
- Lost context → restart current objective.

### Relevant UI states
- Populated, Empty.

### Current implementation status
`Not Designed`.

---

## Journey 15: Manage courses and preferences

**Actor:** Student  
**Goal:** Maintain courses and account settings.

### Starting condition
Authenticated, one or more courses.

### User goal
Edit, archive, delete courses; manage preferences.

### User actions
1. Edits course metadata (edit dialog).
2. Archives a course.
3. Views archived courses ("Show archived").
4. Deletes a course (with confirmation).
5. (Future) manages account preferences, language.

### System responses
- Saves edits, toggles archive, soft-deletes, hard-deletes with confirmation.
- Settings page shows account info (local dev mode notice).

### Decisions and branches
- Delete requires confirmation dialog.
- Archive toggles visibility.

### Expected outcome
Courses and preferences reflect student's choices.

### Failure and recovery paths
- Delete/archive failure → error, retry.

### Relevant UI states
- Populated, Loading, Destructive confirmation, Empty.

### Current implementation status
`Partially Implemented` (course edit/archive/delete UI exists in `/courses` and `/dashboard`; `/settings` shell present, preferences not built).

---

## Implementation Status Summary

| Journey | Label |
|---------|-------|
| 1. Discover AQVERA | Implemented |
| 2. Register and enter | Planned |
| 3. First-time onboarding | Partially Implemented |
| 4. Create the first course | Partially Implemented |
| 5. Organize academic materials | Planned |
| 6. Upload and process materials | Planned |
| 7. Inspect generated course structure | Planned |
| 8. Start a learning session | Planned |
| 9. Receive an explanation | Planned |
| 10. Practice and answer questions | Planned |
| 11. Receive feedback | Planned |
| 12. Follow adaptive recommendation | Planned |
| 13. Review previous learning | Planned |
| 14. Return to unfinished activity | Not Designed |
| 15. Manage courses and preferences | Partially Implemented |
