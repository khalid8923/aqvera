# COMPONENTS.md

# AQVERA Design System — Components

Status: DECIDED

## Button

Variants:
- Primary: `bg-ink text-white px-6 py-3 rounded-md text-sm font-medium hover:bg-navy transition-colors`
- Secondary: `border border-border text-ink px-6 py-3 rounded-md text-sm font-medium hover:bg-surface transition-colors`
- Destructive: `text-terracotta border border-border px-6 py-3 rounded-md text-sm font-medium hover:bg-terracotta/10 transition-colors`

States: default, hover, focus (ring-2 ring-sage-dark), active, disabled, loading.

All buttons: specific labels ("Create course", "Save changes", "Archive course", "Delete course"); no generic "Submit"/"OK".

## Input

`w-full px-3 py-2 border border-border rounded-md focus:ring-2 focus:ring-sage-dark focus:outline-none`

Required fields marked `*` and `aria-required="true"`. Invalid fields `aria-invalid="true"` with error text via `aria-describedby`.

## Label

`block text-sm font-medium mb-1` text-ink. Programmatically associated (`for`/`id` or `aria-labelledby`).

## Card

`bg-white border border-border rounded-xl p-6` with `hover:border-sage-dark/50 transition-colors`.

## Badge

`inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-medium`
- Active: `bg-sage/10 text-sage-dark border border-sage/20`
- Archived: `bg-terracotta/10 text-terracotta border border-terracotta/20`

## Dialog

Fixed centered, `bg-white rounded-xl p-8 w-full max-w-md shadow-xl border border-border`, `role="dialog" aria-modal="true"`. Focus trap, escape closes, focus returns on close. Close button (`✕`) with `aria-label`.

## Table

`w-full text-left border-collapse bg-white`; header `border-b border-border` text-xs font-medium text-muted; rows `divide-y divide-border` hover:bg-surface/50.

## Empty state

`bg-white border border-border rounded-xl p-16 text-center` with icon, heading, message, primary action.

## Navigation (sidebar)

`hidden md:flex flex-col w-64 border-r border-border bg-white`; nav items `flex items-center gap-3 px-4 py-3 rounded-md text-sm font-medium`; active `bg-surface text-ink`, inactive `text-muted hover:text-ink hover:bg-surface/50`.

No new component variants without a documented design decision.
