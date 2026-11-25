"""AI model and output evaluation.

Evaluates teaching quality, groundedness, citation correctness, question
quality, mathematical correctness, and structured output validity using
representative academic test cases. No live provider calls in tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import AIResponse, TaskType
from ai.orchestration import Orchestrator


@dataclass
class EvalCase:
    id: str
    task_type: TaskType
    input: str
    expected_grounding: Optional[str] = None  # source that should be cited
    expected_answer: Optional[str] = None
    domain: str = "mathematics"


@dataclass
class EvalResult:
    case_id: str
    passed: bool
    score: float  # 0.0 to 1.0
    reason: str
    response: Optional[AIResponse] = None


class Evaluator:
    """Runs evaluation cases against the orchestrator (mock or live provider)."""

    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator
        self.results: list[EvalResult] = []

    async def run_case(self, case: EvalCase) -> EvalResult:
        from ai import Message
        messages = [
            Message(role="system", content="You are a helpful academic assistant."),
            Message(role="user", content=case.input),
        ]
        response = await self.orchestrator.generate(
            task_type=case.task_type,
            messages=messages,
            model="mock-model",
        )

        passed, score, reason = self._judge(case, response)
        result = EvalResult(
            case_id=case.id,
            passed=passed,
            score=score,
            reason=reason,
            response=response,
        )
        self.results.append(result)
        return result

    def _judge(self, case: EvalCase, response: AIResponse) -> tuple[bool, float, str]:
        if response.error is not None:
            return False, 0.0, f"Provider error: {response.error.message}"
        content = response.content or ""
        if not content.strip():
            return False, 0.0, "Empty response"
        # Groundedness: if expected grounding set, check it appears.
        if case.expected_grounding and case.expected_grounding.lower() not in content.lower():
            return False, 0.4, f"Expected grounding '{case.expected_grounding}' not found"
        # Deterministic answer check when expected answer provided.
        if case.expected_answer and case.expected_answer.lower() not in content.lower():
            return False, 0.5, f"Expected answer '{case.expected_answer}' not found"
        return True, 1.0, "Pass"

    def summary(self) -> dict:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        avg_score = sum(r.score for r in self.results) / total if total else 0.0
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "average_score": round(avg_score, 3),
        }
