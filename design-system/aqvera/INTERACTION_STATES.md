# INTERACTION_STATES.md

# AQVERA Design System — Interaction States

Status: DECIDED

## Universal states

| State | Visual treatment |
|-------|------------------|
| Default | Normal token colors, fully opaque |
| Hover | Subtle background shift (hover:bg-surface / hover:bg-navy), 150–300ms transition |
| Focus | `focus:ring-2 focus:ring-sage-dark focus:outline-none`, ≥2px perimeter, 3:1 contrast |
| Active | Pressed appearance, slightly darker background |
| Disabled | Opacity reduced, `disabled` attribute, not focusable, no hover |
| Loading | Spinner/progress + specific message ("Loading courses…"); submit disabled |
| Error | `border-terracotta/20 text-terracotta` + inline text; never color alone |
| Success | Confirmation text ("Course created."), then return to default/populated |

## Focus ring

`--color-ring`: sage-dark `#315C50`. Applied to all interactive elements.

## Motion & reduced motion

- Transitions 150–300ms for hover/focus.
- Stagger lists 300–450ms with back.out(1.4).
- `prefers-reduced-motion: reduce` → skip non-essential motion, render final state immediately.

## No color-only state

Every state (error, success, active, disabled) is paired with text, icon, pattern, or border — never color alone.
