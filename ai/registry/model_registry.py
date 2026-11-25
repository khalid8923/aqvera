"""Unified model registry.

AQVERA maintains a single source of truth for all available models across all
providers. The registry is provider-agnostic and does not depend on any one
provider's internal model identifiers remaining permanent.

Models can be registered statically (from provider documentation) or refreshed
from provider model-list endpoints when available. Disabled and deprecated
models are supported without crashing the system.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from ai import (
    AvailabilityStatus,
    FreeTierStatus,
    ModelCapability,
    ModelSpec,
    PricingClass,
    TaskCapability,
    TaskType,
)
from ai.registry.capability import CapabilityIndex, register_for_scoring, unregister_for_scoring


class ModelRegistry:
    """Unified model registry with capability discovery.

    Stores ModelSpec entries keyed by model_id. Provides lookups by provider,
    capability, task type, pricing class, and availability.
    """

    def __init__(self) -> None:
        self._models: dict[str, ModelSpec] = {}
        self._by_provider: dict[str, list[str]] = {}
        self._capability_index = CapabilityIndex()
        self._last_refreshed: Optional[str] = None

    # ------------------------------------------------------------------ #
    # Registration
    # ------------------------------------------------------------------ #

    def register(self, spec: ModelSpec) -> None:
        """Register or update a model specification."""
        self._models[spec.model_id] = spec
        self._by_provider.setdefault(spec.provider_id, [])
        if spec.model_id not in self._by_provider[spec.provider_id]:
            self._by_provider[spec.provider_id].append(spec.model_id)
        self._capability_index.add(spec)
        register_for_scoring(spec)

    def register_many(self, specs: list[ModelSpec]) -> None:
        for spec in specs:
            self.register(spec)

    def unregister(self, model_id: str) -> bool:
        """Remove a model from the registry. Returns True if removed."""
        spec = self._models.pop(model_id, None)
        if spec is None:
            return False
        provider_models = self._by_provider.get(spec.provider_id, [])
        if model_id in provider_models:
            provider_models.remove(model_id)
        self._capability_index.remove(spec)
        unregister_for_scoring(model_id)
        return True

    # ------------------------------------------------------------------ #
    # Lookup
    # ------------------------------------------------------------------ #

    def get(self, model_id: str) -> Optional[ModelSpec]:
        return self._models.get(model_id)

    def list_models(
        self,
        provider_id: Optional[str] = None,
        active_only: bool = True,
        capability: Optional[TaskCapability] = None,
        task_type: Optional[TaskType] = None,
        pricing_class: Optional[PricingClass] = None,
        free_tier_status: Optional[FreeTierStatus] = None,
        availability: Optional[AvailabilityStatus] = None,
    ) -> list[ModelSpec]:
        """List models matching the given filters."""
        results = list(self._models.values())

        if provider_id is not None:
            results = [m for m in results if m.provider_id == provider_id]

        if active_only:
            results = [m for m in results if m.availability == AvailabilityStatus.ACTIVE]

        if capability is not None:
            results = [m for m in results if capability in m.task_capabilities]

        if task_type is not None:
            results = [m for m in results if task_type in m.task_types]

        if pricing_class is not None:
            results = [m for m in results if m.pricing_class == pricing_class]

        if free_tier_status is not None:
            results = [m for m in results if m.free_tier_status == free_tier_status]

        if availability is not None:
            results = [m for m in results if m.availability == availability]

        results.sort(key=lambda m: (m.provider_id, m.display_name))
        return results

    def list_providers(self) -> list[str]:
        return sorted(self._by_provider.keys())

    def models_for_provider(self, provider_id: str) -> list[ModelSpec]:
        return [self._models[mid] for mid in self._by_provider.get(provider_id, []) if mid in self._models]

    # ------------------------------------------------------------------ #
    # Capability discovery
    # ------------------------------------------------------------------ #

    def find_for_task(self, task_type: TaskType) -> list[ModelSpec]:
        """Return active models capable of the given task type, ordered by
        capability index score (quality/latency/availability heuristics)."""
        return self._capability_index.find_for_task(task_type)

    def has_capability(self, model_id: str, capability: TaskCapability) -> bool:
        spec = self._models.get(model_id)
        if spec is None:
            return False
        return capability in spec.task_capabilities

    def supports_task(self, model_id: str, task_type: TaskType) -> bool:
        spec = self._models.get(model_id)
        if spec is None:
            return False
        return task_type in spec.task_types

    # ------------------------------------------------------------------ #
    # Refresh
    # ------------------------------------------------------------------ #

    def set_last_refreshed(self, timestamp: Optional[str] = None) -> None:
        if timestamp is None:
            timestamp = datetime.now(timezone.utc).isoformat()
        self._last_refreshed = timestamp

    def last_refreshed(self) -> Optional[str]:
        return self._last_refreshed

    def count(self) -> int:
        return len(self._models)

    def count_active(self) -> int:
        return sum(1 for m in self._models.values() if m.availability == AvailabilityStatus.ACTIVE)