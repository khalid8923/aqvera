# PRODUCT_VISION.md

# AQVERA — Product Vision

## Vision Statement

AQVERA is an AI-powered academic learning platform that owns the complete student learning experience. It is not a chatbot wrapper. AI models provide capabilities, academic materials provide evidence, teaching methodology provides instructional consistency, and an adaptive engine determines the next useful learning step. No single AI model controls the entire academic experience.

## Target Users

- **Students** — guided, adaptive academic learning with clear progress visibility.
- **Independent learners / self-study students** — structured courses with assessment and feedback.
- **Instructors / content creators** (future) — course creation, review, and editing tools.

## Core Value Propositions

1. **Instructional consistency** — a versioned teaching methodology applies the same quality standard across all domains.
2. **Domain-specific adaptation** — the adaptive engine personalizes what to learn next based on demonstrated mastery, not fixed learning-style labels.
3. **Evidence-based mastery** — mastery is estimated from structured assessment evidence, not from a single correct answer.
4. **Provider independence** — AI models are interchangeable capabilities behind an abstraction layer; the platform never depends on one vendor.
5. **Explainable recommendations** — every adaptive recommendation states why it was selected and what evidence supports it.
6. **Private operation** — suitable for self-hosted, private use without sending all student data to a single AI vendor.

## Guiding Principles

| Principle | Description |
|-----------|-------------|
| Platform owns the experience | AI provides capabilities; the platform orchestrates instruction, assessment, and adaptation. |
| Teaching methodology is versioned | A single standard is applied across all domains; domain profiles add instructional behavior. |
| No fixed learning styles | Preferences and interaction patterns are observed over time, not assumed. |
| Evidence is traceable | Learning evidence is immutable; corrections are new records; calculations are reproducible. |
| AI never assigns mastery silently | AI may generate content and interpret errors, but mastery scores come from the adaptive engine. |
| Clarity over visual complexity | The interface prioritizes academic clarity, not decorative UI. |
| Modular monolith | Clear module boundaries; future extraction into services is possible but not required. |

## Out of Scope (Initial Release)

- Multi-tenancy / organization support.
- Mobile native applications (desktop + mobile browser layouts only).
- Public SaaS launch.
- Microservices or Kubernetes deployment.
- Every possible visualization tool (only the most valuable initial capability).

## Success Metrics (MVP)

- Student can complete: upload material → course generated → lesson → assessment → adaptive recommendation.
- Learner model updates after each assessment attempt.
- Adaptive recommendations include rationale and evidence confidence.
- At least one AI provider swap possible without rewriting teaching logic.
- All AI outputs validated against structured contracts.
