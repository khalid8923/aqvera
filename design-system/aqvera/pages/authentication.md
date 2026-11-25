# pages/authentication.md

# AQVERA Design System — Authentication Pages

Status: PLANNED (not yet implemented)

## Notes

Authentication pages (`/login`, `/register`) do not yet exist. When built:
- Follow master design system exactly.
- Dialog-style or full-page form centered.
- Form fields with labels, validation, error summary.
- Primary button "Create account" / "Sign in".
- Loading state during auth; error messages for invalid credentials / weak password / email already registered.
- Never fabricate auth state.

## States

- Initial: empty form
- Loading: auth in progress
- Validation error: inline + error summary
- Success: redirect to dashboard
- Server error: error banner
