# SECURITY_ARCHITECTURE.md

# AQVERA — Security Architecture

## Core Principles (DECIDED)

- Security is part of the architecture from the beginning; not bolted on.
- Uploaded documents are untrusted data.
- Instructions inside uploaded files must never override system policies or application instructions.
- No claim of regulatory compliance without evidence.
- Private academic documents and student learning records are protected.

## A. Authentication

| Requirement | Implementation (PROPOSED) |
|-------------|---------------------------|
| Secure password handling | bcrypt or argon2id hashing; salted; pepper via env var |
| Session management | Server-side sessions; hashed refresh tokens; `Sessions` table |
| Token expiration | Access token short-lived (e.g., 15 min); refresh token longer (e.g., 7 days) |
| Password recovery | Email-based reset token; single-use; expiration; rate-limited |
| Account protection | Failed login lockout; rate limiting; MFA deferred |

## B. Authorization

| Requirement | Implementation (PROPOSED) |
|-------------|---------------------------|
| Resource ownership | `user_id` on all user-owned resources; ownership checks in service layer |
| Course-level access control | `CourseMemberships` table; role-based (student, instructor) |
| IDOR protection | Server-side permission validation on every resource access; never trust client-supplied IDs |
| Server-side permission validation | Middleware + service-level checks; authorization enforced on backend, not frontend |

## C. File Security

| Requirement | Implementation (PROPOSED) |
|-------------|---------------------------|
| File type validation | Allow-list extensions (PDF, DOCX, TXT, etc.); MIME type verification |
| File size limits | Configurable max (e.g., 50 MB per file) |
| Malicious file considerations | Antivirus scan (if available); sandboxed extraction; no execution of uploaded content |
| Secure file storage | S3-compatible; private bucket; signed URLs for download; no public access |
| Temporary processing files | Isolated temp directory; cleaned after processing; encrypted at rest |
| Download authorization | Signed, time-limited URLs; ownership check before serving |
| File deletion behavior | Soft delete metadata; actual file removal on retention policy or user request; orphan cleanup |

## D. AI Security

| Requirement | Implementation (PROPOSED) |
|-------------|---------------------------|
| Prompt injection from uploaded documents | System instructions in separate channel; document content treated as untrusted user input; delimiter-based separation; never concatenate document text into system prompt |
| Untrusted retrieved content | Retrieval results treated as untrusted; sanitized before use in prompts; source attribution required |
| Data leakage between users | Tenant isolation via `user_id` / `course_id` on all queries; no cross-user data in AI context |
| Secrets protection | API keys encrypted at rest; environment variables; never logged |
| Provider request boundaries | Requests go through Abstraction Layer; no direct provider access from frontend |
| Output validation | All AI outputs validated against structured contracts; sanitized before display |

## E. Data Privacy

| Requirement | Implementation (PROPOSED) |
|-------------|---------------------------|
| Minimize PII to external providers | Send student IDs, not names; redact sensitive content; configurable opt-out |
| Define transmitted content | Only course-relevant text sent to AI providers; document metadata only |
| Clear deletion behavior | User data deleted on account deletion; retention policy documented |
| Retention policies | Configurable per data type; audit events retained longer |
| Avoid logging private content | Logs exclude document text, PII, assessment answers; log metadata only |

## F. Operational Security

| Requirement | Implementation (PROPOSED) |
|-------------|---------------------------|
| Environment variables | Secrets via .env (dev) or secret manager (prod); never committed |
| Secret management | Encrypted credentials in database; rotation supported |
| CORS | Configured origins only; credentials allowed for same-origin |
| Rate limiting | Per-user and per-endpoint; AI provider rate limits enforced |
| Input validation | All API inputs validated; SQL injection prevented via ORM/parameterized queries |
| Dependency security | Regular dependency scanning; lockfile pinned versions |
| Audit logging | `AuditEvents` table; auth events, permission changes, data exports, deletions |

## G. Future Public Access (DEFERRED)

Before opening AQVERA to external students, address:

- Full security penetration test.
- Data processing agreement and privacy policy.
- Age verification / parental consent (if minors).
- Regulatory assessment (GDPR, COPPA, FERPA as applicable) — **do not claim compliance without evidence**.
- Public-facing authentication (OAuth providers).
- Terms of service and acceptable use.
- DDoS protection and WAF.
- Data residency and regional deployment.

## Security Boundaries

```
Client (browser) ← HTTPS → API Gateway (auth, rate limit, CORS)
                                                     ↓
                                          Business Services (server-side authorization)
                                                     ↓
                                          Database (row-level security via user_id)
                                                     ↓
                                          Object Storage (signed URLs, private bucket)
                                                     ↓
                                          AI Providers (via Abstraction Layer; encrypted credentials)
```

## What Is NOT Logged (DECIDED)

- Document text content.
- Student names/emails in AI logs.
- Assessment answers.
- Passwords or password hashes.
- API keys/secrets.

## What IS Logged (DECIDED)

- Request failures (endpoint, status code, user ID hash).
- Job failures (job type, failure reason, user ID hash).
- AI provider latency, usage, cost (tokens, not content).
- Processing duration per stage.
- Retrieval quality indicators (top-k, similarity scores — not content).
- Assessment evaluation errors (error type, not answer content).
