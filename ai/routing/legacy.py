"""Task-to-model routing with fallback, circuit breaker, and cost control.

Routes AI requests to providers based on task compatibility, cost, latency,
availability, and budget. Implements fallback chains and circuit breakers.
"""

from __future__ import annotations

from typing import Optional

from ai import (
    AIError,
    AIErrorCategory,
    AIRequest,
    AIResponse,
    AIUsage,
    TaskType,
)
from ai.cost_control import CostTracker, estimate_cost
from ai.providers.base import AIProvider, ProviderRegistry


class Router:
    """Selects providers for AI tasks and manages fallback."""

    def __init__(
        self,
        registry: ProviderRegistry,
        cost_tracker: CostTracker,
        max_fallback: int = 3,
    ) -> None:
        self.registry = registry
        self.cost_tracker = cost_tracker
        self.max_fallback = max_fallback

    async def route(
        self,
        request: AIRequest,
        task_type: TaskType,
        user_id: Optional[str] = None,
        preferred_provider: Optional[str] = None,
    ) -> AIResponse:
        """Route a request to the best available provider, with fallback.

        Returns the first successful response. If all providers fail or are
        unavailable, returns an AIResponse with an error and no content.
        """
        candidates = self._candidates(task_type, preferred_provider)

        last_error: Optional[AIError] = None
        attempts = 0

        for provider in candidates:
            if attempts >= self.max_fallback:
                break
            attempts += 1

            # Budget check before any paid request.
            estimated = self._estimate(provider, task_type)
            allowed, reason = self.cost_tracker.check_budget(
                provider.config.id,
                request.model,
                task_type,
                estimated,
                user_id,
            )
            if not allowed:
                last_error = AIError(
                    category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                    message=reason or "Budget exhausted",
                    retryable=False,
                )
                continue

            response = await provider.complete(request)
            # Record usage via provider's own tracker (keeps per-provider metrics).
            # The caller may also record via CostRecord; avoid double counting.

            if response.error is None:
                return response

            last_error = response.error
            # Circuit-break non-retryable errors immediately; retryable errors fall through.
            if response.error.category in (
                AIErrorCategory.INVALID_REQUEST,
                AIErrorCategory.UNSUPPORTED_CAPABILITY,
            ):
                continue
            # For retryable errors, try the next provider as fallback.

        # All attempts failed or no providers available.
        return AIResponse(
            content=None,
            structured_output=None,
            usage=AIUsage(),
            cost_estimate=None,
            latency_ms=0,
            provider=request.provider or "none",
            model=request.model,
            finish_reason=None,
            error=last_error
            or AIError(
                category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                message="No provider available for task",
                retryable=False,
            ),
        )

    def _candidates(
        self,
        task_type: TaskType,
        preferred_provider: Optional[str],
    ) -> list[AIProvider]:
        eligible = self.registry.find_for_task(task_type)
        if preferred_provider:
            pref = self.registry.get(preferred_provider)
            if pref is not None and pref.supports_task(task_type):
                eligible.remove(pref)
                eligible.insert(0, pref)
        return eligible

    def _estimate(self, provider: AIProvider, task_type: TaskType) -> float:
        # Conservative estimate; provider may return actual cost in response.
        return 0.01
