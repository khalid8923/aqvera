# DOMAIN_BOUNDARIES.md

# AQVERA — Domain Boundaries

## Principle

Each domain owns its data and business logic. Cross-domain communication happens through well-defined interfaces and the Unified Learning Context Service. No domain reaches into another domain's database tables directly.

## Domain 1: Identity & Access

**Owns:** Users, User Profiles, User Preferences, Sessions.  
**Responsibilities:** Authentication, authorization, password hashing, session management, token expiration, password recovery, account protection.  
**Exposed via:** Auth service (auth middleware, permission checks).  
**Depends on:** Database, Config, Secrets.  
**Dependents:** All domains (via auth context).

## Domain 2: Academic Structure

**Owns:** Courses, Modules, Lessons, Topics, Learning Objectives, Prerequisites, Course Memberships.  
**Responsibilities:** Course structure integrity, prerequisite graph, objective hierarchy, lesson-topic mapping.  
**Exposed via:** Course service API.  
**Depends on:** Database, Identity (ownership/access).  
**Dependents:** Content Processing, Teaching Engine, Assessment Engine, Adaptive Engine.

## Domain 3: Content Processing

**Owns:** Uploaded Materials, Document Versions, Processing Jobs, Extracted Sections, Content Chunks, Source References, Embeddings.  
**Responsibilities:** File validation, storage, extraction, OCR, chunking, embedding, vector indexing, job lifecycle.  
**Exposed via:** Processing job API, vector search interface.  
**Depends on:** Database, Object Storage, Background Worker, AI Providers (for extraction assistance), Academic Structure (course linkage).  
**Dependents:** Academic Structure (course generation input), Knowledge Retrieval.

## Domain 4: Teaching

**Owns:** Teaching Profiles, Teaching Methodology Versions, Lesson Content, Learning Activities.  
**Responsibilities:** Applying the versioned teaching methodology, domain-specific instructional behavior, output contracts, validation rules.  
**Exposed via:** Teaching Engine API.  
**Depends on:** Database, AI Providers (via Abstraction), Learning Context.  
**Dependents:** Adaptive Engine, Content Generation, Assessment Engine.

## Domain 5: AI Infrastructure

**Owns:** AI Providers, Model Configurations, AI Task Records, Usage Records.  
**Responsibilities:** Provider abstraction, model selection, credentials management, request/response normalization, structured output, streaming, token/usage tracking, cost estimation, timeouts, retries, rate limiting, error classification, availability, fallback policies, capability metadata.  
**Exposed via:** AI Provider Abstraction Layer interface.  
**Depends on:** Config, Secrets.  
**Dependents:** Teaching Engine, Content Generation, Evaluation Engine.

## Domain 6: Assessment

**Owns:** Assessments, Questions, Question Options, Answer Keys, Assessment Attempts, Student Responses, Evaluation Results.  
**Responsibilities:** Question generation (linked to objectives), question validation, difficulty classification, answer evaluation (deterministic + subjective), feedback generation, evidence recording.  
**Exposed via:** Assessment API.  
**Depends on:** Database, Teaching Engine (methodology), AI Providers (via Abstraction, validated), Academic Structure (objectives).  
**Dependents:** Adaptive Engine (evidence input).

## Domain 7: Adaptive Learning

**Owns:** Learner Models, Knowledge States, Learning Evidence, Learning Recommendations, Learning Paths, Retention Reviews.  
**Responsibilities:** Knowledge tracing, mastery estimation, adaptive decision pipeline, learning path generation, retention scheduling, adaptive feedback.  
**Exposed via:** Adaptive Engine API, Learner Model query interface.  
**Depends on:** Database, Assessment (evidence), Academic Structure (prerequisites), Teaching Engine (feedback content).  
**Dependents:** Teaching Engine (feedback), UI (progress analytics).

## Domain 8: Visual Learning

**Owns:** Visualization definitions, visual activity records, visual asset metadata.  
**Responsibilities:** Deterministic rendering from structured data, AI-generated visual descriptions, static assets, interactive simulations, visualization interface receiving learning context.  
**Exposed via:** Visual Learning API.  
**Depends on:** Database, Learning Context, Academic Structure (objectives).  
**Dependents:** Course Learning Interface, AI Tutor Interface.

## Domain 9: Application (Cross-Cutting)

**Owns:** Notifications, User Feedback, Audit Events, Unified Learning Context.  
**Responsibilities:** Context ownership/persistence/retrieval/update rules, notifications, audit logging, feedback collection.  
**Exposed via:** Context service, notification service, audit service.  
**Depends on:** Database, Identity.  
**Dependents:** All domains.

## Dependency Direction Summary

```
Identity ← All domains (auth context)
Academic Structure → Content Processing, Teaching, Assessment, Adaptive
Content Processing → Knowledge Retrieval
Teaching → Adaptive, Content Generation, Assessment
AI Infrastructure → Teaching, Content Generation, Evaluation
Assessment → Adaptive
Adaptive → Teaching (feedback), UI
Visual Learning ← Learning Context, Academic Structure
Application (Context) → All domains
```

**No circular dependencies.** Any new domain must declare its dependencies and be approved by the Architecture Agent.

## Context Ownership

The Unified Learning Context Service owns the learning context. Domains read context through the service; they do not independently reconstruct student knowledge from chat history.

## Data Ownership Rule

Each domain is the sole writer of its own entities. Other domains read via service interfaces. Derived/cached data is marked as such and owned by the deriving domain.
