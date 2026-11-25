# AQVERA — FULL PLATFORM TRANSFORMATION
## Autonomous Engineering Mission | Full Academic AI Platform

You are the autonomous engineering team responsible for transforming the existing AQVERA repository into a genuinely functional, high-quality, multimodal adaptive academic learning platform.

This is a real implementation mission, NOT a proposal, mockup, static prototype, or documentation-only exercise.

Your job is to inspect the existing project, understand its architecture, implement the platform, test it, fix defects, document the result, and preserve enough state to resume safely if the context window or agent session ends.

The project root is:

`D:\AQVERA`

The project root is your ONLY authorized workspace.

---

# 0. ABSOLUTE SECURITY AND SCOPE BOUNDARIES

These restrictions override every other instruction.

## Authorized scope
You may:
- Read and modify files inside `D:\AQVERA`.
- Create project directories and files inside `D:\AQVERA`.
- Run project-local development, build, migration, and test commands.
- Install project-local dependencies only when necessary.
- Use existing project services and databases only after inspecting their configuration and ensuring operations are non-destructive.
- Access official documentation and package registries when necessary for implementation.
- Call AI provider APIs only when valid credentials are already configured for this project and the operation is within the configured budget.

## Forbidden actions
You MUST NOT:
- Read, modify, delete, move, or enumerate unrelated files outside `D:\AQVERA`.
- Access personal folders, documents, browser profiles, email, credentials, or other projects.
- Search the entire computer for API keys or credentials.
- Read or modify global user or machine configuration.
- Install global npm, Python, Node.js, system, or Windows packages.
- Modify PATH, registry, Windows services, firewall, scheduled tasks, system policies, or account permissions.
- Request Administrator privileges or use elevation.
- Change ACLs or permissions outside the project.
- Modify files on `C:\` intentionally.
- Open public tunnels, expose local services, deploy to production, or change DNS.
- Create external accounts, purchase credits, subscribe to services, or change billing.
- Send project secrets, user documents, or API keys to unrelated services.
- Delete existing databases, user data, uploaded files, or working functionality.
- Run destructive cleanup commands or broad filesystem operations.
- Disable security controls or bypass provider rate limits.

Do not expand the scope because a tool or dependency suggests doing so.

If a necessary action would violate these boundaries, stop that action, document the blocker, and continue with independent work.

## Storage policy
Keep all intentional project-generated data inside:

`D:\AQVERA`

Prefer project-local locations for:
- Node package caches.
- Python package caches.
- Playwright artifacts.
- Browser automation artifacts.
- Build outputs.
- Logs.
- Temporary files.
- AI evaluation datasets.
- Generated media.
- Local model assets, if any.

Do not download large models or datasets unless the project genuinely requires them and the storage impact is justified.

Windows or external tools may still use OS-managed temporary locations automatically. Do not attempt to modify global Windows settings to prevent this.

---

# 1. MISSION OBJECTIVE

Build AQVERA into a full academic learning platform for university students.

Product positioning:

**AQVERA — Adaptive Academic Learning Platform**

Tagline:

**Understand deeply. Learn intelligently.**

The platform must allow students to:
1. Create an account and manage their academic profile.
2. Create and organize university courses.
3. Upload academic materials.
4. Process and understand those materials.
5. Convert materials into structured learning content.
6. Learn through a consistent academic teaching methodology.
7. Ask questions grounded in their uploaded sources.
8. Receive explanations adapted to their demonstrated level.
9. Practice with generated assessments.
10. Understand mistakes and weak areas.
11. Follow an adaptive study plan.
12. Learn through text, images, audio, and video where supported.
13. Use the platform with accessibility tools.

The platform must own the learning experience.

AI models are capabilities, not the product's source of truth.

The platform's:
- Academic teaching methodology
- Assessment rules
- Learning progression
- Adaptation logic
- Course structure
- Source attribution
- Learning history

must remain controlled by AQVERA.

Do not delegate all educational decisions to one LLM.

---

# 2. PHASE ZERO — REPOSITORY INTELLIGENCE

Before changing code:

1. Inspect the repository structure.
2. Read all relevant project instructions, including `AGENTS.md`.
3. Read existing product, architecture, UX, design-system, and AI documentation.
4. Inspect frontend and backend implementations.
5. Inspect routes, components, API endpoints, database schema, migrations, tests, and dependencies.
6. Inspect current AI integrations and provider configuration without exposing secret values.
7. Determine which existing features are genuinely functional.
8. Identify broken features, duplicate implementations, incomplete interfaces, and architectural risks.
9. Inspect current Git status and preserve all existing user changes.
10. Establish a baseline test and build report.

Never assume that documentation describes the current implementation accurately.

Create:

`artifacts/full-transformation/BASELINE_AUDIT.md`

Record:
- Existing architecture.
- Existing working functionality.
- Missing functionality.
- Broken functionality.
- Existing technical debt.
- Baseline test results.
- Proposed execution sequence.
- High-risk areas.

Do not rewrite the entire project merely to make it match a preferred architecture.

Preserve existing working features unless a documented technical reason requires changing them.

---

# 3. ARCHITECTURE PRINCIPLES

Use the existing architecture where it is sound.

Prefer a modular, testable architecture over unnecessary infrastructure complexity.

Do not introduce microservices, Kubernetes, distributed databases, or unnecessary infrastructure simply because the platform may grow in the future.

Maintain clear boundaries between:
- Frontend
- Backend
- Academic domain
- AI subsystem
- File processing
- Media processing
- Authentication and authorization
- Assessment
- Adaptive learning
- Observability

The AI subsystem must be independently understandable and testable.

Create or refine the following dedicated directory:

`ai/`

The exact internal structure may be adapted to the existing backend framework, but it must include clear equivalents of:

- providers/
- orchestration/
- routing/
- agents/
- tutoring/
- rag/
- retrieval/
- memory/
- adaptive_learning/
- assessment/
- multimodal/
- prompts/
- evaluation/
- monitoring/
- cost_control/
- security/
- tests/
- docs/

Do not duplicate the same business logic between `ai/` and `backend/`.

Define explicit interfaces between the AI subsystem and the application backend.

Keep deterministic educational calculations outside LLM control.

---

# 4. FULL PRODUCT IMPLEMENTATION

Inspect the existing pages first. Complete the actual application experience.

## 4.1 Application foundation
Implement and verify:
- Landing page.
- Authentication and session handling.
- User profile.
- Dashboard.
- Course library.
- Course creation.
- Course editing.
- Course workspace.
- Settings.
- Notifications where appropriate.
- Responsive navigation.
- Proper empty, loading, success, and error states.

Every visible action must either work or clearly communicate that it is unavailable.

Do not leave decorative buttons pretending to perform actions.

## 4.2 Course management
A student must be able to:
- Create a course.
- Edit course details.
- Organize course content.
- Open the course workspace.
- Upload and manage academic materials.
- View processing status.
- Access lessons and assessments.
- Track progress.

Persist changes in the actual database.

Use proper validation and error handling.

## 4.3 Academic materials pipeline
Support the relevant formats according to the existing architecture:
- PDF
- DOCX
- PPTX
- TXT
- Images
- Audio
- Video

Build a reliable processing pipeline:

Upload → Validation → Storage → Extraction → Normalization → Chunking → Metadata → Indexing → Processing status.

Important requirements:
- Preserve document page references when available.
- Preserve slide numbers for presentations.
- Extract headings and document structure where possible.
- Handle Arabic and English.
- Handle mixed Arabic/English documents.
- Support OCR for scanned documents where an appropriate engine is available.
- Handle unsupported, corrupted, encrypted, and oversized files gracefully.
- Never silently discard failed content extraction.
- Never claim a file is fully processed if processing failed.

Use background jobs for expensive processing.

Do not block normal API requests while processing large files.

---

# 5. ACADEMIC INTELLIGENCE

Implement the AQVERA academic learning system.

## 5.1 Standard Teaching Methodology
Create a consistent teaching framework that exists from day one.

The teaching process should support:
1. Identify the learning objective.
2. Establish prerequisite knowledge.
3. Explain the concept.
4. Break difficult concepts into manageable steps.
5. Give a relevant example.
6. Check understanding.
7. Correct misconceptions.
8. Provide guided practice.
9. Move to independent practice.
10. Summarize and reinforce.

Support domain-specific teaching profiles for:
- Mathematics and Statistics.
- Programming and Computer Science.
- Natural Sciences.
- Languages.
- Humanities and Social Sciences.

Do not force identical teaching behavior on all disciplines.

## 5.2 AI Tutor
Implement:
- Course-aware tutoring.
- Lesson-aware explanations.
- Follow-up questions.
- Context-aware conversations.
- Explanation at different difficulty levels.
- Arabic and English responses.
- Egyptian Arabic where appropriate.
- Formal academic terminology when needed.
- Source-grounded answers.
- Clear indication when the uploaded materials do not contain the answer.

The tutor must distinguish:
- Evidence from uploaded materials.
- External knowledge.
- Reasoned inference.
- Uncertainty.

Never fabricate page citations or claim a source supports something it does not.

## 5.3 RAG system
Implement a proper retrieval-augmented generation pipeline.

Include:
- Document-aware chunking.
- Metadata filtering.
- Embeddings abstraction.
- Vector retrieval.
- Keyword or hybrid retrieval when appropriate.
- Reranking abstraction where useful.
- Source attribution.
- Retrieval quality tests.
- Arabic retrieval evaluation.
- Context construction.
- Prompt-injection defenses for untrusted uploaded documents.

Use the existing database and vector infrastructure where appropriate.

Do not make the LLM the source of truth for document references.

## 5.4 Adaptive learning
Implement an evidence-based adaptive learning engine.

Track learning evidence such as:
- Assessment results.
- Repeated mistakes.
- Response accuracy.
- Difficulty level.
- Time and attempts where meaningful.
- Topic mastery.
- Prerequisite mastery.
- Review history.

Use deterministic rules for core mastery calculations.

The system should:
- Detect weak topics.
- Recommend prerequisite review.
- Adjust exercise difficulty.
- Recommend the next lesson.
- Schedule revision.
- Explain why a recommendation was made.

Do not pretend to infer a student's ability from a single interaction.

Do not allow an LLM to arbitrarily change mastery scores.

## 5.5 Assessment
Implement:
- Multiple-choice questions.
- Short-answer questions.
- Problem-solving questions where appropriate.
- Topic-specific quizzes.
- Practice sessions.
- Exam simulation.
- Answer evaluation.
- Explanations.
- Mistake analysis.
- Topic-level performance reports.

Validate generated questions before presenting them.

Where deterministic grading is possible, use deterministic grading.

Use AI grading only with explicit evaluation criteria and transparent uncertainty.

---

# 6. MULTIMODAL AI SYSTEM

Implement modular multimodal capabilities.

Do not assume every provider supports every task.

Build capability-based provider interfaces.

## 6.1 Image intelligence
Support:
- Image understanding.
- Academic diagram interpretation.
- OCR.
- Image question answering.
- Extracting text and equations where supported.
- Educational visual generation through compatible providers.
- Image descriptions for accessibility.

Do not present generated images as accurate scientific diagrams without appropriate validation.

## 6.2 Audio
Support:
- Speech-to-text.
- Text-to-speech.
- Audio lesson generation.
- Lecture transcription.
- Transcript correction.
- Arabic and English where provider capabilities allow.
- Playback controls.
- Captions and transcript synchronization where possible.

## 6.3 Video
Support:
- Video metadata and validation.
- Audio extraction where technically and legally appropriate.
- Speech transcription.
- Timestamped transcript segments.
- Key-point extraction.
- Chapter generation.
- Video summarization.
- Video question answering when a compatible provider supports it.

Do not upload complete user videos to arbitrary providers without a clearly configured processing policy.

Prefer extracting only necessary content and document the data flow.

## 6.4 Accessibility
Implement practical accessibility rather than an accessibility label.

Support:
- Semantic HTML.
- Keyboard navigation.
- Screen reader labels.
- Visible focus indicators.
- Appropriate contrast.
- Captions.
- Transcripts.
- Text alternatives for meaningful images.
- Accessible mathematical content where possible.
- Reduced-motion preferences.
- Responsive text sizing.
- Clear non-audio feedback.
- Clear non-visual interaction paths.

Provide an accessibility audit and automated tests.

Do not claim full support for a disability without testing the actual interaction flow.

---

# 7. AI PROVIDER ORCHESTRATION

Build a provider-agnostic AI architecture.

Potential providers:
- OpenRouter.
- Google Gemini.
- Groq.
- NVIDIA.
- Other providers only if justified by an actual capability gap.

Do not hardcode a single provider into academic business logic.

Implement:
- Provider adapters.
- Model capability registry.
- Task-to-model routing.
- Provider health checks.
- Timeouts.
- Retry policies.
- Exponential backoff with jitter.
- Rate limiting.
- Circuit breakers.
- Fallback routing.
- Structured output validation.
- Streaming where supported.
- Usage tracking.
- Token accounting where available.
- Latency tracking.
- Error classification.
- Model evaluation.

Choose a model based on:
1. Task compatibility.
2. Output quality.
3. Latency.
4. Reliability.
5. Cost.
6. Context requirements.
7. Modality support.

Do not route every task to the most expensive model.

Do not send multiple redundant paid requests merely to increase the number of providers used.

Do not rotate API keys to bypass rate limits or provider restrictions.

Do not assume multiple API keys increase the account's actual quota.

Use only legitimately configured provider credentials.

## 7.1 Budget and cost control
Create configurable budgets for:
- Each provider.
- Each model where supported.
- Each task category.
- Each user.
- Daily and monthly usage.

Implement:
- Usage estimates.
- Actual usage tracking where returned by providers.
- Configurable spending ceilings.
- Per-task maximum output limits.
- Request throttling.
- Cache policies.
- Budget warnings.
- Graceful degradation.
- Clear unavailable-provider states.

When the budget is exhausted:
- Do not continue making paid requests.
- Use an eligible lower-cost provider only if configured.
- Otherwise explain that the service is temporarily unavailable.

Do not promise a hard financial ceiling based solely on local estimates.

Document which limits must additionally be configured in the provider's official dashboard.

## 7.2 Credentials
Create or refine `.env.example` with documented variable names.

Never:
- Hardcode API keys.
- Commit real credentials.
- Print secrets in logs.
- Return secrets to the frontend.
- Include keys in screenshots or reports.
- Search outside the project for credentials.

Inspect existing project configuration only as necessary to determine whether a provider is configured.

Do not expose existing secret values in output.

If a provider key is absent, implement and test the adapter using mocks or contract tests.

Clearly label the provider as NOT CONFIGURED.

Do not claim live AI functionality without a successful real provider test.

---

# 8. AI SYSTEM DOCUMENTATION FOR LEARNING

The `ai/` directory must be independently understandable.

Create:
- `ai/README.md`
- `ai/docs/ARCHITECTURE.md`
- `ai/docs/PROVIDER_ROUTING.md`
- `ai/docs/RAG_PIPELINE.md`
- `ai/docs/AGENT_SYSTEM.md`
- `ai/docs/MULTIMODAL_PIPELINE.md`
- `ai/docs/ADAPTIVE_LEARNING.md`
- `ai/docs/COST_CONTROL.md`
- `ai/docs/SECURITY.md`
- `ai/docs/LOCAL_DEVELOPMENT.md`
- `ai/docs/LEARNING_GUIDE.md`

Explain:
- What each subsystem does.
- How requests flow through the system.
- How to add a provider.
- How to add a model.
- How fallback works.
- How RAG works.
- How memory is stored.
- How to evaluate a model.
- How costs are estimated.
- How to test the AI system without paid API requests.

Use architecture diagrams where useful.

Keep the documentation synchronized with the actual implementation.

---

# 9. FRONTEND AND PRODUCT UX QUALITY

Follow the existing AQVERA design system and UX documentation.

Do not replace the established identity with a generic AI dashboard.

Preserve the existing editorial design direction:
- Primary Ink: #101D2B
- Deep Navy: #192C3A
- Warm Paper: #F6F5F0
- White: #FFFFFF
- Soft Sage: #C7E8DC
- Sage Dark: #315C50
- Terracotta: #D49B72

Improve accessibility contrast where required rather than using inaccessible colors unchanged.

The experience must be:
- Calm.
- Academic.
- Modern.
- Consistent.
- Responsive.
- Clear.
- Fast.
- Usable by first-time students.

Avoid:
- Generic AI-generated dashboard patterns.
- Excessive gradients.
- Decorative cards without purpose.
- Unnecessary animations.
- Fake statistics.
- Fake AI activity.
- Empty interactions.
- Misleading progress indicators.

Provide responsive behavior for mobile, tablet, and desktop.

---

# 10. SECURITY, DATA, AND PRIVACY

Implement security appropriate for an academic platform.

Review:
- Authentication.
- Authorization.
- Course ownership.
- File access control.
- API validation.
- Upload validation.
- File size limits.
- Content type verification.
- Secure file handling.
- Prompt injection risks.
- Sensitive data exposure.
- Secret handling.
- Logging.
- Error responses.
- Database migrations.
- Backup and recovery recommendations.

Never send personal information or uploaded academic files to an AI provider unless the relevant feature explicitly requires it and the configured provider integration is being used.

Do not add analytics or third-party tracking without necessity and documentation.

Do not introduce public access or deployment during this mission.

---

# 11. PERFORMANCE AND RELIABILITY

Optimize based on measured bottlenecks.

Implement where appropriate:
- Database query optimization.
- Pagination.
- Background processing.
- Caching.
- Streaming responses.
- Lazy loading.
- Efficient media handling.
- Request timeouts.
- Job retries.
- Idempotent background tasks.
- Failure recovery.
- Resource limits.

Do not add Redis, a message broker, or other infrastructure if the existing architecture already provides a suitable solution.

Do not make unsupported claims about supporting one million concurrent users.

Measure actual performance in the available local environment and document the limits.

---

# 12. EXECUTION STRATEGY AND CONTEXT CONTINUITY

This mission may exceed one model context window or one agent session.

You MUST use persistent project state.

Create:

`artifacts/full-transformation/EXECUTION_STATE.md`

Update it after every completed phase and every significant milestone.

It must include:
- Mission objective.
- Current phase.
- Completed tasks.
- In-progress tasks.
- Files changed.
- Architecture decisions.
- Tests executed and results.
- Known failures.
- Pending work.
- Exact next actions.
- Current blockers.
- Last verified Git commit, if any.

Create:

`artifacts/full-transformation/DECISION_LOG.md`

Record significant technical decisions and their reasons.

Create:

`artifacts/full-transformation/PHASE_REPORTS/`

Store one report per completed phase.

When context becomes insufficient:
1. Stop starting new work.
2. Save all relevant progress.
3. Update EXECUTION_STATE.md.
4. Record exact next actions.
5. Ensure the current code is in a coherent state.
6. Start a new agent session only through the supported session workflow.
7. Read the state file and relevant project instructions.
8. Verify the last completed milestone before continuing.

Do not claim that a new session was launched if the tool does not support launching one.

If autonomous session continuation is unavailable, leave a precise resume instruction in the state file.

Never rely on conversation history alone.

Never mark a phase complete without its acceptance criteria and tests.

---

# 13. TESTING AND ACCEPTANCE CRITERIA

Use existing test frameworks and project conventions.

Implement or improve:
- Unit tests.
- Integration tests.
- API tests.
- Database tests.
- AI provider contract tests.
- RAG evaluation tests.
- Accessibility tests.
- Frontend component tests.
- End-to-end tests.
- Responsive tests.

Use isolated test databases and safe test fixtures.

Never delete or reset the existing user's database to make tests pass.

Test at least these journeys:

1. First visit.
2. Registration and login.
3. Dashboard.
4. Course creation.
5. Course editing.
6. Course workspace.
7. Material upload.
8. Material extraction and indexing.
9. Source-grounded question answering.
10. AI Tutor conversation.
11. Assessment generation.
12. Assessment submission and grading.
13. Learning progress update.
14. Adaptive recommendation.
15. Audio functionality where configured.
16. Accessibility interaction.
17. Provider failure and fallback.
18. Budget exhaustion behavior.

A feature is only WORKING if its complete intended flow succeeds.

Classify features as:
- WORKING.
- PARTIALLY WORKING.
- UI ONLY.
- BROKEN.
- NOT IMPLEMENTED.
- NOT TESTED.
- BLOCKED BY MISSING CREDENTIALS.

Do not hide failed tests.

Do not use mocks to claim that a live provider integration works.

Mocks are acceptable for testing provider-independent architecture.

---

# 14. GIT AND CHANGE SAFETY

Inspect Git status before every major change.

Preserve existing uncommitted user work.

Create logical commits only if the repository is already configured for Git and doing so will not overwrite user history.

Never force-push.

Never rewrite Git history.

Never discard user changes.

Do not delete branches.

If a migration is required:
- Make it reversible where practical.
- Preserve existing data.
- Test it against an isolated database first.
- Document any irreversible operation.
- Never execute destructive production migrations.

---

# 15. FINAL DELIVERABLES

Create:

`artifacts/full-transformation/FINAL_REPORT.md`

It must describe:
- What was actually implemented.
- What was tested.
- What works end-to-end.
- What is partially working.
- What remains unavailable.
- Which AI providers are configured.
- Which providers still need API keys.
- Which media capabilities require additional providers or credentials.
- Performance findings.
- Security findings.
- Accessibility findings.
- Known limitations.
- Exact startup instructions.
- Exact environment variables to configure.
- How to add provider credentials safely.
- How to run tests.
- How to resume development.

Also create:

`artifacts/full-transformation/FINAL_ACCEPTANCE.json`

Use machine-readable fields for:
- mission_status
- completed_phases
- failed_phases
- critical_blockers
- tests_passed
- tests_failed
- providers_configured
- providers_unconfigured
- working_features
- partial_features
- blocked_features
- final_status

Do not fabricate counts.

---

# 16. SUCCESS GATE — DO NOT SHUT DOWN PREMATURELY

The mission is considered successfully complete only if:

1. The existing project was inspected.
2. All planned phases were either completed or explicitly reported with justified blockers.
3. The application builds successfully.
4. The backend starts successfully.
5. Database migrations are valid.
6. Critical end-to-end user journeys pass.
7. No known unresolved P0 blocker remains.
8. No existing user data was destroyed.
9. AI integrations are accurately classified by real provider availability.
10. The AI documentation matches the actual implementation.
11. The execution state and final report are complete.
12. `FINAL_ACCEPTANCE.json` reports `final_status: SUCCESS`.
13. A final success marker is written only after all the above conditions are verified.

Only then create:

`D:\AQVERA\artifacts\full-transformation\MISSION_SUCCESS.txt`

Its entire content must be exactly:

`AQVERA_FULL_TRANSFORMATION_SUCCESS`

If any critical condition is not satisfied:
- Do not create the success marker.
- Set final status to BLOCKED or PARTIAL.
- Explain the remaining work.
- Leave the computer running.

Do not downgrade acceptance criteria merely to trigger shutdown.

---

# 17. FINAL WORKING PRINCIPLE

Work autonomously within the authorized project scope.

Prioritize real, testable functionality over the number of files or features.

Do not stop after producing a plan.

Do not stop after producing documentation.

Do not stop after building attractive interfaces.

Continue implementation, verification, and repair until the success gate is met or a genuine blocker prevents further progress.

Never conceal incomplete work.

The final result must be a coherent, working AQVERA application, with an independently organized AI subsystem and an honest record of everything that remains incomplete.