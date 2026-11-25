# Agent System

## Overview

AI agents coordinate retrieval, tutoring, and content generation for specific
academic workflows. Agents sit on top of the `Orchestrator` and provide
AI capabilities within the boundaries of the Standard Teaching Methodology.

## Agents

| Agent | Responsibility |
|-------|----------------|
| `TutorAgent` | Course-aware tutoring; preserves academic topic and source context. |
| `ContentAgent` | Generates lessons, examples, explanations, practice materials. |

## Agent Boundaries (per Standard Teaching Methodology)

| AI May | AI Must Not |
|--------|-------------|
| Generate lesson content, examples, explanations | Independently assign mastery scores |
| Suggest practice activities | Silently modify the learner model |
| Interpret student errors | Override validation rules |
| Generate assessment questions (validated) | Bypass output contracts/schema validation |
| Recommend next steps (input to engine) | Make final adaptive decisions without engine |

The `AdaptiveEngine` makes final learning decisions; agents provide input only.

## Data Flow

```
Student Question → TutorAgent → Orchestrator.generate() →
Router → Provider → AIResponse → AgentResult (content, sources, evidence_type)
```

## Evidence Type

Each agent result includes an `evidence_type`:
- `source`: answer grounded in uploaded materials.
- `external`: answer from external knowledge.
- `inference`: reasoned inference.
- `uncertain`: not enough evidence.

## Provider Status

Agents use the `MockProvider` in tests. No live provider is configured.
