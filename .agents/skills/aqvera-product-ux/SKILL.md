---
name: aqvera-product-ux
description: "AQVERA product-specific UX engineering skill for the Adaptive Academic Learning Platform. Governs AQVERA UI/UX decisions: new pages and screen redesigns, navigation and information architecture, user flows, design systems and design tokens, forms/dialogs/interaction patterns, responsive layouts, Arabic/English presentation, accessibility, UX audits, and frontend visual testing. Directs agents to read AQVERA product and architecture documentation before proposing major UX changes, and enforces a repeatable workflow distinguishing UX design recommendations, approved product decisions, implemented functionality, planned functionality, and tested behavior."
---

# aqvera-product-ux

AQVERA Product UX Engineering Skill.

## Product Identity

AQVERA is an **Adaptive Academic Learning Platform for university students**. Its job is to transform students' academic materials into organized learning experiences that adapt to evidence of the student's understanding over time.

AQVERA is NOT a generic AI chatbot dashboard. The platform owns the learning experience. AI models are supporting capabilities, not the entire product.

## Preserved Product Principles

1. AQVERA owns the learning experience. AI models are supporting capabilities, not the entire product.
2. Teaching methodology is a stable product standard, not something that must be invented separately for each student.
3. Adaptive learning responds to demonstrated student performance and learning needs.
4. Academic materials are important sources of truth.
5. Students must understand what the system is doing and retain appropriate control.
6. Unimplemented functionality must never appear operational.
7. Never fabricate progress, mastery percentages, lesson completion, AI analysis, upload processing, or generated content.
8. Privacy, clarity, and trust are essential to the student experience.

## Mandatory Workflow

Every relevant task (UI/UX, pages, screens, navigation, IA, user flows, design systems, tokens, forms, dialogs, interactions, responsive layouts, RTL, accessibility, audits, visual testing) must follow this sequence:

1. **Understand the user objective.**
2. **Inspect the existing implementation.**
3. **Identify the affected user journey.**
4. **Review the information architecture.**
5. **Define the expected interaction and UI states.**
6. **Consult UI/UX Pro Max for relevant design intelligence.**
7. **Follow AQVERA's approved design system.**
8. **Implement the interface.**
9. **Test the functional behavior.**
10. **Perform visual, responsive, and accessibility QA.**
11. **Report actual evidence and unresolved issues.**

## Category Distinctions

Explicitly distinguish between:

- **UX design recommendations** — suggested guidance from UI/UX Pro Max or analysis; not binding until approved.
- **Approved product decisions** — decisions recorded in AGENTS.md, DECISION_LOG.md, or docs/ux; binding.
- **Implemented functionality** — code that exists in the frontend/backend and is verified working.
- **Planned functionality** — documented in PRODUCT_REQUIREMENTS.md, MVP_SCOPE.md, or docs/ux; not yet built.
- **Tested behavior** — behavior verified by running tests or manual QA with captured evidence.

Do not treat these categories as interchangeable. Never present planned or recommended functionality as implemented or tested.

## Documentation Precedence

Before proposing major UX changes, read the actual AQVERA product and architecture documentation:

- `D:\AQVERA\docs\product\PRODUCT_VISION.md`
- `D:\AQVERA\docs\product\PRODUCT_REQUIREMENTS.md`
- `D:\AQVERA\docs\product\MVP_SCOPE.md`
- `D:\AQVERA\docs\product\USER_JOURNEYS.md`
- `D:\AQVERA\docs\architecture\SYSTEM_ARCHITECTURE.md`
- `D:\AQVERA\docs\ux\` (product experience principles, information architecture, user journeys, interaction flows, content & localization, accessibility standard, responsive behavior, UI state matrix, UX acceptance criteria)
- `D:\AQVERA\design-system\aqvera\MASTER.md` and page-specific files
- Root `D:\AQVERA\AGENTS.md`

## UI/UX Pro Max Consultation

Where relevant, invoke `ui-ux-pro-max` for design intelligence (color palettes, typography, UX guidance, accessibility guidance, stack-specific recommendations for Next.js/React/Tailwind) before finalizing visual decisions.

## Triggers

This skill should be used when a task involves any of the following:

- AQVERA UI/UX
- New pages or screen redesigns
- Navigation and information architecture
- User flows
- Design systems and design tokens
- Forms, dialogs, and interaction patterns
- Responsive layouts
- Arabic/English presentation (RTL)
- Accessibility
- UX audits and frontend visual testing

## Current Implementation Status (reference)

Frontend: Next.js 16.4.6, React 19.3.0, TypeScript, Tailwind CSS 4.3.3, Playwright 1.65.1.
Routes: landing (`/`), dashboard (`/dashboard`), course library (`/courses`), course workspace (`/courses/[id]`), learning (`/learning`), resources (`/resources`), settings (`/settings`).
Components: `Shell.tsx`, `Navigation.tsx`, `AQVERALogo.tsx`.
Brand colors: ink `#101D2B`, navy `#192C3A`, paper `#F6F5F0`, sage `#C7E8DC`, sage-dark `#315C50`, terracotta `#D49B72`, muted `#77828A`, border `#E7E8E3`, surface `#EFEEE8`.
Fonts: Inter (sans), Crimson Text (editorial serif).
