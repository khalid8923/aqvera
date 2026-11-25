# AI Subsystem Architecture

## Overview

The `ai/` subsystem is AQVERA's independently organized AI layer. It sits between
the application backend and external AI providers, providing provider-agnostic
interfaces for tutoring, RAG, assessment, content generation, adaptive learning,
and multimodal processing.

## Core Principle

AI models are capabilities, not the product's source of truth. AQVERA's teaching
methodology, assessment rules, learning progression, adaptation logic, and source
attribution remain controlled by the platform. No single AI provider controls the
academic experience.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Backend (FastAPI)            │
│  Courses, Auth, Materials, Assessment, Adaptive Learning    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP / JSON (ai-service interface)
┌────────────────────▼────────────────────────────────────────┐
│                     AI Orchestrator                         │
│  generate() · explain() · generate_questions() · evaluate()  │
└────────────────────┬────────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    ▼                ▼                ▼
┌──────────┐   ┌──────────┐   ┌────────────┐
│ Tutor    │   │ RAG      │   │ Assessment │
│ Agent    │   │ Pipeline │   │ Engine     │
└──────────┘   └──────────┘   └────────────┘
         │                  │                  │
         ▼                  ▼                  ▼
    ┌─────────────────────────────────────────────┐
    │              AI Router                      │
    │  task→model · fallback · circuit breaker    │
    └────────────────────┬────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     ┌────────┐    ┌────────┐    ┌─────────┐
     │ OpenAI │    │ Claude │    │ Mock    │
     │ Adapter│    │ Adapter│    │ Adapter │
     └────────┘    └────────┘    └─────────┘
```

## Data Flow: AI Request

1. Backend domain (tutor/assessment/RAG) calls `Orchestrator.generate()`.
2. Orchestrator sanitizes user content via `PromptInjectionGuard`.
3. Request normalized into `AIRequest` (provider-agnostic).
4. `Router` selects provider based on task type, priority, budget, health.
5. Provider adapter translates to provider-specific format and calls the API.
6. Response normalized into `AIResponse`; usage/cost/latency recorded.
7. Structured output validated against contracts (where applicable).
8. Validated result returned to the backend domain.

## Directory Responsibilities

| Directory | Responsibility |
|-----------|----------------|
| `providers/` | Provider adapters (OpenAI-compatible, Anthropic, Mock) |
| `orchestration/` | High-level task orchestration (tutor, questions, evaluation) |
| `routing.py` | Task→model routing, fallback, circuit breaker, budget |
| `agents.py` | Domain AI agents (tutor agent, content agent) |
| `tutoring.py` | Course-aware, source-grounded tutoring |
| `rag.py` | RAG pipeline: retrieval → grounded answer |
| `retrieval.py` | Embeddings, vector store, keyword search, reranking |
| `memory.py` | Conversation memory store |
| `adaptive_learning.py` | Deterministic mastery estimation, recommendations |
| `assessment.py` | Question model, deterministic + subjective grading |
| `multimodal.py` | Image/audio/video processing interfaces |
| `prompts.py` | Versioned prompt templates |
| `evaluation.py` | Model/output evaluation |
| `cost_control.py` | Budgets, spending ceilings |
| `monitoring.py` | Latency tracking |
| `security.py` | Prompt-injection defense |

## Provider-Agnostic Contract

`AIRequest` → `AIResponse` is the contract between backend and providers.
Adapters never leak provider-specific types into business logic.

## Error Handling

| Provider Error | AQVERA Category | Retryable | Action |
|----------------|-----------------|-----------|--------|
| 429 rate limit | rate_limit | Yes | Retry with backoff + fallback |
| 401/403 auth | provider_unavailable | No | Fallback / unavailable message |
| 400 invalid request | invalid_request | No | Do not retry; log |
| 502/503/504 | provider_unavailable | Yes | Retry + fallback |
| Timeout | timeout | Yes | Retry once + fallback |
| Malformed output | malformed_output | Yes (once) | Repair + fallback |
| Missing capability | unsupported_capability | No | Route to capable provider |

## Circuit Breaker

Per-provider, with closed/open/half-open states. Trips after N consecutive
failures. Open state rejects immediately and uses fallback.

## Adding a Provider

1. Create an adapter subclassing `ai.providers.base.AIProvider`.
2. Implement `is_healthy()`, `complete()`, `supports_task()`, `capabilities_for()`.
3. Register the adapter in `ProviderRegistry`.
4. Add budget/cost control as needed.
5. Add contract tests in `ai/tests/`.

## Provider Status

No live provider API key is configured. All adapters are implemented and
contract-tested with the `MockProvider`. Providers are **NOT CONFIGURED** for
live use until a valid API key is supplied.
