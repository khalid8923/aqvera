# Cost Control

## Overview

Configurable budgets prevent runaway AI spending. Budgets can be set per
provider, model, task type, and user, with daily and monthly ceilings.

## Budget Model

```
Budget {
  provider (optional),
  model (optional),
  task_type (optional),
  daily_usd (optional),
  monthly_usd (optional),
  per_user_daily_usd (optional),
}
```

## Enforcement

Before each provider call, `CostTracker.check_budget()` verifies:
- Daily cost + estimated cost ≤ daily ceiling.
- Monthly cost + estimated cost ≤ monthly ceiling.
- Per-user daily cost + estimated cost ≤ per-user ceiling.

If a budget would be exceeded, the request is **not** made. The router tries
the next eligible (lower-cost) provider, or returns an unavailable-provider
state.

## Budget Exhaustion Behavior

- Do not continue making paid requests.
- Use an eligible lower-cost provider only if configured.
- Otherwise explain that the service is temporarily unavailable.

## Usage Tracking

Every AI request logs: input_tokens, output_tokens, total_tokens,
estimated_cost, latency_ms, provider, model, task_type, user_id.

## Limitations

- No hard financial ceiling based solely on local estimates. Provider dashboards
  must also be configured with spending limits.
- Cost estimates are approximate unless the provider returns actual usage.

## Provider Status

No provider key configured → no real costs incurred. Cost tracking is active
for mock/test usage (recorded at $0.00).
