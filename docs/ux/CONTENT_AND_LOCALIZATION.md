# CONTENT_AND_LOCALIZATION.md

# AQVERA — Content Design and Localization

Status: DECIDED (content rules), PROPOSED (Arabic localization — to be validated with native review).

## Content Design Rules

### Language and tone
- Clear, academically appropriate language. Address the student directly ("you", "your course").
- Avoid marketing hyperbole and AI hype. No fabricated capability claims.
- Use consistent terminology across the product (see Terminology below).

### Instructions
- Short, actionable instructions. One primary action per screen where possible.
- Lead with the verb: "Create course", "Upload document", "Return to library".
- Avoid noun-only labels where a verb clarifies the action.

### Button labels
- Specific, not generic. Use "Create course" not "Submit"; "Save changes" not "Save"; "Archive course" not "Archive".
- Destructive actions use clear labels: "Delete course" with destructive confirmation.
- Never use "OK" or "Yes" alone for destructive actions.

### Form descriptions
- Helpful, concise field helper text beneath inputs.
- Mark required fields with `*` and explain what is required.
- Placeholder text shows format examples (e.g., "e.g. MATH101"), not instructions.

### Error messages
- Identify the error in plain language: "Course title is required."
- Tell the user how to fix it.
- Never communicate an error by color alone; pair with text.
- Associate errors with fields via `aria-describedby` and `aria-invalid`.

### Empty-state writing
- State what is missing: "No courses yet."
- Give a clear next action: "Create your first course."
- Never show blank empty screens.

### Loading and success messages
- Loading: "Loading courses…" (specific, not generic "Loading…").
- Success: confirm what happened: "Course created." — avoid toast-only with no field context.

## Terminology

| Term | Usage | Avoid |
|------|-------|-------|
| Course | An academic course with title, code, domain | Class, module (use module only for course sub-structure) |
| Module | Sub-division within a course | Unit, section (inconsistent) |
| Topic | Sub-division within a module | Chapter |
| Learning objective | Measurable goal | Goal, aim |
| Mastery | Estimated from evidence | Score, grade, level |
| Adaptive recommendation | System suggestion with rationale | AI suggestion, next step (without rationale) |
| Evidence | Assessment/data supporting mastery | Proof (too strong) |
| Archive | Soft removal | Delete (unless hard delete) |
| Delete | Hard removal | Remove (ambiguous) |
| Processing | Upload/job in progress | Working (vague) |

## Arabic and English localization

### Language direction
- AQVERA supports English (LTR) and Arabic (RTL).
- `dir="ltr"` for English; `dir="rtl"` for Arabic, set on `<html>` and inherited.
- `lang="en"` / `lang="ar"` on `<html>`.

### Text alignment
- English: left-aligned body text; headings may be center-aligned on landing/hero sections.
- Arabic: right-aligned body text; mirror alignment accordingly.
- Do not force center alignment to "fake" RTL.

### Mirrored navigation and icons
- Navigation order is mirrored: primary navigation starts on the right for RTL.
- Back/forward arrows, carousel controls, and progress indicators are mirrored for RTL.
- **Do not mirror:** icons with inherent directionality that must not flip (e.g., play ▶, charts, mathematical notation, LTR-only logos, text, numeric digits that remain LTR, Arabic numerals contextually).
- Icons that are purely directional (chevrons, arrows) are mirrored.

### Form layout
- Field labels align to the start (right in RTL, left in LTR).
- Input text direction follows the content language; mixed LTR/RTL content handled with `dir="auto"` where appropriate.
- Error messages appear beneath fields in the page direction.

### Bidirectional technical content
- Code, mathematical expressions, chemical formulas, and course codes remain LTR even within Arabic UI (`dir="ltr"` inline).
- Numbers and dates: use locale-appropriate formatting; Arabic locales may use Arabic-Indic digits contextually — do not assume; validate with native review.
- Mixed-direction paragraphs use the Unicode Bidirectional Algorithm; avoid manual reordering.

### Academic terminology consistency
- Translate academic terms consistently across EN/AR; maintain a glossary.
- "Course", "Module", "Topic", "Objective", "Mastery" have fixed Arabic equivalents.
- Never machine-translate assessment content or learning objectives without review.

## Content quality rules
- No placeholder text (Lorem Ipsum) in production UI.
- No fabricated progress, mastery, or completion claims in copy.
- All UI copy must map to a real, implemented, or clearly-labeled-planned capability.
