# UX_ACCEPTANCE_CRITERIA.md

# AQVERA — UX Acceptance Criteria

Status: DECIDED.

A screen or workflow is not considered complete until all applicable criteria pass. "Passed" means verified by test or manual QA with captured evidence, not merely documented.

## 1. Functionality
- [ ] Every user action produces the correct system response.
- [ ] API integration behaves correctly (success, error, loading).
- [ ] Form submission validates, submits, and confirms.
- [ ] Destructive actions require confirmation.
- [ ] Navigation between pages and sections works.
- [ ] Unimplemented functionality never appears operational (no fake buttons, no fake data).

## 2. Visual consistency
- [ ] Colors come from the approved design system tokens only (no arbitrary hex values).
- [ ] Typography uses Inter (sans) and Crimson Text (editorial) only; no new pairings.
- [ ] Spacing uses the approved spacing scale; no arbitrary padding/margin.
- [ ] Radii, borders, elevation follow the design system.
- [ ] Component variants (buttons, inputs, cards, badges) match the design system.
- [ ] No page-specific colors introduced without design-system documentation and approval.

## 3. Responsive behavior
- [ ] Layout verified at 390px mobile, 768px tablet, 1024px laptop, 1280px desktop, 1440px wide desktop.
- [ ] Mobile-first: no desktop-only layouts shrunk to fit mobile.
- [ ] Navigation adapts (hamburger/drawer on mobile; sidebar on desktop).
- [ ] No horizontal overflow on any breakpoint.
- [ ] Touch targets ≥ 24×24 CSS px.

## 4. Accessibility (WCAG 2.2 AA)
- [ ] Text contrast ≥ 4.5:1 normal, ≥ 3:1 large; UI components ≥ 3:1.
- [ ] Color never the only means of conveying state.
- [ ] Semantic HTML used; heading hierarchy logical.
- [ ] All interactive elements keyboard-operable with visible focus.
- [ ] Focus order logical; no keyboard traps.
- [ ] Every form field has a programmatically associated label.
- [ ] Errors identified in text + inline + error summary; `aria-invalid`, `aria-describedby`.
- [ ] Dialogs: role, aria-modal, focus trap, escape closes, focus returns.
- [ ] Screen reader names on all interactive elements; alt text on meaningful images.
- [ ] Content reflows at 400% zoom without loss.
- [ ] `prefers-reduced-motion` respected.
- [ ] Manual keyboard + screen-reader review completed (automated axe checks insufficient alone).

## 5. Interaction clarity
- [ ] Button labels are specific ("Create course", "Save changes", "Archive course").
- [ ] Instructions short and actionable.
- [ ] Empty states show helpful message + primary action.
- [ ] Loading states show specific message, not generic spinner only.
- [ ] Success states confirm what happened.
- [ ] One primary action per screen where possible.

## 6. Content quality
- [ ] Academically appropriate language; consistent terminology.
- [ ] No placeholder/Lorem Ipsum text.
- [ ] No fabricated progress, mastery, completion, or AI claims.
- [ ] Arabic/English localization rules followed where applicable (dir, alignment, mirroring).

## 7. Loading and error behavior
- [ ] Every async action has a loading state.
- [ ] Every error has a text message and recovery path.
- [ ] Network failure handled with retry/offline indication.
- [ ] Unauthorized access redirects to sign-in.

## 8. No fabricated information
- [ ] No fake mastery percentages, completion, lesson completion, AI analysis, upload processing, or generated content.
- [ ] Unimplemented features marked honestly ("coming in Phase 2") or hidden.
- [ ] Progress bars reflect actual job status, not simulated.

## Evidence required
- Screenshot of each state at each breakpoint (stored under `D:\AQVERA\artifacts\ux-audit\`).
- Test results (Playwright) for functional journeys.
- axe-core accessibility results.
- Manual keyboard/screen-reader notes.
