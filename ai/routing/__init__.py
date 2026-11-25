"""Task-based model routing package."""

from ai.routing.fallbacks import FallbackChain, FallbackManager
from ai.routing.legacy import Router
from ai.routing.model_router import ModelRouter, RoutingDecision
from ai.routing.selection import estimate_max_cost_usd, has_capability, score_model
from ai.routing.task_policies import RoutingPolicy, TaskPolicyRegistry

__all__ = [
    "ModelRouter",
    "Router",
    "RoutingDecision",
    "FallbackChain",
    "FallbackManager",
    "RoutingPolicy",
    "TaskPolicyRegistry",
    "score_model",
    "has_capability",
    "estimate_max_cost_usd",
]
