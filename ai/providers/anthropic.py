"""Anthropic provider adapter (Claude).

NOT CONFIGURED unless an API key is supplied via environment variables.
"""

from __future__ import annotations

import os
import time
from typing import Any

from anthropic import AsyncAnthropic

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


class AnthropicProvider(AIProvider):
    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        api_key = config.api_key or os.getenv("AQVERA_ANTHROPIC_API_KEY")
        if not api_key:
            self._client = None
            self._configured = False
        else:
            self._client = AsyncAnthropic(
                api_key=api_key,
                base_url=config.endpoint or "https://api.anthropic.com",
                timeout=config.timeout_ms / 1000.0 if config.timeout_ms else 30.0,
            )
            self._configured = True

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.ANTHROPIC

    @property
    def available_models(self) -> list[ModelConfig]:
        return [
            ModelConfig(
                name="claude-3-5-sonnet-20241022",
                provider=self.config.id,
                capabilities=[
                    ModelCapability(
                        name="claude-3-5-sonnet-20241022",
                        structured_output=False,
                        streaming=True,
                        vision=True,
                        max_context_tokens=200_000,
                    )
                ],
                default_task_types=[
                    TaskType.TUTOR_EXPLANATION,
                    TaskType.CONTENT_GENERATION,
                    TaskType.QUESTION_GENERATION,
                    TaskType.ANSWER_EVALUATION,
                    TaskType.SUMMARIZATION,
                ],
                is_active=self._configured,
            ),
        ]

    async def is_healthy(self) -> bool:
        if not self._configured or self._client is None:
            return False
        try:
            # Anthropic has no cheap health endpoint; count a token as a lightweight call.
            await self._client.messages.create(
                model=self.available_models[0].name,
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}],
            )
            return True
        except Exception:
            return False

    def supports_task(self, task_type: TaskType) -> bool:
        return any(
            task_type in m.default_task_types for m in self.available_models if m.is_active
        )

    def capabilities_for(self, model: str) -> list[ModelCapability]:
        for m in self.available_models:
            if m.name == model:
                return m.capabilities
        return []

    async def complete(self, request: AIRequest) -> AIResponse:
        if not self._configured or self._client is None:
            return AIResponse(
                content=None,
                structured_output=None,
                usage=AIUsage(),
                cost_estimate=None,
                latency_ms=0,
                provider=self.config.id,
                model=request.model,
                finish_reason=None,
                error=AIError(
                    category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                    message="Anthropic provider not configured (no API key)",
                    retryable=False,
                ),
            )

        start = time.time()
        try:
            safe_messages = self.guard_prompt(request.messages)
            # Extract system message separately for Anthropic.
            system_msgs = [m.content for m in safe_messages if m.role == "system"]
            user_msgs = [m for m in safe_messages if m.role != "system"]
            system = system_msgs[0] if system_msgs else None

            response = await self._client.messages.create(
                model=request.model,
                system=system,
                max_tokens=request.max_tokens or 1024,
                temperature=request.temperature,
                messages=[
                    {"role": m.role, "content": m.content} for m in user_msgs
                ],
            )
            latency_ms = int((time.time() - start) * 1000)
            content_parts = [b.text for b in response.content if hasattr(b, "text")]
            content = "\n".join(content_parts)
            usage = response.usage
            ai_usage = AIUsage(
                input_tokens=getattr(usage, "input_tokens", 0) or 0,
                output_tokens=getattr(usage, "output_tokens", 0) or 0,
                total_tokens=(getattr(usage, "input_tokens", 0) or 0)
                + (getattr(usage, "output_tokens", 0) or 0),
            )
            self.mark_success()
            return AIResponse(
                content=content,
                structured_output=None,
                usage=ai_usage,
                cost_estimate=None,
                latency_ms=latency_ms,
                provider=self.config.id,
                model=request.model,
                finish_reason=response.stop_reason,
                error=None,
            )
        except Exception as exc:  # noqa: BLE001
            latency_ms = int((time.time() - start) * 1000)
            self.mark_failure()
            return AIResponse(
                content=None,
                structured_output=None,
                usage=AIUsage(),
                cost_estimate=None,
                latency_ms=latency_ms,
                provider=self.config.id,
                model=request.model,
                finish_reason=None,
                error=self.classify_error(exc),
            )
