# AI_ARCHITECTURE.md

# AQVERA — AI Architecture

## Core Principle (DECIDED)

AQVERA must not become dependent on a single commercial AI API. An AI Provider Abstraction Layer sits between all AI-consuming business logic and the underlying providers. Providers are replaceable without rewriting the teaching methodology or core business logic.

## AI Provider Abstraction Layer

### Responsibilities (DECIDED)

| Capability | Description |
|------------|-------------|
| Provider configuration | Register/configure providers (endpoint, auth, defaults) |
| Model selection | Choose model per task type and capability |
| API credentials management | Encrypted storage and retrieval of provider credentials |
| Request/response normalization | Unified request/response schema across providers |
| Structured output handling | JSON-schema-constrained generation with validation |
| Streaming where appropriate | Token-by-token streaming for chat/tutor interactions |
| Token and usage tracking | Count input/output tokens per request |
| Cost estimation | Estimate cost before/after requests |
| Timeouts | Per-request and per-provider timeouts |
| Retries with safe limits | Exponential backoff, max retry count, idempotency |
| Rate limiting | Per-provider and per-user rate limits |
| Error classification | Translate provider errors into application error categories |
| Provider availability handling | Health checks, circuit breaker, fallback |
| Fallback policies | Primary → secondary provider chain on failure |
| Model capability metadata | Structured output support, streaming, context window, cost |

### Contract

```
AIRequest {
  provider: string
  model: string
  messages: Message[]
  tools?: ToolDefinition[]
  tool_choice?: "auto" | "required" | "none"
  response_format?: JSONSchema
  temperature?: number
  max_tokens?: number
  stream?: boolean
  timeout_ms?: number
  idempotency_key?: string
}

AIResponse {
  content: string | null
  tool_calls: ToolCall[] | null
  structured_output: any | null      // validated against response_format
  usage: { input_tokens, output_tokens, total_tokens }
  cost_estimate: decimal
  latency_ms: integer
  provider: string
  model: string
  finish_reason: string
  error: AIError | null
}

AIError {
  category: "rate_limit" | "timeout" | "invalid_request" | "provider_unavailable" | "malformed_output" | "unsupported_capability" | "unknown"
  retryable: boolean
  message: string
  provider_error_code?: string
}
```

## Separation of Responsibilities (DECIDED)

| Component | Responsibility |
|-----------|---------------|
| **AI Orchestration** | Selects the appropriate model, tools, and workflow for a task. Routes tasks to providers based on capability, cost, and availability. |
| **Teaching Engine** | Applies the instructional methodology (versioned, provider-independent). Ensures teaching quality standards are met. |
| **Knowledge Retrieval** | Retrieves relevant academic evidence from vector store and document store. |
| **Evaluation Engine** | Validates answers and assessment outcomes. Deterministic for numerical/math; criteria+confidence for subjective. |
| **Adaptive Engine** | Determines learning decisions (next topic, review vs. advance, difficulty, retention). Never lets AI assign mastery silently. |
| **Content Generation** | Generates lessons, examples, explanations, and practice materials. Output validated against structured contracts. |

### Dependency Rule

Business components (Teaching, Evaluation, Adaptive) depend on the AI Abstraction Layer interface, not on concrete providers. The Abstraction Layer does not depend on business logic.

## Structured AI Output Contracts (DECIDED)

All important AI outputs are validated against JSON schemas before use. Contract schema files live under `docs/architecture/contracts/` and are maintained alongside architecture documents:

| Contract | Purpose | Schema Location |
|----------|---------|-----------------|
| Course structure generation | Proposed course from content | `docs/architecture/contracts/course_structure.json` |
| Topic extraction | Topics from document sections | `docs/architecture/contracts/topic_extraction.json` |
| Learning objective generation | Objectives from topics | `docs/architecture/contracts/learning_objectives.json` |
| Lesson generation | Lesson content | `docs/architecture/contracts/lesson_generation.json` |
| Question generation | Assessment questions | `docs/architecture/contracts/question_generation.json` |
| Error classification | Classifying student errors | `docs/architecture/contracts/error_classification.json` |
| Explanation generation | Explanations with sources | `docs/architecture/contracts/explanation_generation.json` |
| Source attribution | Citing academic sources | `docs/architecture/contracts/source_attribution.json` |

