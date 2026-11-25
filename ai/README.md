# AQVERA — AI Subsystem

The `ai/` directory is AQVERA's independently organized AI layer. It sits between the
application backend and external AI providers, providing:

- Provider adapters (OpenAI, Anthropic, and more) behind a common interface.
- Model capability registry and task-to-model routing.
- Orchestration for tutoring, RAG, assessment, and content generation.
- Retrieval, chunking, embedding, and vector search abstraction.
- Adaptive learning engine (deterministic, rule-based).
- Multimodal capabilities (image, audio, video).
- Cost control, budget tracking, circuit breakers, retries.
- Security: prompt-injection defenses, credential handling.
- Monitoring: latency, usage, token accounting.

## Core Principle

AI models are capabilities, not the product's source of truth. AQVERA's teaching
methodology, assessment rules, learning progression, and adaptation logic remain
controlled by the platform. No single AI provider controls the academic experience.

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `providers/` | Provider adapters (OpenAI, Anthropic, mock/test) |
| `orchestration/` | Task orchestration (tutor, RAG, assessment, content generation) |
| `routing/` | Task-to-model routing, provider selection, fallback |
| `agents/` | Domain-specific AI agents (tutor, content, assessment) |
| `tutoring/` | AI tutor: course-aware, lesson-aware, source-grounded conversations |
| `rag/` | RAG pipeline: retrieval, context construction, source attribution |
| `retrieval/` | Vector/keyword retrieval, embeddings abstraction, reranking |
| `memory/` | Conversation and learning memory storage |
| `adaptive_learning/` | Deterministic mastery estimation, recommendations |
| `assessment/` | Question generation, evaluation, grading |
| `multimodal/` | Image, audio, video processing |
| `prompts/` | Versioned prompt templates |
| `evaluation/` | Model and output evaluation |
| `monitoring/` | Latency, usage, cost tracking |
| `cost_control/` | Budgets, spending ceilings, throttling |
| `security/` | Prompt-injection defense, credential handling |
| `tests/` | Contract tests, mock-based tests |
| `docs/` | AI subsystem documentation |

## Provider Status

No AI provider API key is configured in this repository. All provider adapters are
implemented and tested with mocks/contract tests. Providers are labeled
**NOT CONFIGURED** until a valid API key is added via environment variables.

See `ai/docs/PROVIDER_ROUTING.md` for how to add a provider and credentials.

## Testing Without Paid API Requests

All provider adapters and orchestration logic are tested using mocks and contract
tests. No live provider request is made in the test suite. See
`ai/docs/LOCAL_DEVELOPMENT.md` and `ai/tests/`.

## Documentation

- `ai/README.md` — this file
- `ai/docs/ARCHITECTURE.md` — subsystem architecture and data flows
- `ai/docs/PROVIDER_ROUTING.md` — adding providers, models, routing, fallback
- `ai/docs/RAG_PIPELINE.md` — retrieval-augmented generation
- `ai/docs/AGENT_SYSTEM.md` — AI agents and tutoring
- `ai/docs/MULTIMODAL_PIPELINE.md` — image/audio/video
- `ai/docs/ADAPTIVE_LEARNING.md` — mastery estimation, recommendations
- `ai/docs/COST_CONTROL.md` — budgets, throttling, graceful degradation
- `ai/docs/SECURITY.md` — prompt injection, credentials, secrets
- `ai/docs/LOCAL_DEVELOPMENT.md` — testing without paid API requests
- `ai/docs/LEARNING_GUIDE.md` — how to learn and extend the AI subsystem
