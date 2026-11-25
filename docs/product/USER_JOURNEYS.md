# USER_JOURNEYS.md

# AQVERA — User Journeys

## Journey 1: Onboarding and Account Creation

**Actor:** New student  
**Goal:** Create an account and access the student dashboard.

### Steps
1. Student navigates to the authentication page.
2. Student registers with email and secure password.
3. System validates input, hashes password, creates user profile and preferences.
4. System creates a session and issues a token with expiration.
5. Student is redirected to the Student Dashboard.

### Key States
- Empty: No courses yet; dashboard shows "Get started" state.
- Loading: Authentication in progress.
- Error: Invalid credentials, weak password, email already registered.

### Required Data
- User identity, credentials, preferences, session.

---

## Journey 2: Material Upload and Course Creation

**Actor:** Student  
**Goal:** Upload academic material and generate a course.

### Steps
1. Student opens the Material Upload and Processing Center.
2. Student uploads a document (PDF, etc.).
3. System validates file type and size, stores securely, starts a processing job.
4. Background worker extracts text, creates document versions, extracts sections, chunks content, generates embeddings.
5. Student opens Generated Course Review and Editing.
6. System presents a proposed course structure linked to learning objectives.
7. Student reviews and edits the course; system saves changes.
8. Student publishes the course to the Academic Course Workspace.

### Key States
- Processing: Upload job in progress with progress reporting.
- Empty: No uploaded materials.
- Error: Extraction failure, unsupported file type, file too large.

### Required Data
- Uploaded materials, document versions, processing jobs, extracted sections, content chunks, embeddings, source references.

---

## Journey 3: Course Learning and Assessment

**Actor:** Student  
**Goal:** Study a course and complete assessments.

### Steps
1. Student opens the Academic Course Workspace and selects an active course.
2. System shows the Course Learning Interface with the current module, topic, and learning objectives.
3. Student views a lesson (text, visualizations, activities).
4. Student opens the Assessment Interface for the current topic.
5. System presents questions linked to learning objectives; no correct answers shown before completion.
6. Student submits answers.
7. Evaluation Engine validates answers (deterministic for numerical/math; criteria+confidence for subjective).
8. System generates feedback and records learning evidence.
9. Adaptive Engine updates the learner model.
10. Adaptive Engine recommends the next activity (review, advance, difficulty adjustment, retention review).

### Key States
- Loading: Lesson/assessment rendering.
- Empty: No activities for the current objective.
- Error: Assessment evaluation failure, invalid AI output.

### Required Data
- Course, modules, lessons, topics, learning objectives, prerequisites, questions, answer keys, learner model, learning evidence.

---

## Journey 4: Adaptive Recommendation and Review

**Actor:** Student  
**Goal:** Understand what to study next and why.

### Steps
1. Student completes an assessment or activity.
2. Adaptive Engine computes the next step: what to learn next, prerequisite attention, review vs. advance, difficulty level.
3. System presents the recommendation with rationale and evidence confidence.
4. Student acts on the recommendation (starts lesson, reviews, or takes retention review).
5. System updates the learner model and learning path.

### Key States
- Empty: No recommendation possible (insufficient evidence).
- Error: Insufficient evidence for reliable judgment — system states this explicitly.

### Required Data
- Learner model, knowledge states, learning evidence, learning recommendations, learning paths, retention reviews.

---

## Journey 5: AI Tutor Interaction

**Actor:** Student  
**Goal:** Get help on a specific academic topic.

### Steps
1. Student opens the AI Tutor Interface from the Course Learning Interface.
2. System passes the Unified Learning Context (active course, topic, objectives, recent mistakes, mastery evidence).
3. Student asks a question or requests a different explanation.
4. Teaching Engine preserves the academic topic and source context.
5. AI Orchestration selects the appropriate model and workflow.
6. Knowledge Retrieval fetches relevant academic evidence.
7. Content Generation produces the explanation; Teaching Engine applies methodology.
8. System returns the explanation with source attribution.

### Key States
- Empty: No context available (student not in a course).
- Error: Provider failure — fallback to another provider or degraded response.

### Required Data
- Learning context, learner model, recent assessment results, uploaded sources, teaching profile.

---

## Journey 6: Visual Learning Activity

**Actor:** Student  
**Goal:** View a deterministic visualization for a mathematical concept.

### Steps
1. Student is in a mathematics lesson involving a function or equation.
2. System opens the Visual Learning Interface with the current learning context.
3. System renders a deterministic visualization from structured data (function graphing, equation visualization).
4. Visualization is associated with the corresponding learning objective.
5. Student interacts with the visualization; interaction may produce learning evidence.

### Key States
- Empty: No visualization available for the current objective.
- Error: Rendering failure — fallback to static illustrative asset or description.

### Required Data
- Learning context, learning objective, structured visualization data, learner model.

---

## Journey 7: Progress and Analytics Review

**Actor:** Student  
**Goal:** Review mastery and what requires attention.

### Steps
1. Student opens Learning Progress and Analytics.
2. System displays mastery by course, module, topic, and objective.
3. System highlights weak areas and retention reviews due.
4. System shows assessment history and evidence counts.
5. Student understands why each recommendation was made.

### Key States
- Empty: No learning data yet.
- Loading: Analytics computation in progress.

### Required Data
- Learner model, knowledge states, learning evidence, learning paths, retention reviews, assessment attempts.
