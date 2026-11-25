"""Mock provider adapter for contract testing without live API calls.

Used to test provider-independent architecture (routing, fallback, circuit
breaker, cost control, structured output validation) without consuming paid
API requests. Clearly labeled NOT CONFIGURED for live use.
"""

from __future__ import annotations

import time
from typing import Any

from ai import (
    AIError,
    AIErrorCategory,
    AIRequest,
    AIResponse,
    AIUsage,
    Message,
    ModelCapability,
    ModelConfig,
    ProviderConfig,
    ProviderType,
    TaskType,
)
from ai.providers.base import AIProvider


class MockProvider(AIProvider):
    """Deterministic mock for offline/contract testing.

    Never makes live provider requests. Returns canned responses based on
    request task type. Configured by default but marked as mock.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        cfg = config or ProviderConfig(
            id="mock",
            name="Mock Provider",
            type=ProviderType.MOCK,
            is_active=True,
            priority=0,
        )
        super().__init__(cfg)
        self._configured = True  # mock is always "configured" for tests
        self.fail_next = False
        self.custom_responses: dict[str, str] = {}

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.MOCK

    @property
    def available_models(self) -> list[ModelConfig]:
        return [
            ModelConfig(
                name="mock-model",
                provider=self.config.id,
                capabilities=[
                    ModelCapability(
                        name="mock-model",
                        structured_output=True,
                        streaming=False,
                        vision=False,
                        max_context_tokens=8192,
                    )
                ],
                default_task_types=[
                    TaskType.CHAT,
                    TaskType.TUTOR_EXPLANATION,
                    TaskType.CONTENT_GENERATION,
                    TaskType.QUESTION_GENERATION,
                    TaskType.ANSWER_EVALUATION,
                    TaskType.SUMMARIZATION,
                    TaskType.EXTRACTION,
                ],
                is_active=True,
            ),
        ]

    async def is_healthy(self) -> bool:
        return True

    def supports_task(self, task_type: TaskType) -> bool:
        return True

    def capabilities_for(self, model: str) -> list[ModelCapability]:
        return self.available_models[0].capabilities

    async def complete(self, request: AIRequest) -> AIResponse:
        start = time.time()
        if self.fail_next:
            self.fail_next = False
            self.mark_failure()
            return AIResponse(
                content=None,
                structured_output=None,
                usage=AIUsage(),
                cost_estimate=0.0,
                latency_ms=int((time.time() - start) * 1000),
                provider=self.config.id,
                model=request.model,
                finish_reason=None,
                error=AIError(
                    category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                    message="Mock provider forced failure",
                    retryable=True,
                ),
            )

        # Deterministic canned response based on last user message.
        last_user = ""
        for m in reversed(request.messages):
            if m.role == "user":
                last_user = m.content
                break
        content = self.custom_responses.get(
            request.model,
            f"Mock response to: {last_user[:60]}",
        )
        latency_ms = int((time.time() - start) * 1000)
        self.mark_success()
        return AIResponse(
            content=content,
            structured_output=None,
            usage=AIUsage(input_tokens=10, output_tokens=20, total_tokens=30),
            cost_estimate=0.0,
            latency_ms=latency_ms,
            provider=self.config.id,
            model=request.model,
            finish_reason="stop",
            error=None,
        )
