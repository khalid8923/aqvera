# ACCESSIBILITY_STANDARD.md

# AQVERA — Accessibility Standard

Status: DECIDED — WCAG 2.2 AA target.

## Conformance target
WCAG 2.2 Level AA is the product accessibility target for all AQVERA interfaces. Automated checks (axe-core) are a gate, not a substitute for manual keyboard and screen-reader review.

## Text and non-text contrast
- Text contrast: normal text ≥ 4.5:1; large text (≥ 18pt bold or 24pt) ≥ 3:1 against background.
- UI components and graphical objects: ≥ 3:1 against adjacent colors.
- Do not use color as the only method of communicating state, action, or response. Always pair color with text, icon, pattern, or border.

## Semantic HTML
- Use native HTML elements: `<button>`, `<a>`, `<input>`, `<label>`, `<fieldset>`, `<legend>`, `<dialog>`, `<table>`, `<h1>`–`<h6>`, `<ul>`, `<ol>`, `<li>`.
- Heading hierarchy is logical and not skipped.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` with `aria-label` where multiple of the same type exist.
- `<html>` declares `lang` and `dir`.

## Keyboard accessibility
- All functionality operable from a keyboard.
- Visible focus indicator on every interactive element (≥ 2 CSS px perimeter, 3:1 contrast).
- Tab order follows visual order; no keyboard traps.
- Custom widgets (dialogs, menus) manage focus and keyboard interactions per ARIA authoring practices.

## Focus order and visibility
- Focus moves logically when modal dialogs open (focus trapped inside) and closes (focus returns to trigger).
- Skip to main content available on pages with repeated navigation.
- No hidden focusable elements unless intentionally inert.

## Form labels and validation
- Every form field has a visible `<label>` programmatically associated (`for`/`id` or `aria-labelledby`).
- Required fields marked `aria-required="true"` and visually (`*`).
- `aria-invalid="true"` on invalid fields; error text associated via `aria-describedby`.
- Error summary at top of form on failed submit; focus moved to error summary heading; each error links to its field.
- Inline errors retained alongside summary.

## Dialog accessibility
- Dialogs use `role="dialog"` and `aria-modal="true"` (or native `<dialog>`).
- Focus trapped within dialog while open.
- Escape closes dialog.
- Focus returns to triggering element on close.
- Dialog title identified via `aria-labelledby`.

## Screen reader names
- Every interactive element has an accessible name (visible label or `aria-label`/`aria-labelledby`).
- Icon-only buttons have `aria-label`.
- Images convey meaning via `alt`; decorative images use `alt=""` and `aria-hidden="true"`.
- `aria-live` regions for dynamic updates (toasts, status) without interrupting.

## Responsive zoom and text reflow
- Content reflows at 400% zoom (equivalent to 1280px viewport at 320px CSS width) without loss of content/functionality and without two-dimensional scrolling (except where essential).
- Text can resize up to 200% without assistive technology, without loss of content/functionality.

## Touch target requirements
- Interactive targets ≥ 24×24 CSS px (WCAG 2.2 AA target size).
- Sufficient spacing between targets.

## Reduced motion
- Respect `prefers-reduced-motion: reduce`; disable or simplify non-essential animation.
- Motion used only to convey state change or relationship; no decorative animation.

## Error identification and recovery
- Errors identified in text, described, and suggested corrections offered where possible.
- Destructive actions require confirmation and are reversible or clearly irreversible.

## Manual checks (required, not optional)
- Keyboard-only operation of every page and workflow.
- Focus order and visibility.
- Dialog open/close and focus restoration.
- Form error announcements (screen reader).
- Color contrast review (automated + visual).
- RTL behavior (Arabic) where available — ensure `dir` and mirroring do not break keyboard/screen-reader operation.
