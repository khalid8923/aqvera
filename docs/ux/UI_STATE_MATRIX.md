# UI_STATE_MATRIX.md

# AQVERA — UI State Matrix

Status: DECIDED.

A page is not complete merely because its populated state looks good. Every major reusable interface pattern must handle all applicable states below.

## States

| State | Meaning | When it occurs | Required UI |
|-------|---------|----------------|-------------|
| Initial | First render, no data yet | Page load before data fetch | Skeleton or neutral placeholder, no fake data |
| Loading | Data/action in progress | Fetching courses, submitting form, processing upload | Spinner/progress, specific message ("Loading courses…"), disable submit |
| Empty | No data to show | No courses, no materials, no learning data | Helpful message + primary action ("Create your first course") |
| Populated | Normal data present | Courses loaded, content available | Full UI with data |
| Partial data | Some data, some missing | One course loaded but materials pending | Show available data, mark missing sections honestly |
| Success | Action completed | Course created/edited/deleted, form submitted | Confirmation message, then return to populated state |
| Validation error | Input invalid | Empty title, bad email, invalid file | Inline field error + error summary, focus to error |
| Server error | API failed | 5xx, network down | Error banner, specific message, retry action |
| Offline/network failure | No network | Fetch fails with network error | Offline indicator, retry when online |
| Disabled | Control not operable | Form invalid, action not allowed | `disabled`, greyed, not focusable |
| Unauthorized | No session | Accessing authenticated page without auth | Redirect to sign-in, message |
| Destructive confirmation | Irreversible action | Delete course | Confirmation dialog, clear label, cancel option |

## Pattern coverage

Each pattern must specify which states apply and what the UI shows:

### Course list
- Initial: skeleton
- Loading: spinner
- Empty: "No courses yet" + create action
- Populated: course table/cards
- Success: "Course created" toast/banner + updated list
- Validation error: inline field error
- Server error: error banner + retry

### Course form (create/edit dialog)
- Initial: empty form
- Loading: submit disabled + spinner
- Validation error: inline errors + error summary
- Success: close dialog + confirm
- Server error: error banner + remain open

### Delete confirmation
- Destructive confirmation: dialog with "Delete course" + cancel
- Success: removed from list + confirm
- Server error: error banner + remain

### Course workspace
- Initial: skeleton
- Loading: "Loading course…"
- Error/Unauthorized: "Course not found" + return link
- Populated: course details + sections
- Partial (future sections): "coming in Phase 2" honest placeholder

### Landing page
- Populated: static marketing content (no loading needed)

## Implementation rule
Never show fabricated content in any state. Use honest placeholders ("coming in Phase 2") for unimplemented features rather than fake data.
