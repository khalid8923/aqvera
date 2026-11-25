# pages/dashboard.md

# AQVERA Design System — Dashboard Page

Status: DECIDED

## Exceptions to MASTER.md

None. Follows master design system exactly.

## Page-specific notes

- Max-width `max-w-5xl mx-auto`.
- Page heading: Crimson Text `text-2xl font-semibold tracking-tight`.
- Course grid: `grid md:grid-cols-2 lg:grid-cols-3 gap-6`.
- Course card: `bg-white border border-border rounded-xl p-6 hover:border-sage-dark/50 transition-colors`.
- Empty state: master empty-state pattern + "Create your first course" primary button.
- Create course dialog: master dialog variant; master form fields.

## States

- Initial: skeleton / "Loading your courses…"
- Empty: "No courses yet" + create action
- Populated: course grid
- Loading: submit disabled + spinner
- Validation error: inline field error
- Success: "Course created" + updated list
- Server error: error banner
