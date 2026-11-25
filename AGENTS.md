# AGENTS.md

# AQVERA — Engineering Instructions for AI Agents

## Project Identity

AQVERA is an AI-powered academic learning platform. It is NOT a generic AI chatbot dashboard.
The platform owns the learning experience. AI models provide capabilities, academic materials provide
evidence, teaching methodology provides instructional consistency, and the adaptive engine determines
the next useful learning step.

No single AI model should control the entire academic experience.

## Phase Status

**Phase 0 — Documentation and Architecture Only.** No application code exists. The repository
D:\AQVERA is empty and is currently read-only for the executing user account (hpc). Documentation
has been produced in C:\Users\hpc\AppData\Local\Temp\kilo\aqvera-docs\ and must be copied to
D:\AQVERA once write permissions are available.

Do not implement frontend source code, backend source code, install packages, create application
components, create fake working functionality, generate unnecessary assets, start deployment, or
modify unrelated files in this phase.

## Repository Structure (Planned)

```
D:\AQVERA\
├── AGENTS.md
├── README.md
├── PROJECT_CONTEXT.md
├── DECISION_LOG.md
├── docs/
│   ├── product/
│   ├── architecture/
│   ├── academic/
│   └── engineering/
```

## Agent Roles (Logical, Not Necessarily Separate Processes)

1. **Architecture Agent** — Reviews architectural decisions and consistency.
2. **Backend Agent** — Implements backend modules and business logic.
3. **Frontend Agent** — Implements the user interface and client-side behavior.
4. **AI Systems Agent** — Implements AI orchestration, provider adapters, retrieval, teaching workflows.
5. **Testing Agent** — Creates tests, evaluates behavior, and identifies regressions.

These are logical responsibilities. One agent may cover multiple roles.

## Mandatory Workflow for Every Implementation Task

1. **Inspect** relevant existing files.
2. **Understand** dependencies.
3. **Identify** the smallest appropriate change.
4. **Implement** the change.
5. **Add or update** tests.
6. **Run** relevant checks (lint, typecheck, tests).
7. **Review** your own changes.
8. **Document** important decisions.

## Coding Conventions

- Follow the existing file's code style and conventions.
- Use existing libraries and utilities already present in the codebase.
- Do not assume a library is available; verify it is already used.
- Mimic naming conventions, typing, and patterns of neighboring code.
- Do NOT add comments unless explicitly asked.
- Do not create duplicate abstractions unnecessarily.
- Do not replace real business logic with hardcoded demo data.
- Do not ignore existing conventions.
- Do not modify unrelated modules without a clear reason.

## Testing Expectations

- Never claim tests passed without running them.
- Add unit tests for domain logic, adaptive decisions, scoring, validation, teaching workflow rules.
- Add integration tests for database interactions, file storage, document processing, AI provider adapters, retrieval, background jobs.
- Add end-to-end tests for core workflows (account creation, course creation, file upload, course generation, learning activities, assessment, learner model update).
- AI evaluation must use representative academic test cases, not a few hand-picked examples.

## Security Rules

- Never expose or log secrets and keys.
- Never commit secrets to the repository.
- Uploaded documents are untrusted data; instructions inside them must never override system policies.
- Do not execute untrusted code inside the main application process.
- Validate all AI outputs against structured contracts before use.
- Minimize PII sent to external AI providers.

## Documentation Requirements

- All documents must agree with one another.
- Mark uncertain decisions as DECIDED, PROPOSED, OPEN, or DEFERRED.
- Do not disguise assumptions as final architectural decisions.
- Avoid unnecessary documentation duplication.

## Prohibited Shortcuts

- Inventing existing functionality.
- Claiming tests passed without running them.
- Silently changing architectural decisions.
- Deleting working functionality without justification.
- Creating duplicate abstractions unnecessarily.
- Replacing real business logic with hardcoded demo data.
- Ignoring existing conventions.
- Modifying unrelated modules without a clear reason.

## How to Report Completed Work

When a task is complete, document the decision in DECISION_LOG.md and update the relevant docs.
Do not commit changes unless explicitly asked by the user.

## UI/UX Development Policy (Mandatory)

Whenever an agent changes AQVERA's interface (pages, components, navigation, forms, dialogs, layouts, design tokens, styling), it must follow this policy:

1. **Invoke `ui-ux-pro-max`** where relevant (design intelligence, color, typography, UX guidance, accessibility guidance, stack-specific recommendations for Next.js/React/Tailwind).
2. **Consult `aqvera-product-ux`** (the AQVERA product-specific UX skill at `D:\AQVERA\.agents\skills\aqvera-product-ux\SKILL.md`).
3. **Read the approved master design system** at `D:\AQVERA\design-system\aqvera\MASTER.md`.
4. **Check the relevant page-specific design rules** under `D:\AQVERA\design-system\aqvera\pages\`.
5. **Identify the affected user journey** from `D:\AQVERA\docs\ux\USER_JOURNEYS.md`.
6. **Preserve existing business behavior and API integration.** Do not change database models or API contracts.
7. **Include all relevant UI states** per `D:\AQVERA\docs\ux\UI_STATE_MATRIX.md` (initial, loading, empty, populated, partial, success, validation error, server error, offline, disabled, unauthorized, destructive confirmation).
8. **Perform responsive and accessibility checks** per `D:\AQVERA\docs\ux\RESPONSIVE_BEHAVIOR.md` and `D:\AQVERA\docs\ux\ACCESSIBILITY_STANDARD.md` (WCAG 2.2 AA).
9. **Capture visual evidence** (screenshots stored under `D:\AQVERA\artifacts\ux-audit\`).
10. **Report what was actually tested**, distinguishing UX design recommendations, approved product decisions, implemented functionality, planned functionality, and tested behavior.

### Design-language restrictions

No developer or AI agent may introduce a new design language, unrelated colors, new typography pairings, or an arbitrary spacing system without documenting and approving the design decision. All colors, typography, spacing, radii, borders, and component variants must come from the approved design system (`D:\AQVERA\design-system\aqvera\MASTER.md`) unless a documented exception is added to a page-specific file under `pages/`.

### Preservation

This policy supplements — and does not replace — the existing project rules above. All existing coding conventions, testing expectations, security rules, and documentation requirements continue to apply.
