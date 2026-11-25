"""Orchestration task types and schemas.

Each AQVERA AI task defines:
- Input schema
- Output schema
- Required capability
- Preferred model policy
- Fallback policy
- Cost policy
- Timeout
- Validation rules

These are provider-agnostic contracts. The orchestration layer coordinates
provider adapters to fulfill tasks without knowing provider internals.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import TaskType, TaskCapability


# --------------------------------------------------------------------------- #
# Task input/output schemas
# --------------------------------------------------------------------------- #

@dataclass
class TaskInput:
    """Generic input for an AI task."""

    task_type: TaskType
    text: Optional[str] = None
    messages: Optional[list[dict]] = None  # {role, content}
    sources: list[str] = field(default_factory=list)
    language: str = "en"
    difficulty: str = "intermediate"
    course_id: Optional[str] = None
    lesson_id: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    # Multimedia inputs (optional, capability-dependent)
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    video_path: Optional[str] = None

    def require_text(self) -> str:
        if self.text is None:
            raise ValueError(f"Task {self.task_type.value} requires text input")
        return self.text


@dataclass
class TaskOutput:
    """Generic output from an AI task."""

    task_type: TaskType
    content: str
    structured: Optional[dict] = None
    sources: list[dict] = field(default_factory=list)
    evidence_type: Optional[str] = None  # source | external | inference | uncertain
    model_id: Optional[str] = None
    provider_id: Optional[str] = None
    latency_ms: int = 0
    usage: Optional[dict] = None
    cost_estimate: Optional[float] = None
    error: Optional[str] = None


# --------------------------------------------------------------------------- #
# Task definitions
# --------------------------------------------------------------------------- #

@dataclass
class TaskDefinition:
    """Definition of an AI task: contract and routing/cost policy."""

    task_type: TaskType
    input_schema: str  # JSON schema identifier
    output_schema: str
    required_capability: Optional[TaskCapability] = None
    preferred_models: list[str] = field(default_factory=list)
    fallback_models: list[str] = field(default_factory=list)
    max_cost_per_request_usd: Optional[float] = None
    max_output_tokens: Optional[int] = None
    timeout_ms: int = 30000
    max_retries: int = 3
    allow_paid: bool = False
    require_free_tier: bool = True
    privacy_policy: Optional[str] = None
    validation_rules: list[str] = field(default_factory=list)

    def to_policy(self):
        from ai.routing.task_policies import RoutingPolicy
        return RoutingPolicy(
            task_type=self.task_type,
            preferred_models=list(self.preferred_models),
            fallback_models=list(self.fallback_models),
            required_capability=self.required_capability.value if self.required_capability else None,
            max_cost_per_request_usd=self.max_cost_per_request_usd,
            max_tokens=self.max_output_tokens,
            timeout_ms=self.timeout_ms,
            max_retries=self.max_retries,
            allow_paid=self.allow_paid,
            require_free_tier=self.require_free_tier,
            privacy_policy=self.privacy_policy,
        )


# --------------------------------------------------------------------------- #
# Built-in task registry
# --------------------------------------------------------------------------- #

TASK_DEFINITIONS: dict[TaskType, TaskDefinition] = {}


def register_task(definition: TaskDefinition) -> None:
    TASK_DEFINITIONS[definition.task_type] = definition


def get_task(task_type: TaskType) -> Optional[TaskDefinition]:
    return TASK_DEFINITIONS.get(task_type)


# Register default task definitions.

register_task(
    TaskDefinition(
        task_type=TaskType.CHAT,
        input_schema="chat.input.v1",
        output_schema="chat.output.v1",
        required_capability=TaskCapability.TEXT,
        preferred_models=[],
        fallback_models=[],
        max_cost_per_request_usd=None,
        max_output_tokens=1024,
        timeout_ms=30000,
        max_retries=3,
        allow_paid=False,
        require_free_tier=True,
        privacy_policy=None,
    )
)

register_task(
    TaskDefinition(
        task_type=TaskType.TUTOR_EXPLANATION,
        input_schema="tutor.input.v1",
        output_schema="tutor.output.v1",
        required_capability=TaskCapability.TEXT,
        max_output_tokens=1536,
        timeout_ms=30000,
        max_retries=3,
        allow_paid=False,
        require_free_tier=True,
    )
)

register_task(
    TaskDefinition(
        task_type=TaskType.EMBEDDING,
        input_schema="embedding.input.v1",
        output_schema="embedding.output.v1",
        required_capability=TaskCapability.EMBEDDING,
        max_output_tokens=None,
        timeout_ms=60000,
        max_retries=2,
        allow_paid=False,
        require_free_tier=True,
    )
)

register_task(
    TaskDefinition(
        task_type=TaskType.IMAGE_UNDERSTANDING,
        input_schema="image.input.v1",
        output_schema="image.output.v1",
        required_capability=TaskCapability.VISION,
        max_output_tokens=1024,
        timeout_ms=60000,
        max_retries=2,
        allow_paid=False,
        require_free_tier=True,
    )
)

register_task(
    TaskDefinition(
        task_type=TaskType.IMAGE_GENERATION,
        input_schema="image_gen.input.v1",
        output_schema="image_gen.output.v1",
        required_capability=TaskCapability.IMAGE_GENERATION,
        max_output_tokens=None,
        timeout_ms=120000,
        max_retries=1,
        allow_paid=False,
        require_free_tier=True,
    )
)

register_task(
    TaskDefinition(
        task_type=TaskType.SPEECH_TO_TEXT,
        input_schema="stt.input.v1",
        output_schema="stt.output.v1",
        required_capability=TaskCapability.AUDIO_INPUT,
        max_output_tokens=None,
        timeout_ms=120000,
        max_retries=2,
        allow_paid=False,
        require_free_tier=True,
    )
)

register_task(
    TaskDefinition(
        task_type=TaskType.TEXT_TO_SPEECH,
        input_schema="tts.input.v1",
        output_schema="tts.output.v1",
        required_capability=TaskCapability.AUDIO_OUTPUT,
        max_output_tokens=None,
        timeout_ms=120000,
        max_retries=2,
        allow_paid=False,
        require_free_tier=True,
    )
)

register_task(
    TaskDefinition(
        task_type=TaskType.RERANK,
        input_schema="rerank.input.v1",
        output_schema="rerank.output.v1",
        required_capability=None,
        max_output_tokens=None,
        timeout_ms=30000,
        max_retries=2,
        allow_paid=False,
        require_free_tier=True,
    )
)

register_task(
    TaskDefinition(
        task_type=TaskType.WEB_RESEARCH,
        input_schema="web_research.input.v1",
        output_schema="web_research.output.v1",
        required_capability=TaskCapability.WEB_SEARCH,
        max_output_tokens=1024,
        timeout_ms=30000,
        max_retries=2,
        allow_paid=False,
        require_free_tier=True,
    )
)