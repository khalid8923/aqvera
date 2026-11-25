# Learning Guide — AQVERA AI Subsystem

## What Each Subsystem Does

| Subsystem | Purpose |
|-----------|---------|
| Providers | Translate AQVERA's provider-agnostic requests into provider-specific API calls and back. |
| Orchestration | Coordinates AI requests for tutoring, questions, evaluation, content generation. |
| Routing | Selects the best provider per task, with fallback, circuit breaker, and budget checks. |
| Agents | Domain AI agents (tutor, content) that operate within teaching-methodology boundaries. |
| Tutoring | Course-aware, source-grounded tutoring; distinguishes source/external/inference/uncertain. |
| RAG | Retrieves relevant chunks from uploaded materials, generates grounded answers with citations. |
| Retrieval | Embeddings, vector search, keyword search, reranking. |
| Memory | Conversation memory for tutor context. |
| Adaptive Learning | Deterministic mastery estimation and recommendations (no AI in core math). |
| Assessment | Question model, deterministic + subjective grading, validation. |
| Multimodal | Image/audio/video processing interfaces. |
| Prompts | Versioned prompt templates. |
| Evaluation | Model/output evaluation with representative academic test cases. |
| Cost Control | Budgets, spending ceilings, graceful degradation. |
| Monitoring | Latency tracking. |
| Security | Prompt-injection defense, credential handling. |

## How Requests Flow

```
Backend domain → Orchestrator.generate() → PromptInjectionGuard →
Router (budget + health + task match) → Provider Adapter →
Provider API → AIResponse → validated → Backend domain
```

## How to Add a Provider

1. Subclass `ai.providers.base.AIProvider`.
2. Implement `is_healthy()`, `complete()`, `supports_task()`, `capabilities_for()`.
3. Register in `ProviderRegistry`.
4. Add contract tests in `ai/tests/`.

## How to Add a Model

1. Add `ModelConfig` to provider's `available_models`.
2. Declare capabilities and mapped `TaskType`s.

## How Fallback Works

Router tries providers in priority order. On retryable error, tries next.
Capped at `max_fallback` to avoid redundant paid requests.

## How RAG Works

Query → embed → vector search + keyword search → merge → optional rerank →
build context with citations → generate answer grounded in context → attribute
sources. LLM never invents citations.

## How Memory Is Stored

`MemoryStore` holds `ConversationMemory` per conversation (in-memory; backend
may persist to DB). Last N turns used as tutor context.

## How to Evaluate a Model

`Evaluator.run_case()` runs representative academic `EvalCase`s through the
orchestrator and judges grounding, answers, and structured output. Runs against
MockProvider (no live calls).

## How Costs Are Estimated

`CostTracker` records per-request cost (provider-reported or estimated).
Budgets checked before each call; exhausted budgets block paid requests.

## How to Test Without Paid API Requests

Use `MockProvider`. Run `python -m pytest` in backend. No provider key needed.
Real provider behavior is only exercised when a key is configured and a live
test is explicitly run.
