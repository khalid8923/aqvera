# ACCESSIBILITY.md

# AQVERA Design System — Accessibility

Status: DECIDED — WCAG 2.2 AA target. See `D:\AQVERA\docs\ux\ACCESSIBILITY_STANDARD.md`.

## Contrast

- Normal text ≥ 4.5:1; large text ≥ 3:1.
- UI components/graphical objects ≥ 3:1.
- Color never the only means of conveying state.

## Semantics

- Native HTML: `<button>`, `<a>`, `<input>`, `<label>`, `<dialog>`.
- Heading hierarchy logical, no skipped levels.
- Landmarks with `aria-label` when repeated.

## Keyboard

- All functionality keyboard-operable.
- Visible focus indicator (≥2px, 3:1 contrast).
- Logical tab order, no traps.

## Forms

- Every field has a visible `<label>` programmatically associated.
- Required: `aria-required="true"` + `*`.
- Invalid: `aria-invalid="true"` + `aria-describedby` to error text.
- Error summary on failed submit; focus to summary; inline errors retained.

## Dialogs

- `role="dialog"` `aria-modal="true"` (or `<dialog>`).
- Focus trapped; escape closes; focus returns to trigger.

## Screen readers

- Accessible name on every interactive element.
- Icon-only buttons: `aria-label`.
- Meaningful images: `alt`; decorative: `alt=""` `aria-hidden="true"`.
- `aria-live` for dynamic updates.

## Zoom / reflow / touch

- Reflow at 400% zoom (320px CSS equivalent) without loss or 2D scrolling.
- Text resize to 200% without loss.
- Touch targets ≥ 24×24 CSS px.

## Motion

- Respect `prefers-reduced-motion: reduce`.

## RTL

- `dir="rtl"` / `lang="ar"` for Arabic; mirrored navigation and directional icons; LTR content (code, math, numbers) preserved.
