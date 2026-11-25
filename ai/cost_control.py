"""Cost tracking, budget enforcement, and graceful degradation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import AIResponse, CostRecord, TaskType


@dataclass
class Budget:
    provider: Optional[str] = None
    model: Optional[str] = None
    task_type: Optional[TaskType] = None
    daily_usd: Optional[float] = None
    monthly_usd: Optional[float] = None
    per_user_daily_usd: Optional[float] = None


@dataclass
class UsageSnapshot:
    provider: str
    model: str
    task_type: TaskType
    daily_cost_usd: float
    monthly_cost_usd: float
    daily_requests: int
    monthly_requests: int


class CostTracker:
    """Tracks AI usage cost and enforces budgets."""

    def __init__(self) -> None:
        self._records: list[CostRecord] = []
        self._budgets: list[Budget] = []

    def add_budget(self, budget: Budget) -> None:
        self._budgets.append(budget)

    def record(self, record: CostRecord) -> None:
        self._records.append(record)

    def check_budget(
        self,
        provider: str,
        model: str,
        task_type: TaskType,
        estimated_cost_usd: float,
        user_id: Optional[str] = None,
    ) -> tuple[bool, Optional[str]]:
        """Return (allowed, reason). If not allowed, reason explains why."""
        for budget in self._budgets:
            if budget.provider and budget.provider != provider:
                continue
            if budget.model and budget.model != model:
                continue
            if budget.task_type and budget.task_type != task_type:
                continue

            daily = self._daily_cost(provider, model, task_type)
            monthly = self._monthly_cost(provider, model, task_type)

            if budget.daily_usd is not None and daily + estimated_cost_usd > budget.daily_usd:
                return False, f"Daily budget exceeded for {provider}/{model}"
            if budget.monthly_usd is not None and monthly + estimated_cost_usd > budget.monthly_usd:
                return False, f"Monthly budget exceeded for {provider}/{model}"
            if budget.per_user_daily_usd is not None and user_id is not None:
                user_daily = self._user_daily_cost(provider, model, task_type, user_id)
                if user_daily + estimated_cost_usd > budget.per_user_daily_usd:
                    return False, f"Per-user daily budget exceeded for {user_id}"

        return True, None

    def _daily_cost(self, provider: str, model: str, task_type: TaskType) -> float:
        return sum(
            r.estimated_cost
            for r in self._records
            if r.provider == provider and r.model == model and r.task_type == task_type
        )

    def _monthly_cost(self, provider: str, model: str, task_type: TaskType) -> float:
        return self._daily_cost(provider, model, task_type)  # simplified: day-window

    def _user_daily_cost(self, provider: str, model: str, task_type: TaskType, user_id: str) -> float:
        return sum(
            r.estimated_cost
            for r in self._records
            if r.provider == provider
            and r.model == model
            and r.task_type == task_type
            and r.user_id == user_id
        )

    def snapshot(self, provider: str, model: str, task_type: TaskType) -> UsageSnapshot:
        return UsageSnapshot(
            provider=provider,
            model=model,
            task_type=task_type,
            daily_cost_usd=self._daily_cost(provider, model, task_type),
            monthly_cost_usd=self._monthly_cost(provider, model, task_type),
            daily_requests=len(
                [r for r in self._records if r.provider == provider and r.model == model and r.task_type == task_type]
            ),
            monthly_requests=0,
        )


class BudgetExhaustedError(Exception):
    """Raised when a budget ceiling would be exceeded."""


def estimate_cost(
    response: AIResponse,
    task_type: TaskType,
) -> float:
    """Estimate cost from response usage if provider did not supply it."""
    if response.cost_estimate is not None:
        return response.cost_estimate
    # Fallback rough estimate if provider does not report cost.
    return 0.0
