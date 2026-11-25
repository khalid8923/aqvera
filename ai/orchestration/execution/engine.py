"""Execution engine.

The execution engine ties together the model router, fallback manager, and
resilience layer to execute AI tasks. It is the bridge between AQVERA's
orchestration layer and the provider adapters.

It does NOT contain provider implementations; it delegates to registered
provider adapters.
"""

from __future__ import annotations

from typing import Optional

from ai import AIError, AIErrorCategory, AIRequest, AIResponse, AIUsage, Message, TaskType
from ai.credentials.manager import CredentialManager
from ai.orchestration.tasks.types import TaskDefinition, get_task
from ai.registry.model_registry import ModelRegistry
from ai.resilience import CircuitBreaker, RetryConfig, execute_with_resilience, is_retryable
from ai.routing import FallbackManager, ModelRouter

# Provider adapter type (imported lazily to avoid circular import).
from ai.providers.base import AIProvider  # noqa: E402


class ExecutionEngine:
    """Executes AI tasks with routing, fallback, and resilience."""

    def __init__(
        self,
        registry: ModelRegistry,
        router: ModelRouter,
        fallback_manager: FallbackManager,
        credential_manager: CredentialManager,
        providers: dict[str, AIProvider],
    ) -> None:
        self.registry = registry
        self.router = router
        self.fallback_manager = fallback_manager
        self.credential_manager = credential_manager
        self._providers = providers
        # Per-provider circuit breakers.
        self._circuits: dict[str, CircuitBreaker] = {}

    def _circuit_for(self, provider_id: str) -> CircuitBreaker:
        if provider_id not in self._circuits:
            self._circuits[provider_id] = CircuitBreaker()
        return self._circuits[provider_id]

    async def execute(
        self,
        task_type: TaskType,
        messages: list[Message],
        user_id: Optional[str] = None,
        preferred_model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        diagnostic: bool = False,
    ) -> AIResponse:
        """Execute a chat/completion task with routing + fallback + resilience.

        Returns the first successful AIResponse. If all candidates fail,
        returns an AIResponse with an error and no content.
        """
        task_def = get_task(task_type)
        timeout_ms = task_def.timeout_ms if task_def else 30000

        chain = self.fallback_manager.build_chain(
            task_type=task_type,
            max_fallback=4,
            user_id=user_id,
            diagnostic=diagnostic,
        )

        last_error: Optional[AIError] = None
        attempted: list[str] = []

        for decision in chain.candidates():
            attempted.append(decision.model_id)
            provider_id = decision.provider_id

            provider = self._providers.get(provider_id)
            if provider is None:
                last_error = AIError(
                    category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                    message=f"Provider {provider_id} not registered",
                    retryable=False,
                )
                continue

            api_key = self.credential_manager.get_credential(provider_id)
            if api_key is None:
                last_error = AIError(
                    category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                    message=f"Provider {provider_id} not configured (no API key)",
                    retryable=False,
                )
                continue

            circuit = self._circuit_for(provider_id)
            if not circuit.allow_request():
                last_error = AIError(
                    category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                    message=f"Provider {provider_id} circuit breaker open",
                    retryable=False,
                )
                continue

            request = AIRequest(
                provider=provider_id,
                model=decision.model_id,
                messages=messages,
                task_type=task_type,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False,
                timeout_ms=timeout_ms,
            )

            try:
                response = await execute_with_resilience(
                    lambda: provider.complete(request),
                    retry_config=RetryConfig(max_retries=3),
                    circuit=circuit,
                    timeout_ms=timeout_ms,
                    is_retryable_fn=is_retryable,
                )
            except Exception as exc:  # noqa: BLE001
                last_error = AIError(
                    category=AIErrorCategory.UNKNOWN,
                    message=str(exc),
                    retryable=True,
                )
                continue

            if response.error is None:
                circuit.record_success()
                return response

            last_error = response.error
            if not is_retryable(response.error):
                # Non-retryable: stop trying fallbacks for this error class.
                continue
            circuit.record_failure()

        # All candidates failed.
        return AIResponse(
            content=None,
            structured_output=None,
            usage=AIUsage(),
            cost_estimate=None,
            latency_ms=0,
            provider="execution",
            model="none",
            finish_reason=None,
            error=last_error
            or AIError(
                category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                message=f"No provider available for task {task_type.value} (attempted: {attempted})",
                retryable=False,
            ),
        )