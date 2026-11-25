# FOUNDATIONS.md

# AQVERA Design System — Foundations

Status: DECIDED

## Color

See MASTER.md for semantic color roles. AQVERA's brand palette: ink `#101D2B`, navy `#192C3A`, paper `#F6F5F0`, white `#FFFFFF`, sage `#C7E8DC`, sage-dark `#315C50`, terracotta `#D49B72`, muted `#77828A`, border `#E7E8E3`, surface `#EFEEE8`.

No new colors may be introduced without a documented design decision and update to MASTER.md.

## Typography

- Sans: Inter (`--font-inter`) — body, UI, labels, buttons.
- Editorial: Crimson Text (`--font-editorial`) — headings, display.
- Weights: Inter 400/500/600; Crimson Text 400/600.
- Loaded via `next/font/google` in `layout.tsx`.

## Spacing

See MASTER.md spacing scale (1–24). Use only tokens from this scale.

## Layout grid

- Container: 1200px.
- Prose: 65ch.
- Editorial: 720px.
- Mobile-first breakpoints: md ≥768px, lg ≥1024px, xl ≥1280px.

## Radii

- sm 0.375rem, md 0.5rem, lg 0.75rem.

## Borders

- border `#E7E8E3`; focus ring sage-dark `#315C50`.

## Elevation

- Border + surface color + subtle shadow; no heavy drop shadows.

## Icons

- SVG only; no emojis as icons. Directional icons mirrored for RTL; non-directional not mirrored.

## Motion

- Subtle transitions 150–300ms; stagger lists 300–450ms; respect `prefers-reduced-motion`.
