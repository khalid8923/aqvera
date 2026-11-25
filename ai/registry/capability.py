"""Capability index for the model registry.

Provides fast lookup of models by task type and capability, with a simple
scoring heuristic to rank models for a given task.
"""

from __future__ import annotations

from typing import Optional

from ai import (
    AvailabilityStatus,
    FreeTierStatus,
    ModelSpec,
    PricingClass,
    TaskCapability,
    TaskType,
)

# Simple quality heuristic by model family prefix. Higher = preferred.
_FAMILY_QUALITY = {
    "nemotron": 90,
    "gpt-oss": 85,
    "claude": 85,
    "gemini": 80,
    "qwen": 78,
    "llama": 75,
    "mistral": 75,
    "deepseek": 72,
    "glm": 70,
    "mock": 50,
}

_FREE_BONUS = 10


class CapabilityIndex:
    """In-memory index mapping task types/capabilities to model IDs."""

    def __init__(self) -> None:
        self._by_task: dict[str, list[str]] = {}
        self._by_capability: dict[str, list[str]] = {}

    def add(self, spec: ModelSpec) -> None:
        for task in spec.task_types:
            self._by_task.setdefault(task.value, [])
            if spec.model_id not in self._by_task[task.value]:
                self._by_task[task.value].append(spec.model_id)
        for cap in spec.task_capabilities:
            self._by_capability.setdefault(cap.value, [])
            if spec.model_id not in self._by_capability[cap.value]:
                self._by_capability[cap.value].append(spec.model_id)

    def remove(self, spec: ModelSpec) -> None:
        for task in spec.task_types:
            bucket = self._by_task.get(task.value, [])
            if spec.model_id in bucket:
                bucket.remove(spec.model_id)
        for cap in spec.task_capabilities:
            bucket = self._by_capability.get(cap.value, [])
            if spec.model_id in bucket:
                bucket.remove(spec.model_id)

    def find_for_task(self, task_type: TaskType) -> list[ModelSpec]:
        """Return models for a task, scored and sorted.

        This is a heuristic ranking used by the router as a starting point;
        the router applies its own policy (cost, latency, budget, provider
        health) on top.
        """
        ids = self._by_task.get(task_type.value, [])
        scored = []
        for mid in ids:
            spec = _MODEL_STORE.get(mid)
            if spec is None:
                continue
            score = self._score(spec)
            scored.append((score, spec))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [spec for _, spec in scored]

    @staticmethod
    def _score(spec: ModelSpec) -> float:
        score = 0.0
        family = spec.model_id.lower()
        for prefix, value in _FAMILY_QUALITY.items():
            if prefix in family:
                score += value
                break
        if spec.pricing_class == "free":
            score += _FREE_BONUS
        if spec.free_tier_status == "permanent":
            score += 5
        if spec.availability == "active":
            score += 5
        if spec.context_window:
            score += min(spec.context_window / 100000, 10)
        return score


# Module-level store referenced by CapabilityIndex for scoring lookups.
_MODEL_STORE: dict[str, ModelSpec] = {}


def register_for_scoring(spec: ModelSpec) -> None:
    _MODEL_STORE[spec.model_id] = spec


def unregister_for_scoring(model_id: str) -> None:
    _MODEL_STORE.pop(model_id, None)


def get_for_scoring(model_id: str) -> Optional[ModelSpec]:
    return _MODEL_STORE.get(model_id)