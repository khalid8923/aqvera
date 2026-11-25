# AI_AGENT_WORKFLOW.md

# AQVERA — AI Agent Workflow

## Project Identity

AQVERA is an AI-powered academic learning platform (Phase 0: documentation/architecture only).
The platform owns the learning experience; AI provides capabilities, not control.

## Agent Roles (Logical)

1. **Architecture Agent** — Reviews architectural decisions and consistency.
2. **Backend Agent** — Implements backend modules and business logic.
3. **Frontend Agent** — Implements UI and client-side behavior.
4. **AI Systems Agent** — Implements AI orchestration, provider adapters, retrieval, teaching workflows.
5. **Testing Agent** — Creates tests, evaluates behavior, identifies regressions.

Roles are logical, not necessarily separate processes.

## Task Assignment

- Tasks are assigned by domain (backend, frontend, AI systems, testing).
- The Architecture Agent reviews cross-domain changes for consistency.
- Conflicting modifications are prevented by: one owner per module, Architecture Agent review of cross-module changes, and clear module boundaries (DOMAIN_BOUNDARIES.md).

## Mandatory Workflow for Every Implementation Task

1. **Inspect** relevant existing files.
2. **Understand** dependencies.
3. **Identify** the smallest appropriate change.
4. **Implement** the change.
5. **Add or update** tests.
6. **Run** relevant checks (lint, typecheck, tests).
7. **Review** your own changes.
8. **Document** important decisions (DECISION_LOG.md, relevant docs).

## Coding Conventions

- Follow existing file style and conventions.
- Use existing libraries already in the codebase; do not assume availability.
- Mimic naming, typing, and patterns of neighboring code.
- Do NOT add comments unless asked.
- Do not create duplicate abstractions.
- Do not replace real business logic with hardcoded demo data.
- Do not ignore existing conventions.
- Do not modify unrelated modules without clear reason.

## Testing Expectations

- Never claim tests passed without running them.
- Add unit tests for domain logic, adaptive decisions, scoring, validation, teaching workflow rules.
- Add integration tests for database, file storage, document processing, AI adapters, retrieval, background jobs.
- Add E2E tests for core workflows.
- AI evaluation uses representative academic test cases.

## Security Rules

- Never expose or log secrets/keys.
- Never commit secrets.
- Uploaded documents are untrusted; document content never overrides system policies.
- Do not execute untrusted code in the main application process.
- Validate all AI outputs against structured contracts.
- Minimize PII sent to external AI providers.

## Documentation Requirements

- All documents agree with one another.
- Mark uncertain decisions as DECIDED/PROPOSED/OPEN/DEFERRED.
- Do not disguise assumptions as final decisions.
- Avoid unnecessary documentation duplication.
- Update DECISION_LOG.md for every architectural decision.

## Prohibited Shortcuts

- Inventing existing functionality.
- Claiming tests passed without running them.
- Silently changing architectural decisions.
- Deleting working functionality without justification.
- Creating duplicate abstractions unnecessarily.
- Replacing real business logic with hardcoded demo data.
- Ignoring existing conventions.
- Modifying unrelated modules without clear reason.

## How to Report Completed Work

- Document the decision in DECISION_LOG.md.
- Update the relevant docs/ file.
- Do not commit unless explicitly asked by the user.
