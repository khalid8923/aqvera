# MASTER.md

# AQVERA Design System — Master Source of Truth

Status: DECIDED

This file is the single source of truth for AQVERA's visual design. All page-specific files define only justified exceptions to this master system. No new design language, unrelated colors, new typography pairings, or arbitrary spacing may be introduced without documenting and approving the design decision.

## Design source
Generated with input from UI/UX Pro Max (Next.js/React/Tailwind stack), refined to preserve AQVERA's existing brand direction (ink, navy, paper, sage, terracotta). The generated teal palette was intentionally not adopted because it conflicts with AQVERA's established academic brand.

## Design personality
Academic, calm, trustworthy, clear. Minimalism & Swiss Style influence: spacious, functional, high contrast, geometric, grid-based, essential. Variance 3/10 (centered/minimal), Motion 4/10 (standard), Density 4/10 (standard).

## Semantic color roles

All colors defined as CSS variables and Tailwind tokens. These are the only colors permitted in AQVERA UI.

| Role | Token | Value | Usage |
|------|-------|-------|-------|
| ink (primary foreground) | `--color-ink` / `ink` | `#101D2B` | Headings, body text, primary buttons |
| navy | `--color-navy` / `navy` | `#192C3A` | Hover states, secondary emphasis |
| paper (background) | `--color-paper` / `paper` | `#F6F5F0` | Page background |
| white | `--color-white` / `white` | `#FFFFFF` | Cards, surfaces, dialogs |
| sage | `--color-sage` / `sage` | `#C7E8DC` | Light accent, active state backgrounds |
| sage-dark | `--color-sage-dark` / `sage-dark` | `#315C50` | Focus rings, active borders |
| terracotta | `--color-terracotta` / `terracotta` | `#D49B72` | Destructive/warm accent, section markers |
| muted | `--color-muted` / `muted` | `#77828A` | Helper text, secondary labels |
| border | `--color-border` / `border` | `#E7E8E3` | Borders, dividers |
| surface | `--color-surface` / `surface` | `#EFEEE8` | Elevated surfaces, hovered rows |

### Semantic role mapping (do not add new roles without approval)

| Semantic role | Maps to | Notes |
|---------------|---------|-------|
| foreground / body text | ink | |
| background / page | paper | |
| card / surface base | white | |
| border | border | |
| focus ring | sage-dark | |
| primary action | ink | bg-ink text-white |
| primary action hover | navy | |
| active / success accent | sage / sage-dark | |
| destructive | terracotta | Never color-only; pair with text |
| muted / helper | muted | |

## Typography

| Role | Font | Variable | Fallback | Usage |
|------|------|----------|----------|-------|
| Sans (body/UI) | Inter | `--font-inter` | ui-sans-serif, system-ui, sans-serif | Body, UI, labels, buttons |
| Editorial (headings) | Crimson Text | `--font-editorial` | ui-serif, Georgia, serif | Headings, display text |

- Weights: Inter 400/500/600; Crimson Text 400/600.
- No new font pairings may be introduced without approval.
- Fonts loaded via `next/font/google` (self-hosted, zero layout shift) in `layout.tsx`.

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| 1 | 0.25rem | tight gaps |
| 2 | 0.5rem | compact gaps |
| 3 | 0.75rem | standard small gaps |
| 4 | 1rem | standard section padding |
| 5 | 1.25rem | |
| 6 | 1.5rem | |
| 8 | 2rem | section padding |
| 10 | 2.5rem | |
| 12 | 3rem | |
| 16 | 4rem | large section padding |
| 20 | 5rem | |
| 24 | 6rem | |

No arbitrary spacing values outside this scale without approval.

## Layout grid

- Max-width container: `container` = 1200px.
- Prose max-width: `prose` = 65ch.
- Editorial max-width: `editorial` = 720px.
- Page content centered with `max-w-6xl` / `max-w-5xl` / `max-w-3xl` per page type.
- Mobile-first: default styles for narrow screens; enhance with `md:` (≥768px), `lg:` (≥1024px), `xl:` (≥1280px).

## Radii

| Token | Value | Usage |
|-------|-------|-------|
| sm | 0.375rem | small elements, badges |
| md | 0.5rem | buttons, inputs, cards |
| lg | 0.75rem | modals, large cards |

## Borders

| Role | Value | Usage |
|------|-------|-------|
| border | `#E7E8E3` | default borders, dividers |
| focus ring | `#315C50` (sage-dark) | 2px ring on focus |
| active border | sage-dark / sage | selected states |

## Elevation

- Cards: `border border-border` + subtle shadow on hover (`hover:border-sage-dark/50`).
- Dialogs: `shadow-xl` + `border border-border`.
- No heavy drop shadows; elevation via border + surface color + subtle shadow.

## Icons

- SVG only. No emojis as icons.
- Brand mark: AQVERA geometric symbol (A peak + open book + ascending chevron).
- Directional icons (chevrons, arrows) mirrored for Arabic RTL.
- Non-directional icons (charts, math, logos, play) NOT mirrored.
- All icon buttons have `aria-label`.

## Motion

- Subtle hover transitions 150–300ms.
- Stagger list (standard): 300–450ms, easing back.out(1.4), only on load/scroll.
- Respect `prefers-reduced-motion: reduce` — skip non-essential motion, render final state immediately.
- No decorative animation; motion conveys state change or relationship only.

## Responsive behavior

| Breakpoint | Width | Behavior |
|------------|-------|----------|
| Mobile | 360–390px | Single column, hamburger/drawer nav, stacked cards, full-width dialogs |
| Tablet | 768px | `md:` — 2-column grids, collapsible sidebar |
| Laptop | 1024px | `lg:` — persistent sidebar, 3-column grids |
| Desktop | 1280px | `xl:` — full layout, max-w-5xl/6xl |
| Wide | 1440px | Layout caps at 1200px container |

## Component variants

- Buttons: primary (bg-ink text-white, hover bg-navy), secondary (border border-border text-ink, hover bg-surface), destructive (text-terracotta).
- Inputs: `border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none`.
- Cards: `bg-white border border-border rounded-xl p-6`.
- Badges: inline-flex, rounded, px-2 py-1, text-xs font-medium (active: bg-sage/10 text-sage-dark border border-sage/20; archived: bg-terracotta/10 text-terracotta border border-terracotta/20).
- Dialogs: fixed centered, bg-white rounded-xl p-8, shadow-xl, border border-border, role="dialog" aria-modal.

## Interaction states

- Default, hover, focus (visible ring), active, disabled, loading, error, success.
- Focus ring: `focus:ring-2 focus:ring-sage-dark focus:outline-none`.
- Disabled: opacity-reduced, not focusable, no hover.

## Page-specific exceptions

Page-specific files under `pages/` define only justified exceptions to this master. Each exception must be documented with a reason.
