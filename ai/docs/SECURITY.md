# Security

## Core Principles

- Uploaded documents are untrusted data.
- Instructions inside uploaded files must never override system policies.
- No claim of regulatory compliance without evidence.
- Private academic documents and student learning records are protected.

## Prompt-Injection Defense

`PromptInjectionGuard` sanitizes user-facing content before it reaches provider
prompts. Detection markers include "ignore previous instructions", "system:",
"you are now", "override system", etc. Sanitized content replaces markers with
`[injection marker removed]`.

System instructions are in a separate channel; document text is never
concatenated into the system prompt. Retrieved content is treated as untrusted
and sanitized before use in prompts.

## Credential Handling

- API keys never hardcoded.
- API keys never committed to the repository.
- API keys never logged.
- API keys never returned to the frontend.
- Credentials provided via environment variables (see `.env.example`).
- `.env.example` documents variable names without real values.

## Data Flow to Providers

- Only course-relevant text is sent to AI providers.
- Minimize PII: student IDs, not names; redact sensitive content.
- Requests go through the AI Abstraction Layer, never direct provider access
  from the frontend.

## Output Validation

All AI outputs validated against structured contracts before reaching business
logic. Malformed JSON, incomplete responses, and unsupported capabilities are
handled safely with fallback behavior.

## What Is NOT Logged

- Document text content.
- Student names/emails in AI logs.
- Assessment answers.
- Passwords or password hashes.
- API keys/secrets.

## Provider Status

No provider key configured → no real provider requests. Security controls are
implemented and ready for live credentials.
