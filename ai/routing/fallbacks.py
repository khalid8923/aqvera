"""Fallback chain management.

Provides ordered fallback model chains for a task, ensuring that a fallback
supports the same task and preserves the expected response contract. Never
suggests incompatible fallbacks (e.g. a chat model for embeddings).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import TaskType
from ai.registry.model_registry import ModelRegistry
from ai.routing.model_router import ModelRouter, RoutingDecision


@dataclass
class FallbackChain:
    """An ordered chain of fallback models for a task."""

    task_type: TaskType
    primary: RoutingDecision
    fallbacks: list[RoutingDecision] = field(default_factory=list)

    def candidates(self) -> list[RoutingDecision]:
        return [self.primary] + self.fallbacks

    def next_after(self, model_id: str) -> Optional[RoutingDecision]:
        all_candidates = self.candidates()
        for i, cand in enumerate(all_candidates):
            if cand.model_id == model_id and i + 1 < len(all_candidates):
                return all_candidates[i + 1]
        return None


class FallbackManager:
    """Builds and manages fallback chains per task."""

    def __init__(self, registry: ModelRegistry, router: ModelRouter) -> None:
        self.registry = registry
        self.router = router

    def build_chain(
        self,
        task_type: TaskType,
        max_fallback: int = 3,
        user_id: Optional[str] = None,
        diagnostic: bool = False,
    ) -> FallbackChain:
        """Build a fallback chain for the given task.

        The primary is the best model; fallbacks are compatible models that
        support the same task type (never an embedding model for chat, etc.).
        """
        primary = self.router.select(
            task_type=task_type,
            user_id=user_id,
            diagnostic=diagnostic,
        )
        excluded = [primary.model_id]
        fallback_decisions = self.router.fallback_candidates(
            task_type=task_type,
            excluded=excluded,
            user_id=user_id,
            diagnostic=diagnostic,
        )
        fallbacks = fallback_decisions[:max_fallback]
        return FallbackChain(
            task_type=task_type,
            primary=primary,
            fallbacks=fallbacks,
        )