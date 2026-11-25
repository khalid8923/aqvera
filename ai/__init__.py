"""Core types and exceptions for the AQVERA AI subsystem.

All types are provider-agnostic. Concrete provider adapters translate between
these types and provider-specific request/response formats.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class TaskType(str, Enum):
    """Categories of AI tasks AQVERA performs."""

    CHAT = "chat"
    TUTOR_EXPLANATION = "tutor_explanation"
    CONTENT_GENERATION = "content_generation"
    QUESTION_GENERATION = "question_generation"
    ANSWER_EVALUATION = "answer_evaluation"
    EXTRACTION = "extraction"
    SUMMARIZATION = "summarization"
    EMBEDDING = "embedding"
    IMAGE_UNDERSTANDING = "image_understanding"
    IMAGE_GENERATION = "image_generation"
    SPEECH_TO_TEXT = "speech_to_text"
    TEXT_TO_SPEECH = "text_to_speech"
    TRANSCRIPTION = "transcription"
    RERANK = "rerank"
    WEB_RESEARCH = "web_research"


class ProviderType(str, Enum):
    """Supported provider families."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENAI_COMPATIBLE = "openai_compatible"  # OpenRouter, Groq, NVIDIA, etc.
    LOCAL = "local"
    MOCK = "mock"


class TaskCapability(str, Enum):
    """Capability flags for models and providers."""

    TEXT = "text"
    VISION = "vision"
    AUDIO_INPUT = "audio_input"
    AUDIO_OUTPUT = "audio_output"
    EMBEDDING = "embedding"
    IMAGE_GENERATION = "image_generation"
    STRUCTURED_OUTPUT = "structured_output"
    TOOL_CALLING = "tool_calling"
    STREAMING = "streaming"
    WEB_SEARCH = "web_search"


class PricingClass(str, Enum):
    """Pricing classification for a model."""

    FREE = "free"
    TRIAL = "trial"
    PAID = "paid"
    UNKNOWN = "unknown"
    LOCAL = "local"


class FreeTierStatus(str, Enum):
    """Free-tier status of a model/provider."""

    PERMANENT = "permanent"
    TRIAL = "trial"
    CREDIT = "credit"
    NONE = "none"
    UNKNOWN = "unknown"


class AvailabilityStatus(str, Enum):
    """Availability status of a model."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    DISABLED = "disabled"


class AIErrorCategory(str, Enum):
    """Error categories for consistent handling across providers."""

    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    INVALID_REQUEST = "invalid_request"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    MALFORMED_OUTPUT = "malformed_output"
    UNSUPPORTED_CAPABILITY = "unsupported_capability"
    UNKNOWN = "unknown"


@dataclass
class AIError:
    category: AIErrorCategory
    message: str
    retryable: bool
    provider_error_code: Optional[str] = None


@dataclass
class Message:
    role: str  # "system" | "user" | "assistant" | "tool"
    content: str


@dataclass
class AIRequest:
    provider: str
    model: str
    messages: list[Message]
    task_type: TaskType
    temperature: float | None = None
    max_tokens: int | None = None
    stream: bool = False
    response_format: dict[str, Any] | None = None
    timeout_ms: int | None = None
    idempotency_key: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AIUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


@dataclass
class AIResponse:
    content: str | None
    structured_output: Any | None
    usage: AIUsage
    cost_estimate: float | None
    latency_ms: int
    provider: str
    model: str
    finish_reason: str | None
    error: AIError | None


@dataclass
class ModelCapability:
    name: str
    structured_output: bool = False
    streaming: bool = False
    vision: bool = False
    audio: bool = False
    video: bool = False
    max_context_tokens: int | None = None
    cost_per_input_token: float | None = None
    cost_per_output_token: float | None = None


@dataclass
class ModelConfig:
    name: str
    provider: str
    capabilities: list[ModelCapability] = field(default_factory=list)
    default_task_types: list[TaskType] = field(default_factory=list)
    is_active: bool = True


@dataclass
class ProviderConfig:
    id: str
    name: str
    type: ProviderType
    endpoint: str | None = None
    api_key: str | None = None
    is_active: bool = True
    priority: int = 0
    default_model: str | None = None
    rate_limits: dict[str, Any] = field(default_factory=dict)
    timeout_ms: int = 30000
    max_retries: int = 3
    fallback_provider_id: str | None = None


@dataclass
class CostRecord:
    provider: str
    model: str
    task_type: TaskType
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    latency_ms: int
    user_id: str | None = None
    timestamp: str | None = None


class ProviderNotConfiguredError(Exception):
    """Raised when no provider is configured for a required task."""

    def __init__(self, message: str = "No provider is configured for the required task."):
        super().__init__(message)
        self.message = message


class ProviderUnavailableError(Exception):
    """Raised when a provider is unavailable (circuit open, auth failure, etc.)."""

    def __init__(self, message: str = "Provider is unavailable.", error: AIError | None = None):
        super().__init__(message)
        self.message = message
        self.error = error


class OutputValidationError(Exception):
    """Raised when AI output fails structured contract validation."""


@dataclass
class ModelSpec:
    """Full specification of a model in the unified model registry."""

    model_id: str
    provider_id: str
    display_name: str
    task_capabilities: list[TaskCapability] = field(default_factory=list)
    task_types: list[TaskType] = field(default_factory=list)
    context_window: int | None = None
    max_output_tokens: int | None = None
    streaming: bool = False
    pricing_class: PricingClass = PricingClass.UNKNOWN
    free_tier_status: FreeTierStatus = FreeTierStatus.UNKNOWN
    availability: AvailabilityStatus = AvailabilityStatus.ACTIVE
    documentation_url: str | None = None
    last_verification_date: str | None = None
    cost_per_input_token: float | None = None
    cost_per_output_token: float | None = None


@dataclass
class ProviderCredential:
    """Credential record for a provider (never exposes secret values)."""

    provider_id: str
    configured: bool
    key_last_four: str | None = None
    validation_status: str = "unknown"  # valid | invalid | untested | expired
    last_connection_test: str | None = None
    usage_status: str = "idle"  # idle | active | rate_limited | disabled
    provider_status: str = "unknown"  # healthy | degraded | down | unknown
    multiple_keys: bool = False
    key_count: int = 0

