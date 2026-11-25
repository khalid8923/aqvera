# Provider Routing

## Routing Model

`Router.route(request, task_type, user_id, preferred_provider)` selects a provider:

1. Find active providers supporting the task type (`ProviderRegistry.find_for_task`).
2. Optionally promote a preferred provider to the front.
3. For each candidate (up to `max_fallback`):
   - Check budget (daily/monthly/per-user ceilings).
   - Call `provider.complete()`.
   - On success, return the response.
   - On retryable error, try the next provider as fallback.
   - On non-retryable error (invalid request, unsupported capability), try next.
4. If all fail, return an `AIResponse` with an error and no content.

## Provider Selection Criteria

Priority order (configurable per provider):
1. Task compatibility (must support the task).
2. Provider priority (admin-configured).
3. Health (circuit-breaker open providers skipped).
4. Budget (not exceeded).
5. Cost (cheapest acceptable — future enhancement).

## Fallback

When a primary provider fails with a retryable error, the router falls back to
the next eligible provider. Fallback is capped at `max_fallback` (default 3) to
avoid redundant paid requests. AQVERA does **not** send multiple redundant paid
requests merely to increase the number of providers used.

## Circuit Breaker

Per-provider. Trips after `max_retries` consecutive failures.
- Closed: requests proceed normally.
- Open: requests rejected immediately, fallback used.
- Half-open: trial request tests recovery (not yet implemented).

## Adding a Provider

1. Implement `AIProvider` (see `ai/providers/base.py`).
2. Register in `ProviderRegistry` at application startup.
3. Configure priority, default model, rate limits, timeouts.
4. Add contract tests in `ai/tests/`.

## Adding a Model

1. Add a `ModelConfig` to the provider's `available_models`.
2. Declare capabilities (structured_output, streaming, vision, audio, video,
   max_context_tokens, costs).
3. Map the model to appropriate `TaskType`s in `default_task_types`.

## Provider Configuration (.env.example)

```
# OpenAI-compatible (OpenAI, OpenRouter, Groq, NVIDIA)
AQVERA_OPENAI_COMPATIBLE_API_KEY=
AQVERA_OPENAI_COMPATIBLE_ENDPOINT=https://api.openai.com/v1

# Anthropic
AQVERA_ANTHROPIC_API_KEY=
AQVERA_ANTHROPIC_ENDPOINT=https://api.anthropic.com
```

## Provider Status

| Provider | Adapter | Configured? | Notes |
|----------|---------|-------------|-------|
| OpenAI-compatible | `OpenAICompatibleProvider` | No | Needs `AQVERA_OPENAI_COMPATIBLE_API_KEY` |
| Anthropic | `AnthropicProvider` | No | Needs `AQVERA_ANTHROPIC_API_KEY` |
| Mock | `MockProvider` | Yes (tests only) | Never makes live requests |

No provider key is committed. Real credentials go in `.env` (never committed).
