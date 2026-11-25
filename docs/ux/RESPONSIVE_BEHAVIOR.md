# RESPONSIVE_BEHAVIOR.md

# AQVERA — Responsive Behavior

Status: DECIDED (breakpoints and intent), PROPOSED (page-specific adaptations to be validated).

## Breakpoints

| Breakpoint | Width | Device class | Tailwind prefix |
|------------|-------|--------------|-----------------|
| Mobile | 360–390px | Mobile portrait | default / `sm:` (≥640px) |
| Tablet | 768px | Tablet portrait | `md:` (≥768px) |
| Laptop / tablet landscape | 1024px | Laptop, tablet landscape | `lg:` (≥1024px) |
| Desktop | 1280px | Desktop | `xl:` (≥1280px) |
| Wide desktop | 1440px | Wide desktop | not a custom breakpoint; layout caps at container |

Container max-width: 1200px (`container`), with prose 65ch and editorial 720px variants.

## Design approach
- Mobile-first: default styles target narrowest screens; enhance with `md:`, `lg:`, `xl:`.
- Never simply shrink desktop layouts to fit mobile. Re-architect for touch, narrow viewports, and single-column flow.
- Avoid horizontal scrolling on mobile.

## Navigation

| Width | Behavior |
|-------|----------|
| 360–390px | Mobile top bar with logo and hamburger menu; sidebar hidden; drawer/overlay navigation on tap. |
| 768px | Sidebar collapsible or hidden behind hamburger; top bar remains. |
| 1024px+ | Persistent sidebar navigation (w-64) with top bar; full nav items visible. |

## Course lists

| Width | Behavior |
|-------|----------|
| 360–390px | Single-column stacked course cards; full-width table on courses page or stacked cards. |
| 768px | 2-column grid of course cards. |
| 1024px+ | 3-column grid of course cards; or full-width table with actions. |

## Dialogs and forms

| Width | Behavior |
|-------|----------|
| 360–390px | Dialog full-width or near-full-width, bottom-anchored or centered with padding; stacked form fields. |
| 768px | Centered dialog, max-w-md; 2-column grid for paired fields where appropriate. |
| 1024px+ | Centered dialog, max-w-md; 2-column grid for paired fields. |

## Workspace layouts

| Width | Behavior |
|-------|----------|
| 360–390px | Single column; course metadata stacked; sections (materials, activities, progress) stacked full-width. |
| 768px | Single column with generous padding; 2-column for metadata grid. |
| 1024px+ | Metadata grid (4 columns); sections side-by-side where beneficial; max-w-5xl. |

## Specific component adaptations

- **Course card:** full width on mobile; fixed aspect image/avatar area; actions stacked vertically on mobile, horizontal on desktop.
- **Table (courses):** horizontal scroll wrapper on mobile; full table on desktop.
- **Buttons:** full-width primary buttons on mobile; inline on desktop.
- **Typography:** scales down on mobile (e.g., `text-4xl md:text-6xl`).

## What to avoid
- Desktop-first media queries (`max-width`).
- Hover-dependent interactions on mobile (no critical action hidden behind hover).
- Fixed pixel widths that overflow narrow screens.
- Two-column form layouts that cramp inputs on mobile.
