# DESIGN_DIRECTION_PROPOSALS.md

# AQVERA — Design Direction Proposals

Status: PROPOSED (not yet implemented).

## Basis: current actual interface

The current frontend (Next.js 16 / React 19 / Tailwind 4) implements:
- Landing page (`/`), dashboard (`/dashboard`), course library (`/courses`), course workspace (`/courses/[id]`), learning (`/learning`), resources (`/resources`), settings (`/settings`).
- Shell: `Shell.tsx` with `MobileTopBar`, persistent `Sidebar` (desktop), `TopNav`.
- Brand palette: ink `#101D2B`, navy `#192C3A`, paper `#F6F5F0`, white `#FFFFFF`, sage `#C7E8DC`, sage-dark `#315C50`, terracotta `#D49B72`, muted `#77828A`, border `#E7E8E3`, surface `#EFEEE8`.
- Fonts: Inter (sans), Crimson Text (editorial serif) via `next/font/google`.
- Course library uses a table; dashboard uses a card grid; course workspace uses metadata cards + placeholder sections.
- Modals built with inline `hidden` classes and direct DOM manipulation (`document.getElementById`), not a dialog component.
- No RTL support, no `dir` attribute handling, no focus-trap dialogs.

Evidence: axe-core audit found real color-contrast violations (muted `#77828A` ~3.9:1 on white; terracotta `#D49B72` 2.4:1 on white), below WCAG 2.2 AA 4.5:1 for normal text.

---

## Direction A — "Academic Swiss" (refinement of current brand)

### Visual personality
Calm, authoritative, scholarly. Editorial serif headings (Crimson Text) paired with neutral sans (Inter). Generous white space, rule-based grid, restrained accent use. Signals "established academic institution" rather than "tech startup."

### Layout philosophy
Centered, maximal 1200px container. Persistent left sidebar navigation on desktop; hamburger drawer on mobile. Single-column page bodies; course library as a table on desktop and stacked cards on mobile. Clear visual hierarchy via type scale and weight, not color.

### Typography direction
Keep Inter + Crimson Text. Crimson Text for H1/H2 and page titles; Inter for UI, labels, data. Modular scale rooted in body 16px. No new font pairings.

### Color application
Preserve the existing ink/navy/paper/sage/terracotta palette exactly. Use ink for primary text, paper for background, white for cards, sage for active/success, terracotta sparingly for destructive accents and section markers. **Do not adopt the UI/UX Pro Max-generated teal palette** — it conflicts with AQVERA's established brand.

### Navigation pattern
Persistent sidebar (desktop) + topbar; mobile drawer. Active state via background tint (surface) + ink text, not color alone.

### Course card/list presentation
Course library: table on desktop (rows with title/code/domain/semester/status/actions), stacked cards on mobile. Course cards: white, border, subtle hover border. Status badges: sage (active) / terracotta (archived).

### Dashboard composition
Hero-style intro (Crimson Text headline), "Your courses" card grid (2-col tablet, 3-col desktop), "Create course" primary button. Empty state: centered icon + message + primary action.

### Course workspace composition
Left metadata block (university/department/semester/language in surface cards), right content area with Materials / Learning activities / Progress sections (currently honest "Phase 2" placeholders). Breadcrumb: Course Library / Course title.

### Strengths
- Zero brand disruption; preserves existing visual equity.
- Meets academic product positioning; high trust/clarity.
- Easiest to implement incrementally from current code.
- Typography already in place via next/font.

### Weaknesses
- Current palette has documented WCAG contrast failures (muted 3.9:1, terracotta 2.4:1 on white) — must be fixed to reach AA.
- Risks feeling conservative / "not premium" without refinement.
- Table-based course library can feel dated on mobile.

### Risks
- Contrast remediation required before any claim of WCAG AA.
- Incremental refinement may not fix structural UI issues (inline DOM modals, no focus traps).

### Compatibility with academic product
High. Scholarly editorial voice aligns with university audience and "platform owns the learning experience" principle.

---

## Direction B — "Adaptive Canvas" (content-first, contextual)

### Visual personality
Light, adaptive, student-centered. Interface recedes so academic content (materials, lessons, assessments) takes priority. Accent color shifts subtly by subject domain (mathematics, humanities, CS) to give each course a distinct but related identity.

### Layout philosophy
Content-first canvas. Narrower read column for lessons (~65ch prose) for readability; full-width for course library. Navigation collapses to icons-only rail on desktop, bottom tab bar on mobile (app-like). Contextual toolbars appear only when relevant (progressive disclosure).

### Typography direction
Inter for body and UI; Crimson Text reserved for display/hero only. Lesson body uses Inter at comfortable measure with increased line height. Subject-specific accent used sparingly for headers within a course.

### Color application
Ink/navy base; paper background; white cards. Subject-domain accent hues derived from terracotta/sage family (e.g., mathematics = sage variant, humanities = terracotta variant), applied as thin left borders and chip backgrounds — never as sole state indicator.

