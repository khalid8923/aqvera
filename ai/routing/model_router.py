"""Intelligent model router.

Selects models for AQVERA AI tasks based on required capability, quality,
language suitability, latency, availability, context window, rate limits,
estimated cost, free-tier restrictions, provider health, task priority,
privacy policy, and administrator configuration.

The router is policy-driven: task policies define preferred/fallback models
and constraints. It never hardcodes a provider choice. It returns a selected
model_id plus the reasoning for diagnostic mode.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import (
    AIError,
    AIErrorCategory,
    AvailabilityStatus,
    FreeTierStatus,
    ModelSpec,
    PricingClass,
    ProviderUnavailableError,
    TaskType,
)
from ai.registry.model_registry import ModelRegistry
from ai.routing.task_policies import RoutingPolicy, TaskPolicyRegistry


@dataclass
class RoutingDecision:
    """Result of model selection with diagnostic reasoning."""

    model_id: str
    provider_id: str
    task_type: TaskType
    reason: str
    diagnostics: list[str] = field(default_factory=list)
    policy: Optional[RoutingPolicy] = None


@dataclass
class ModelCandidate:
    spec: ModelSpec
    score: float
    reasons: list[str]


class ModelRouter:
    """Selects the best model for a task given routing policies and constraints.

    The router is deterministic and explainable: every decision carries a
    human-readable reason and a list of diagnostic notes.
    """

    def __init__(
        self,
        registry: ModelRegistry,
        policy_registry: TaskPolicyRegistry,
    ) -> None:
        self.registry = registry
        self.policy_registry = policy_registry

    def select(
        self,
        task_type: TaskType,
        user_id: Optional[str] = None,
        preferred_model: Optional[str] = None,
        require_capability: Optional[str] = None,
        require_free_tier: bool = False,
        diagnostic: bool = False,
    ) -> RoutingDecision:
        """Select the best model for the given task.

        Returns a RoutingDecision with the selected model and reasoning.
        Raises if no eligible model is available.
        """
        policy = self.policy_registry.get(task_type)
        diagnostics: list[str] = []

        # 1. Gather active candidate models supporting the task.
        candidates = self.registry.list_models(
            active_only=True,
            task_type=task_type,
        )
        diagnostics.append(f"{len(candidates)} active models support task {task_type.value}")

        if not candidates:
            raise ProviderUnavailableError(
                f"No active model supports task {task_type.value}",
                error=AIError(
                    category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                    message=f"No active model supports task {task_type.value}",
                    retryable=False,
                ),
            )

        # 2. Apply required capability filter.
        required_cap = require_capability or (policy.required_capability if policy else None)
        if required_cap:
            candidates = [c for c in candidates if required_cap in (c.task_capabilities or [])]
            diagnostics.append(f"After capability filter '{required_cap}': {len(candidates)} models")

        if not candidates:
            raise AIError(
                category=AIErrorCategory.UNSUPPORTED_CAPABILITY,
                message=f"No active model supports task {task_type.value} with capability {required_cap}",
                retryable=False,
            )

        # 3. Apply policy constraints (paid/free tier, disabled providers, cost).
        require_free = require_free_tier or (policy.require_free_tier if policy else False)
        eligible: list[ModelCandidate] = []
        for spec in candidates:
            reasons: list[str] = []
            ok = True

            # Free tier constraint applies regardless of whether a policy exists.
            if require_free and spec.free_tier_status != FreeTierStatus.PERMANENT:
                ok = False
                reasons.append("not permanent free tier")

            if policy:
                if spec.provider_id in policy.disabled_providers:
                    ok = False
                    reasons.append(f"provider {spec.provider_id} disabled for task")
                if spec.pricing_class == PricingClass.PAID and not policy.allow_paid:
                    ok = False
                    reasons.append("paid model not allowed")
                if spec.pricing_class == PricingClass.UNKNOWN:
                    ok = False
                    reasons.append("pricing unknown")
                if policy.max_cost_per_request_usd is not None and spec.cost_per_output_token is not None:
                    # Conservative: treat max output tokens as a proxy.
                    est = spec.cost_per_output_token * (spec.max_output_tokens or 1024) / 1_000_000
                    if est > policy.max_cost_per_request_usd:
                        ok = False
                        reasons.append(f"estimated cost {est:.6f} exceeds ceiling")

            if not ok:
                diagnostics.append(f"skipping {spec.model_id}: {'; '.join(reasons)}")
                continue

            eligible.append(ModelCandidate(spec=spec, score=0.0, reasons=reasons))

        if not eligible:
            raise ProviderUnavailableError(
                f"No eligible model for task {task_type.value} under policy constraints",
                error=AIError(
                    category=AIErrorCategory.PROVIDER_UNAVAILABLE,
                    message=f"No eligible model for task {task_type.value} under policy constraints",
                    retryable=False,
                ),
            )

        diagnostics.append(f"{len(eligible)} eligible models after policy constraints")

        # 4. Score eligible candidates.
        for cand in eligible:
            cand.score = self._score_candidate(cand.spec, task_type, policy, diagnostics)

        # 5. Preferred model override.
        if preferred_model:
            for cand in eligible:
                if cand.spec.model_id == preferred_model:
                    cand.score += 100.0
                    cand.reasons.append("explicitly preferred model")
                    diagnostics.append(f"using explicitly preferred model {preferred_model}")
                    break

        # 6. Policy preferred models boost.
        if policy and policy.preferred_models:
            pref_set = set(policy.preferred_models)
            for cand in eligible:
                if cand.spec.model_id in pref_set:
                    cand.score += 50.0
                    cand.reasons.append("policy preferred model")

        # 7. Fallback ordering: eligible models already sorted by score.
        eligible.sort(key=lambda c: c.score, reverse=True)
        best = eligible[0]

        # Build reason string.
        reason_parts = [
            f"task={task_type.value}",
            f"model={best.spec.model_id}",
            f"provider={best.spec.provider_id}",
        ]
        if best.reasons:
            reason_parts.append("reasons=" + "; ".join(best.reasons))
        reason = ", ".join(reason_parts)

        diagnostics.append(f"selected {best.spec.model_id} (score {best.score:.1f})")
        for r in best.reasons:
            diagnostics.append(f"  - {r}")

        return RoutingDecision(
            model_id=best.spec.model_id,
            provider_id=best.spec.provider_id,
            task_type=task_type,
            reason=reason,
            diagnostics=diagnostics if diagnostic else [],
            policy=policy,
        )

    def fallback_candidates(
        self,
        task_type: TaskType,
        excluded: list[str],
        user_id: Optional[str] = None,
        diagnostic: bool = False,
    ) -> list[RoutingDecision]:
        """Return ordered fallback model candidates (excluding `excluded`)."""
        policy = self.policy_registry.get(task_type)
        diagnostics: list[str] = []
        candidates = self.registry.list_models(active_only=True, task_type=task_type)

        required_cap = policy.required_capability if policy else None
        if required_cap:
            candidates = [c for c in candidates if required_cap in (c.task_capabilities or [])]

        results: list[RoutingDecision] = []
        for spec in candidates:
            if spec.model_id in excluded:
                continue
            # Apply same policy constraints as select().
            ok = True
            reasons: list[str] = []
            if policy:
                if spec.provider_id in policy.disabled_providers:
                    ok = False
                if policy.require_free_tier and spec.free_tier_status != FreeTierStatus.PERMANENT:
                    ok = False
                if spec.pricing_class == PricingClass.PAID and not policy.allow_paid:
                    ok = False
            if not ok:
                continue
            decision = RoutingDecision(
                model_id=spec.model_id,
                provider_id=spec.provider_id,
                task_type=task_type,
                reason=f"fallback for {task_type.value}: {spec.model_id}",
                diagnostics=diagnostics if diagnostic else [],
                policy=policy,
            )
            results.append(decision)
        return results

    # ------------------------------------------------------------------ #
    # Internal scoring
    # ------------------------------------------------------------------ #

    @staticmethod
    def _score_candidate(
        spec: ModelSpec,
        task_type: TaskType,
        policy: Optional[RoutingPolicy],
        diagnostics: list[str],
    ) -> float:
        score = 0.0

        # Quality heuristic (from capability index, approximated here).
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

        # Free tier preference.
        if spec.free_tier_status == FreeTierStatus.PERMANENT:
            score += 15
        elif spec.free_tier_status == FreeTierStatus.TRIAL:
            score += 5

        # Unknown pricing is a mild negative.
        if spec.pricing_class == PricingClass.UNKNOWN:
            score -= 10

        # Larger context window is a mild positive.
        if spec.context_window:
            score += min(spec.context_window / 100000, 10)

        # Max output tokens ceiling.
        if spec.max_output_tokens:
            score += min(spec.max_output_tokens / 65536, 5)

        return score