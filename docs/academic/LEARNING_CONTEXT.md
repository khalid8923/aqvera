# LEARNING_CONTEXT.md

# AQVERA — Learning Context

## Purpose

All AQVERA learning tools share a consistent academic context. The Learning Context model ensures that every tool understands the student's current academic situation without independently reconstructing knowledge from chat history.

## Learning Context Model (DECIDED)

| Field | Description | Persistence |
|-------|-------------|-------------|
| student_id | Student identity within the application | Persisted (Users) |
| active_course_id | The course currently being studied | Temporary (current session) |
| current_module_id | Current module within the course | Temporary |
| current_topic_id | Current topic within the module | Temporary |
| learning_objectives | Objectives relevant to current context | Derived from Academic Structure |
| uploaded_sources | Relevant uploaded source materials | Persisted (UploadedMaterials) |
| current_lesson_id | The lesson currently being viewed | Temporary |
| mastery_evidence | Student's mastery evidence (from learner model) | Derived (LearnerModel/KnowledgeStates) |
| recent_assessment_results | Recent assessment outcomes | Derived (AssessmentAttempts/EvaluationResults) |
| active_learning_path | Current learning path | Persisted (LearningPaths) |
| teaching_profile | Relevant teaching profile | Persisted (TeachingProfiles) |

## Context Ownership (DECIDED)

- The **Unified Learning Context Service** owns the learning context.
- Domains read context through the service; they do not independently reconstruct student knowledge from chat history.
- Context is set when a student enters a course/workspace and cleared when they leave or it expires.

## Context Categories (DECIDED)

| Category | Examples | Persistence |
|----------|----------|-------------|
| **Temporary** | active_course_id, current_module_id, current_topic_id, current_lesson_id | Session-scoped; cleared on logout or context switch |
| **Persisted** | student_id, uploaded_sources, active_learning_path, teaching_profile | Database-persisted; survives across sessions |
| **Learner Model** | mastery_evidence, recent_assessment_results | Part of LearnerModel/KnowledgeStates; authoritative |

## Context Retrieval and Update Rules (DECIDED)

1. **Set context** when a student selects a course in the Academic Course Workspace.
2. **Update context** as the student navigates modules, topics, and lessons.
3. **Read context** through the Learning Context Service API; no direct database reads by UI components.
4. **Clear context** on logout, course change, or session expiration.
5. **No tool reconstructs knowledge from chat history** — all academic state comes from the context service and learner model.

## Context Examples (DECIDED)

### Example 1: Quiz Completion → AI Tutor

A student completes a quiz and opens the AI Tutor:
- Context includes: active_course, current_topic, recent_assessment_results (mistakes), mastery_evidence for related objectives.
- The tutor understands the relevant mistakes because they are in the context.
- Teaching Engine preserves the academic topic and source context.

### Example 2: Mathematical Visualization

A student views a mathematical visualization:
- Context includes: active_course, current_topic, current_lesson, learning_objectives.
- The visualization is associated with the corresponding learning objective.
- Visual activity is recorded against the objective in the learner model.

### Example 3: Different Explanation Request

A student asks for a different explanation:
- Teaching Engine preserves the academic topic and source context from the Learning Context.
- The explanation is generated within the same objective and source frame.

## Context API (PROPOSED)

```
GET /context          → Returns current learning context
PUT /context/course   → Sets active course
PUT /context/topic    → Sets current topic
PUT /context/lesson   → Sets current lesson
DELETE /context       → Clears context (logout/switch)
```

## Context and Learner Model Relationship

- Learning Context points to the current academic focus.
- Learner Model (Adaptive domain) holds the authoritative mastery data.
- Context references LearnerModel data by ID; does not duplicate it.
- When mastery updates, context consumers see the update through the context service (derived data).

## Privacy

- Context contains only data the student is authorized to see.
- Context is scoped to the current user; no cross-user leakage.
- Sensitive data (document text, PII) not included in context passed to AI providers unless necessary and sanitized.
