"""Google Gemini provider adapter.

Uses the Gemini REST API (generativelanguage.googleapis.com) via httpx, which
is already a project dependency. No dependency on the deprecated
google-generativeai SDK.

NOT CONFIGURED unless AQVERA_GOOGLE_GEMINI_API_KEY or GEMINI_API_KEY is set.
"""

from __future__ import annotations

import os
import time
from typing import Any

import httpx

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

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Mapping from AQVERA model ids to Gemini model names.
GEMINI_MODELS = {
    "gemini-3.5-flash-lite": {
        "display": "Gemini 3.5 Flash-Lite",
        "api_name": "gemini-3.5-flash-lite",
        "task_types": [
            TaskType.CHAT,
            TaskType.TUTOR_EXPLANATION,
            TaskType.CONTENT_GENERATION,
            TaskType.QUESTION_GENERATION,
            TaskType.ANSWER_EVALUATION,
            TaskType.SUMMARIZATION,
            TaskType.EXTRACTION,
        ],
        "context_window": 1_000_000,
        "max_output": 8192,
        "vision": True,
        "pricing": (0.0, 0.0),  # free tier
        "free_tier": True,
    },
    "gemini-3.6-flash": {
        "display": "Gemini 3.6 Flash",
        "api_name": "gemini-3.6-flash",
        "task_types": [
            TaskType.CHAT,
            TaskType.TUTOR_EXPLANATION,
            TaskType.CONTENT_GENERATION,
            TaskType.QUESTION_GENERATION,
            TaskType.ANSWER_EVALUATION,
            TaskType.SUMMARIZATION,
        ],
        "context_window": 1_000_000,
        "max_output": 8192,
        "vision": True,
        "pricing": (0.0, 0.0),
        "free_tier": True,
    },
    "gemini-3.8-flash": {
        "display": "Gemini 3.8 Flash",
        "api_name": "gemini-3.8-flash",
        "task_types": [
            TaskType.CHAT,
            TaskType.TUTOR_EXPLANATION,
            TaskType.CONTENT_GENERATION,
            TaskType.IMAGE_UNDERSTANDING,
            TaskType.SUMMARIZATION,
        ],
        "context_window": 1_000_000,
        "max_output": 65536,
        "vision": True,
        "pricing": (0.75, 3.0),
        "free_tier": False,
    },
}


class GeminiProvider(AIProvider):
    """Google Gemini provider adapter (REST via httpx)."""

    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        api_key = config.api_key or os.getenv("AQVERA_GOOGLE_GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            self._client = None
            self._configured = False
        else:
            self._client = httpx.AsyncClient(
                base_url=GEMINI_BASE_URL,
                timeout=config.timeout_ms / 1000.0 if config.timeout_ms else 30.0,
                headers={"x-goog-api-key": api_key},
            )
            self._configured = True

    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.OPENAI_COMPATIBLE  # Gemini is REST, but treated as compatible family

    @property
    def available_models(self) -> list[ModelConfig]:
        models: list[ModelConfig] = []
        for model_id, info in GEMINI_MODELS.items():
            caps = [
                ModelCapability(
                    name=model_id,
                    structured_output=False,
                    streaming=True,
                    vision=info["vision"],
                    max_context_tokens=info["context_window"],
                    cost_per_input_token=info["pricing"][0],
                    cost_per_output_token=info["pricing"][1],
                )
            ]
            models.append(
                ModelConfig(
                    name=model_id,
                    provider=self.config.id,
                    capabilities=caps,
                    default_task_types=list(info["task_types"]),
                    is_active=self._configured and info["free_tier"],
                )
            )
        return models

    async def is_healthy(self) -> bool:
        if not self._configured or self._client is None:
            return False
        try:
            resp = await self._client.get("/models", timeout=10.0)
            return resp.status_code == 200
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
                    message="Gemini provider not configured (no API key)",
                    retryable=False,
                ),
            )

        model_info = GEMINI_MODELS.get(request.model)
        if model_info is None:
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
                    category=AIErrorCategory.INVALID_REQUEST,
                    message=f"Unknown Gemini model: {request.model}",
                    retryable=False,
                ),
            )

        start = time.time()
        try:
            safe_messages = self.guard_prompt(request.messages)
            contents = self._to_gemini_contents(safe_messages)
            payload: dict[str, Any] = {"contents": contents}
            generation_config: dict[str, Any] = {}
            if request.temperature is not None:
                generation_config["temperature"] = request.temperature
            if request.max_tokens:
                generation_config["maxOutputTokens"] = request.max_tokens
            if generation_config:
                payload["generationConfig"] = generation_config

            resp = await self._client.post(
                f"/models/{model_info['api_name']}:generateContent",
                json=payload,
                timeout=(request.timeout_ms / 1000.0) if request.timeout_ms else 30.0,
            )
            latency_ms = int((time.time() - start) * 1000)

            if resp.status_code == 429:
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
                    error=AIError(
                        category=AIErrorCategory.RATE_LIMIT,
                        message=resp.text,
                        retryable=True,
                    ),
                )
            if resp.status_code in (401, 403):
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
                    error=AIError(
                        category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                        message=resp.text,
                        retryable=False,
                    ),
                )
            resp.raise_for_status()
            data = resp.json()
            self.mark_success()
            return self._parse_response(data, latency_ms, request.model)
        except httpx.TimeoutException as exc:
            self.mark_failure()
            return AIResponse(
                content=None,
                structured_output=None,
                usage=AIUsage(),
                cost_estimate=None,
                latency_ms=int((time.time() - start) * 1000),
                provider=self.config.id,
                model=request.model,
                finish_reason=None,
                error=AIError(
                    category=AIErrorCategory.TIMEOUT,
                    message=str(exc),
                    retryable=True,
                ),
            )
        except Exception as exc:  # noqa: BLE001
            self.mark_failure()
            return AIResponse(
                content=None,
                structured_output=None,
                usage=AIUsage(),
                cost_estimate=None,
                latency_ms=int((time.time() - start) * 1000),
                provider=self.config.id,
                model=request.model,
                finish_reason=None,
                error=self.classify_error(exc),
            )

    # ------------------------------------------------------------------ #
    # Gemini format conversion
    # ------------------------------------------------------------------ #

    def _to_gemini_contents(self, messages: list[Message]) -> list[dict]:
        contents: list[dict] = []
        for m in messages:
            role = "model" if m.role == "assistant" else ("user" if m.role == "user" else "model")
            contents.append({"role": role, "parts": [{"text": m.content}]})
        return contents

    def _parse_response(self, data: dict, latency_ms: int, model: str) -> AIResponse:
        candidates = data.get("candidates", [])
        content = ""
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            content = "".join(p.get("text", "") for p in parts)
        usage_meta = data.get("usageMetadata", {})
        usage = AIUsage(
            input_tokens=int(usage_meta.get("promptTokenCount", 0) or 0),
            output_tokens=int(usage_meta.get("candidatesTokenCount", 0) or 0),
            total_tokens=int(usage_meta.get("totalTokenCount", 0) or 0),
        )
        return AIResponse(
            content=content or None,
            structured_output=None,
            usage=usage,
            cost_estimate=None,
            latency_ms=latency_ms,
            provider=self.config.id,
            model=model,
            finish_reason=candidates[0].get("finishReason") if candidates else None,
            error=None,
        )