### Schema Validation Rule (DECIDED)

No AI output reaches application business logic without passing schema validation. Malformed JSON, incomplete responses, unsupported capabilities, and provider failures are handled safely with fallback behavior.

## Safe Handling Requirements (DECIDED)

| Failure Mode | Handling |
|--------------|----------|
| Malformed JSON | Reject; attempt repair once; fallback to template/default; log error |
| Incomplete responses | Detect missing required fields; retry or fallback; never partial-apply |
| Unsupported model capability | Route to capable provider; degrade gracefully; inform user |
| Provider failure | Circuit breaker; fallback to secondary provider; degraded response |
| Rate limit | Retry with backoff; respect provider retry-after headers |
| Timeout | Cancel request; retry once; fallback |

## AI Never Independently Assigns Mastery (DECIDED)

- AI may generate content, interpret errors, and suggest explanations.
- AI must NOT independently invent mastery scores.
- AI must NOT silently modify the learner model.
- Mastery scores come from the Adaptive Engine based on structured assessment evidence.
- AI outputs that affect the learner model are treated as suggestions, validated by the Evaluation Engine and Adaptive Engine.

## Provider Configuration Model

```
ProviderConfig {
  id: UUID
  name: string
  type: "openai" | "anthropic" | "ollama" | "azure" | "custom"
  endpoint: string?
  api_key_encrypted: string
  is_active: boolean
  priority: integer
  default_model: string
  capabilities: ModelCapability[]
  rate_limits: RateLimitConfig
  timeout_ms: integer
  max_retries: integer
  fallback_provider_id: UUID?
}
```

## Initial Provider Selection (OPEN)

No provider selected yet. The abstraction layer is provider-agnostic. Recommended candidates: OpenAI, Anthropic, Ollama (local/private), Azure OpenAI. Decision requires user input.

## Error Classification Mapping

| Provider Error | AQVERA Category | Retryable | Action |
|----------------|-----------------|-----------|--------|
| 429 rate limit | rate_limit | Yes | Retry with backoff + fallback |
| 401/403 auth | provider_unavailable | No | Alert admin; fallback |
| 400 invalid request | invalid_request | No | Do not retry; log |
| 502/503/504 | provider_unavailable | Yes | Retry + fallback |
| Timeout | timeout | Yes | Retry once + fallback |
| Malformed JSON | malformed_output | Yes (once) | Repair attempt + fallback |
| Missing capability | unsupported_capability | No | Route to capable provider |

## Circuit Breaker

- Per-provider circuit breaker with closed/open/half-open states.
- Trips after N consecutive failures.
- Open state: reject requests immediately, use fallback.
- Half-open: trial request to test recovery.

## Token & Cost Tracking

Every AI request logs: input_tokens, output_tokens, total_tokens, estimated_cost, latency_ms, provider, model, task_type, user_id. Stored in `AITaskRecords` and aggregated in `UsageRecords`.

## Data Flow: AI Request

1. Business component requests AI capability (e.g., "generate question").
2. AI Orchestration selects provider+model based on task type, capability, cost, availability.
3. Request normalized through Abstraction Layer.
4. Provider called with retries, rate limiting, timeout.
5. Response normalized; structured output validated against schema.
6. Token/cost recorded.
7. Validated output returned to business component.
8. Business component applies output (never bypasses validation).

## Security

- Credentials encrypted at rest; never logged.
- Minimal PII sent to providers (student IDs, not names; redacted content where possible).
- Prompt injection from uploaded documents treated as untrusted; system instructions never overridden by document content.
- Output validation prevents injection of malicious content into the application.
