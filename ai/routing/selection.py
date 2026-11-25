"""Model selection utilities.

Pure helper functions for scoring and ranking models during routing. Kept
separate so selection logic can be tested independently of the router.
"""

from __future__ import annotations

from ai import ModelSpec, PricingClass, TaskCapability


def score_model(
    spec: ModelSpec,
    require_free: bool = True,
    allow_paid: bool = False,
) -> float:
    """Score a model for routing suitability.

    Higher is better. Pure function of the model spec and constraints.
    """
    score = 0.0

    family = spec.model_id.lower()
    quality = 50
    for prefix, value in {
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
    }.items():
        if prefix in family:
            quality = value
            break
    score += quality

    if spec.free_tier_status == "permanent":
        score += 15
    elif spec.free_tier_status == "trial":
        score += 5

    if require_free and spec.free_tier_status != "permanent":
        score -= 100

    if spec.pricing_class == PricingClass.PAID and not allow_paid:
        score -= 100

    if spec.context_window:
        score += min(spec.context_window / 100000, 10)
    if spec.max_output_tokens:
        score += min(spec.max_output_tokens / 65536, 5)

    return score


def has_capability(spec: ModelSpec, capability: TaskCapability) -> bool:
    return capability in (spec.task_capabilities or [])


def estimate_max_cost_usd(spec: ModelSpec, max_output_tokens: int) -> Optional[float]:
    """Estimate max cost for a response given output token cap. None if price unknown."""
    if spec.cost_per_output_token is None:
        return None
    return spec.cost_per_output_token * max_output_tokens / 1_000_000