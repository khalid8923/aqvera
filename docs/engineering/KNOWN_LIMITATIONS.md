# KNOWN_LIMITATIONS.md

# AQVERA — Known Limitations

## Phase 0 (Documentation/Architecture) Limitations

- No application code exists; this is a blueprint only.
- D:\AQVERA is read-only for the executing user; documentation staged in temp directory pending write access.
- Initial AI provider not selected (OPEN).
- Initial academic domain not confirmed (mathematics recommended, OPEN).
- No git repository initialized.

## MVP Limitations (All Phases)

- **Single domain initially:** Mathematics is the recommended first domain; other domains (CS, physics, languages, humanities) deferred.
- **No Bayesian Knowledge Tracing:** Rule-based mastery estimation initially; BKT is a possible later enhancement.
- **No programming code execution sandbox:** Programming exercises presented without direct untrusted code execution in the main process.
- **Limited visual tools:** Only function graphing/equation visualization initially; other visualization types deferred.
- **No multi-tenancy:** Single-tenant / private operation only.
- **No mobile native apps:** Desktop + mobile browser layouts only.
- **Not a public SaaS:** Private, self-hosted operation only.
- **No regulatory compliance claims:** GDPR, COPPA, FERPA, etc. not assessed; do not claim compliance without evidence.

## Technical Limitations

- **AI provider dependence for content generation:** While providers are replaceable, content generation requires at least one working AI provider.
- **Vector search limited to pgvector:** Sufficient for initial scale; separate vector DB not introduced.
- **Knowledge tracing is rule-based initially:** Explainable but simpler than Bayesian/Deep Knowledge Tracing; replaceable interface allows future upgrade.
- **Subjective evaluation confidence is estimated:** Not a guarantee of correctness; exposed as confidence to avoid misleading precision.
- **Prompt injection resistance:** Mitigated via system instruction separation and untrusted document handling; not formally verified.

## Operational Limitations

- **Single-host Docker Compose:** Not designed for high-traffic enterprise scale.
- **Background worker on same host:** No separate worker cluster initially.
- **Object storage via MinIO/S3-compatible:** Single bucket; no multi-region replication.

## Future Work to Address Limitations

- Bayesian Knowledge Tracing (after sufficient data).
- Programming assessment sandbox.
- Additional visualization types.
- Additional academic domains.
- Multi-tenancy (if needed).
- Public SaaS readiness (security audit, compliance).
