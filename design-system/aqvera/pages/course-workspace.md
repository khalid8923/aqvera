# pages/course-workspace.md

# AQVERA Design System — Course Workspace Page

Status: DECIDED (layout), PROPOSED (future content sections)

## Exceptions to MASTER.md

None for the implemented shell. Future sections (materials, activities, progress) follow master patterns when built.

## Page-specific notes

- Max-width `max-w-5xl mx-auto p-6`, `min-h-screen bg-paper`.
- Breadcrumb navigation: text-xs text-muted.
- Course title: Crimson Text `text-2xl font-semibold`.
- Metadata grid: `grid md:grid-cols-4 gap-4` text-sm cards (`bg-surface border border-border rounded-xl p-4`).
- Future sections (materials, learning activities, progress): honest "coming in Phase 2" placeholder (not fake functionality).
- No new colors, fonts, or spacing beyond MASTER.md.

## States

- Initial: skeleton / "Loading course…"
- Error/Not found: "Course not found" + return link
- Populated: course details + sections
- Partial (future): honest placeholder, never fake data
