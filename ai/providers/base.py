"""Provider adapter interface and base class.

All provider adapters implement AIProvider and translate between AQVERA's
provider-agnostic types and provider-specific request/response formats.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ai import (
    AIError,
    AIErrorCategory,
    AIRequest,
    AIResponse,
    ModelCapability,
    ModelConfig,
    ProviderConfig,
    ProviderType,
    TaskType,
)
from ai.cost_control import CostTracker
from ai.monitoring import LatencyTracker
from ai.security import PromptInjectionGuard


class AIProvider(ABC):
    """Abstract base for AI provider adapters."""

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config
        self._cost_tracker = CostTracker()
        self._latency_tracker = LatencyTracker()
        self._injection_guard = PromptInjectionGuard()
        self._consecutive_failures = 0
        self._circuit_open = False

    @property
    @abstractmethod
    def provider_type(self) -> ProviderType:
        ...

    @property
    @abstractmethod
    def available_models(self) -> list[ModelConfig]:
        ...

    @abstractmethod
    async def is_healthy(self) -> bool:
        """Return True if the provider is reachable and configured."""

    @abstractmethod
    async def complete(self, request: AIRequest) -> AIResponse:
        """Generate a completion for the given request."""

    @abstractmethod
    def supports_task(self, task_type: TaskType) -> bool:
        """Return True if this provider can handle the task type."""

    @abstractmethod
    def capabilities_for(self, model: str) -> list[ModelCapability]:
        """Return capabilities for a model."""

    # --- Cross-cutting concerns (shared by all adapters) ---

    def record_usage(self, response: AIResponse, task_type: TaskType, user_id: str | None = None) -> CostRecord:
        record = CostRecord(
            provider=response.provider,
            model=response.model,
            task_type=task_type,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            estimated_cost=response.cost_estimate or 0.0,
            latency_ms=response.latency_ms,
            user_id=user_id,
        )
        self._cost_tracker.record(record)
        self._latency_tracker.record(response.latency_ms)
        return record

    def guard_prompt(self, messages: list[Message]) -> list[Message]:
        """Strip prompt-injection attempts from untrusted user content."""
        return self._injection_guard.sanitize(messages)

    def mark_failure(self) -> None:
        self._consecutive_failures += 1
        if self._consecutive_failures >= self.config.max_retries:
            self._circuit_open = True

    def mark_success(self) -> None:
        self._consecutive_failures = 0
        self._circuit_open = False

    @property
    def circuit_open(self) -> bool:
        return self._circuit_open

    def classify_error(self, exc: Exception, provider_error_code: str | None = None) -> AIError:
        text = str(exc).lower()
        if "rate limit" in text or "429" in text:
            return AIError(
                category=AIErrorCategory.RATE_LIMIT,
                message=str(exc),
                retryable=True,
                provider_error_code=provider_error_code,
            )
        if "timeout" in text or "504" in text:
            return AIError(
                category=AIErrorCategory.TIMEOUT,
                message=str(exc),
                retryable=True,
                provider_error_code=provider_error_code,
            )
        if "unauthorized" in text or "401" in text or "403" in text:
            return AIError(
                category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                message=str(exc),
                retryable=False,
                provider_error_code=provider_error_code,
            )
        if "invalid" in text or "400" in text:
            return AIError(
                category=AIErrorCategory.INVALID_REQUEST,
                message=str(exc),
                retryable=False,
                provider_error_code=provider_error_code,
            )
        return AIError(
            category=AIErrorCategory.UNKNOWN,
            message=str(exc),
            retryable=True,
            provider_error_code=provider_error_code,
        )


class ProviderRegistry:
    """Holds registered provider adapters and selects among them."""

    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}
        self._configs: dict[str, ProviderConfig] = {}

    def register(self, provider: AIProvider) -> None:
        self._providers[provider.config.id] = provider
        self._configs[provider.config.id] = provider.config

    def get(self, provider_id: str) -> AIProvider | None:
        return self._providers.get(provider_id)

    def list_active(self) -> list[AIProvider]:
        return [p for p in self._providers.values() if p.config.is_active and not p.circuit_open]

    def get_config(self, provider_id: str) -> ProviderConfig | None:
        return self._configs.get(provider_id)

    def find_for_task(self, task_type: TaskType) -> list[AIProvider]:
        """Return active providers that support the task, ordered by priority."""
        eligible = [
            p
            for p in self.list_active()
            if p.supports_task(task_type)
        ]
        eligible.sort(key=lambda p: p.config.priority, reverse=True)
        return eligible
