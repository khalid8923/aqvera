"""OpenAI-compatible provider adapter (OpenAI, OpenRouter, Groq, NVIDIA, etc.).

Uses the OpenAI Python client against any OpenAI-compatible endpoint.
NOT CONFIGURED unless an API key is supplied via environment variables.
"""

from __future__ import annotations

import os
import time
from typing import Any

from openai import AsyncOpenAI

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
    ProviderNotConfiguredError,
)
from ai.providers.base import AIProvider


class OpenAICompatibleProvider(AIProvider):
    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        api_key = config.api_key or os.getenv("AQVERA_OPENAI_COMPATIBLE_API_KEY")
        if not api_key:
            self._client = None
            self._configured = False
        else:
            self._client = AsyncOpenAI(
                api_key=api_key,
                base_url=config.endpoint or "https://api.openai.com/v1",
                timeout=config.timeout_ms / 1000.0 if config.timeout_ms else 30.0,
            )
            self._configured = True

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.OPENAI_COMPATIBLE

    @property
    def available_models(self) -> list[ModelConfig]:
        return [
            ModelConfig(
                name="gpt-4o-mini",
                provider=self.config.id,
                capabilities=[
                    ModelCapability(
                        name="gpt-4o-mini",
                        structured_output=True,
                        streaming=True,
                        vision=True,
                        max_context_tokens=128_000,
                    )
                ],
                default_task_types=[
                    TaskType.CHAT,
                    TaskType.TUTOR_EXPLANATION,
                    TaskType.CONTENT_GENERATION,
                    TaskType.QUESTION_GENERATION,
                    TaskType.ANSWER_EVALUATION,
                    TaskType.SUMMARIZATION,
                ],
                is_active=self._configured,
            ),
            ModelConfig(
                name="gpt-4o",
                provider=self.config.id,
                capabilities=[
                    ModelCapability(
                        name="gpt-4o",
                        structured_output=True,
                        streaming=True,
                        vision=True,
                        max_context_tokens=128_000,
                    )
                ],
                default_task_types=[
                    TaskType.TUTOR_EXPLANATION,
                    TaskType.IMAGE_UNDERSTANDING,
                    TaskType.CONTENT_GENERATION,
                ],
                is_active=self._configured,
            ),
        ]

    async def is_healthy(self) -> bool:
        if not self._configured or self._client is None:
            return False
        try:
            await self._client.models.list()
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
                    message="OpenAI-compatible provider not configured (no API key)",
                    retryable=False,
                ),
            )

        start = time.time()
        try:
            safe_messages = self.guard_prompt(request.messages)
            completion = await self._client.chat.completions.create(
                model=request.model,
                messages=[{"role": m.role, "content": m.content} for m in safe_messages],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=request.stream,
                timeout=request.timeout_ms / 1000.0 if request.timeout_ms else None,
            )
            latency_ms = int((time.time() - start) * 1000)
            choice = completion.choices[0]
            content = choice.message.content or ""
            usage = completion.usage
            ai_usage = AIUsage(
                input_tokens=getattr(usage, "prompt_tokens", 0) or 0,
                output_tokens=getattr(usage, "completion_tokens", 0) or 0,
                total_tokens=getattr(usage, "total_tokens", 0) or 0,
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
                finish_reason=choice.finish_reason,
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
