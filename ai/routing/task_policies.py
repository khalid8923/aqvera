"""Task-based routing policies.

Each AQVERA AI task type has a routing policy that defines which providers and
models are preferred, which are fallbacks, cost limits, timeouts, and privacy
constraints. Policies are configurable by administrators and are not hardcoded
provider choices.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import TaskType


@dataclass
class RoutingPolicy:
    """Routing policy for a single task type.

    Attributes:
        task_type: The task this policy governs.
        preferred_models: Ordered list of preferred model_ids.
        fallback_models: Ordered list of fallback model_ids (used if preferred fail).
        required_capability: Capability that a model MUST have (e.g. vision).
        max_cost_per_request_usd: Hard cost ceiling per request (None = no limit).
        max_tokens: Maximum output tokens.
        timeout_ms: Request timeout in milliseconds.
        max_retries: Maximum retry attempts.
        allow_paid: Whether paid providers may be used (default False).
        require_free_tier: Whether only free-tier models may be used.
        privacy_policy: Privacy constraint string (e.g. "no-external-provider").
        preferred_providers: Ordered list of preferred provider_ids.
        disabled_providers: Provider IDs that must not be used for this task.
    """

    task_type: TaskType
    preferred_models: list[str] = field(default_factory=list)
    fallback_models: list[str] = field(default_factory=list)
    required_capability: Optional[str] = None
    max_cost_per_request_usd: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout_ms: int = 30000
    max_retries: int = 3
    allow_paid: bool = False
    require_free_tier: bool = True
    privacy_policy: Optional[str] = None
    preferred_providers: list[str] = field(default_factory=list)
    disabled_providers: list[str] = field(default_factory=list)


class TaskPolicyRegistry:
    """Holds routing policies keyed by task type.

    Administrators can define preferences per task. Policies are consulted by
    the model router when selecting a model.
    """

    def __init__(self) -> None:
        self._policies: dict[TaskType, RoutingPolicy] = {}
        self._defaults: dict[TaskType, RoutingPolicy] = {}

    def set(self, policy: RoutingPolicy) -> None:
        self._policies[policy.task_type] = policy

    def get(self, task_type: TaskType) -> Optional[RoutingPolicy]:
        return self._policies.get(task_type) or self._defaults.get(task_type)

    def set_default(self, task_type: TaskType, policy: RoutingPolicy) -> None:
        self._defaults[task_type] = policy

    def list_tasks(self) -> list[TaskType]:
        return sorted(
            set(self._policies.keys()) | set(self._defaults.keys()),
            key=lambda t: t.value,
        )

    def remove(self, task_type: TaskType) -> bool:
        return self._policies.pop(task_type, None) is not None