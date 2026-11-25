# PROJECT_CONTEXT.md

# AQVERA — Project Context

## Repository State

- **Path:** D:\AQVERA
- **Git:** Not a git repository (no .git directory).
- **Contents:** Empty directory (0 entries).
- **Write permissions:** The executing user (desktop-1kcl8nl\hpc) has ReadAndExecute only; cannot create directories or files in D:\AQVERA without Administrator elevation.
- **Existing code:** None.
- **Existing documentation:** None.
- **Existing configuration:** None.

## Project Origin

This is a greenfield project. AQVERA is being specified from scratch based on the requirements in sections 4–19 of the user's task description. Phase 0 is documentation and architecture only.

## Staging Location

Because D:\AQVERA is not writable, all Phase 0 documentation has been staged in:
`C:\Users\hpc\AppData\Local\Temp\kilo\aqvera-docs\`

These files must be copied to D:\AQVERA once write permissions are obtained.

## Key Constraints

1. **No implementation code in Phase 0.** Documentation and architecture only.
2. **Modular monolith** is the default architectural direction unless strong technical reason exists otherwise.
3. **Solo developer** suitability is a stated evaluation criterion.
4. **Private operation** — not a public SaaS initially.
5. **No single AI provider dependency** — provider abstraction layer required.
6. **Teaching methodology must be versioned, testable, and provider-independent.**

## Unresolved Questions Requiring User Input

- Write access to D:\AQVERA (requires Administrator elevation or permission change).
- Preferred AI provider(s) for initial implementation (open — abstraction layer supports multiple).
- Initial academic domain for the first vertical slice (open — mathematics is the recommended default).
- Database hosting (local PostgreSQL vs. managed) — deferred to deployment phase.

## Relationship to Other Documents

- DECISION_LOG.md records all major technical decisions with status (DECIDED/PROPOSED/OPEN/DEFERRED).
- docs/engineering/TECHNOLOGY_DECISIONS.md evaluates the candidate stack.
- docs/engineering/IMPLEMENTATION_ROADMAP.md defines phases A–F.
- AGENTS.md defines agent workflow rules and conventions.
