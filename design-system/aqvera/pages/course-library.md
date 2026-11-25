# pages/course-library.md

# AQVERA Design System — Course Library Page

Status: DECIDED

## Exceptions to MASTER.md

None. Follows master design system exactly.

## Page-specific notes

- Max-width `max-w-6xl mx-auto`.
- Page heading: Crimson Text `text-2xl font-semibold tracking-tight`.
- Course table: master table variant with `overflow-x-auto` wrapper on narrow screens.
- Status badges: master badge variant (active: sage; archived: terracotta).
- Action buttons (Open, Edit, Archive, Delete): secondary button variant at small size; Delete text-terracotta.
- Create course button: primary button variant.
- Dialogs: master create/edit dialog variant.

## States

- Initial: skeleton / "Loading courses…"
- Empty: "No courses yet" / "No archived courses" + create action
- Populated: course table
- Loading: spinner
- Validation error: inline field error
- Success: updated list + confirmation
- Server error: error banner
- Destructive confirmation: Delete dialog