### Navigation pattern
Icons-only rail (desktop), bottom tab bar (mobile). Active state via filled accent icon + label tooltip. Global search/command bar at top.

### Course card/list presentation
Cards with a thin subject-color left border, title + short description, "Open" primary action, compact metadata row. Table view optional for power users.

### Dashboard composition
Welcome + "continue where you left off" resume card (resume unfinished activity), course grid, quick actions. Strong empty state with onboarding guidance.

### Course workspace composition
Collapsible sidebar within course: Materials / Activities / Progress. Main canvas shows current lesson/assessment at readable measure. Resume entry point prominent.

### Strengths
- Content prioritized; fits "academic materials are sources of truth."
- Resume/unfinished-activity support maps to Journeys 8, 14.
- Subject differentiation aids course switching.

### Weaknesses
- Icons-only rail reduces discoverability for labels (accessibility risk; needs tooltips/aria-labels).
- Bottom tab bar on mobile diverges from current sidebar/drawer pattern — more change.
- Subject accent hues risk color-coded meaning that must be reinforced with text.

### Risks
- Greater departure from current code = more implementation effort.
- "Adaptive" visual theming could be mistaken for adaptive learning (confusing product claim).

### Compatibility with academic product
High for reading/learning sessions; medium risk of over-styling that distracts from academic clarity.

---

## Direction C — "Institutional Dashboard" (dense, data-rich, administrative)

### Visual personality
Efficient, systematic, data-forward. Dense information architecture, strong grid, badge/status heavy. Signals "student information system" — useful for students managing many courses.

### Layout philosophy
Dense dashboard: sidebar navigation + top global bar + multi-column dashboard with widgets (course list, upcoming assessments, retention reviews, mastery quick-view). Data tables preferred over cards for scanability.

### Typography direction
Inter throughout (headings and body) for maximum legibility at small sizes; Crimson Text reserved for landing-page marketing only. Small text (12–14px) for data rows.

### Color application
Ink base; statuses color-coded (active=sage, archived=terracotta, due=amber variant). Heavy use of badge chips and status pills. Color paired with text labels (never color alone).

### Navigation pattern
Persistent sidebar with grouped sections (Courses, Learning, Resources, Settings); topbar with global search, notifications, user profile.

### Course card/list presentation
Data table with sortable columns, bulk actions, status chips, "Open/Edit/Archive/Delete" action row. Card view as secondary.

### Dashboard composition
Widget grid: "Your courses" table, "Due soon" retention reviews, "Mastery overview" sparkline (future), quick-create button.

### Course workspace composition
Tabbed sections within course (Details, Materials, Activities, Progress). Dense metadata table. Action toolbar at top.

### Strengths
- Scales to many courses and rich data (future phases).
- Familiar SIS/LMS pattern students may recognize.
- Clear status communication via badges + text.

### Weaknesses
- Density conflicts with "clarity over visual complexity" and cognitive-load principles.
- Heavy badging risks color-dependent meaning; accessibility burden.
- Less appropriate for a focused, single-course learning session.

### Risks
- May feel like a generic LMS, undermining "NOT a generic LMS" positioning.
- Contrast and color-dependence must be carefully managed for WCAG AA.

### Compatibility with academic product
Medium. Fits administration but less aligned with focused learning experience and cognitive-load principles.

---

## Recommendation: Direction A — "Academic Swiss"

### Why Direction A
1. **Brand continuity**: Preserves AQVERA's existing ink/navy/paper/sage/terracotta brand and Inter/Crimson Text typography already in production. No brand disruption, no wasted visual equity.
2. **Academic positioning**: Editorial serif + restrained grid best communicates "established academic platform," aligning with "platform owns the learning experience" and "clarity over visual complexity."
3. **Lowest risk**: Incremental refinement of existing code rather than wholesale restructuring (sidebar, shell, routes already exist).
4. **Contrast defects are fixable within the palette**: The axe-core failures (muted, terracotta on white) are contrast-ratio issues, not palette issues. They can be resolved by darkening `muted` and `terracotta` text or adjusting backgrounds — keeping hue, raising contrast to 4.5:1. This stays within Direction A.
5. **Product-principle alignment**: Minimal decoration, honest states, text-paired semantics support trust, transparency, and no fabricated progress.

### Required before any redesign (from this foundation)
- Fix color-contrast violations (muted `#77828A`, terracotta `#D49B72` on white/paper) to ≥4.5:1.
- Replace inline DOM modals with accessible dialogs (role, aria-modal, focus trap, escape, focus return).
- Add `dir`/`lang` handling for Arabic/English RTL readiness.
- No new colors, fonts, or spacing outside the design system.

Directions B and C remain available as future options if product requirements evolve toward dense data management or subject-themed canvases, but they involve greater change and risk for Phase 1.

Do not modify the actual frontend styling during this foundation phase. The UX architecture and recommended direction are ready for review before the complete visual redesign begins.
