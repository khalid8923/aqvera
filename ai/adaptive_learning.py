"""Adaptive learning engine — deterministic, rule-based mastery estimation.

Tracks learning evidence and produces recommendations. AI never assigns mastery
scores; mastery comes from deterministic rules applied to structured evidence.

Core calculations are deterministic and testable without AI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import TaskType
from ai.orchestration import Orchestrator


# Mastery thresholds (deterministic, configurable).
MASTERY_THRESHOLD = 0.70
CONFIDENCE_THRESHOLD = 0.60
LEARNING_RATE_INITIAL = 0.20
DECAY_FACTOR = 0.98  # per day without interaction


@dataclass
class EvidenceRecord:
    objective_id: str
    evidence_type: str  # "correct_answer" | "incorrect_answer" | "partial" | "repeated_mistake" | ...
    strength: str  # "direct" | "behavioral"
    value: float  # 0.0 to 1.0
    item_difficulty: float = 0.5  # 0.0 easy to 1.0 hard
    timestamp: str | None = None


@dataclass
class KnowledgeState:
    objective_id: str
    estimated_mastery: float = 0.0
    confidence: float = 0.0
    evidence_count: int = 0
    recent_performance: list[float] = field(default_factory=list)
    repeated_misconceptions: list[str] = field(default_factory=list)
    last_interaction_at: str | None = None
    retention_review_status: str = "none"  # none | due | completed | overdue


@dataclass
class Recommendation:
    type: str  # "next_topic" | "review" | "advance" | "prerequisite" | "retention"
    target_objective_id: Optional[str] = None
    rationale: str = ""
    evidence_confidence: float = 0.0
    difficulty: Optional[str] = None


class AdaptiveEngine:
    """Deterministic adaptive learning engine.

    Public methods are pure functions of evidence; no AI involvement in
    mastery calculation.
    """

    def __init__(self, orchestrator: Orchestrator | None = None) -> None:
        self.orchestrator = orchestrator
        self._states: dict[str, KnowledgeState] = {}

    def get_state(self, objective_id: str) -> KnowledgeState:
        if objective_id not in self._states:
            self._states[objective_id] = KnowledgeState(objective_id=objective_id)
        return self._states[objective_id]

    def record_evidence(self, evidence: EvidenceRecord) -> KnowledgeState:
        """Apply a new evidence record to a knowledge state (deterministic)."""
        state = self.get_state(evidence.objective_id)
        signal = self._signal_value(evidence)
        weight = self._evidence_weight(evidence)

        # Incremental mastery update: mastery_new = mastery + lr * (signal - mastery)
        learning_rate = LEARNING_RATE_INITIAL / (1.0 + 0.1 * state.evidence_count)
        state.estimated_mastery = max(
            0.0,
            min(1.0, state.estimated_mastery + learning_rate * weight * (signal - state.estimated_mastery)),
        )

        state.evidence_count += 1
        state.recent_performance.append(signal)
        if len(state.recent_performance) > 10:
            state.recent_performance = state.recent_performance[-10:]

        # Confidence grows with evidence count and consistency.
        consistency = 1.0 - self._stddev(state.recent_performance)
        state.confidence = max(0.0, min(1.0, min(1.0, state.evidence_count / 10.0) * max(0.0, consistency)))

        if evidence.evidence_type == "repeated_mistake" and evidence.value > 0.5:
            if evidence.objective_id not in state.repeated_misconceptions:
                state.repeated_misconceptions.append(evidence.objective_id)

        state.last_interaction_at = evidence.timestamp
        return state

    def recommend_next(
        self,
        objective_id: str,
        prerequisite_mastery: dict[str, float] | None = None,
    ) -> Recommendation:
        """Determine the next step for an objective (deterministic pipeline)."""
        state = self.get_state(objective_id)
        prereqs = prerequisite_mastery or {}

        # 1. Evidence sufficiency check.
        if state.evidence_count < 3:
            return Recommendation(
                type="review",
                target_objective_id=objective_id,
                rationale=(
                    f"Not enough evidence ({state.evidence_count} records) for a "
                    "reliable judgment. Recommend more practice/assessment."
                ),
                evidence_confidence=state.confidence,
            )

        # 2. Prerequisite check.
        unmastered = [pid for pid, m in prereqs.items() if m < MASTERY_THRESHOLD]
        if unmastered:
            return Recommendation(
                type="prerequisite",
                target_objective_id=unmastered[0],
                rationale=(
                    f"Prerequisite {unmastered[0]} is not mastered "
                    f"(mastery {prereqs[unmastered[0]]:.2f} < {MASTERY_THRESHOLD}). "
                    "Review prerequisite before advancing."
                ),
                evidence_confidence=state.confidence,
            )

        # 3. Mastery threshold check.
        if state.estimated_mastery >= MASTERY_THRESHOLD and state.confidence >= CONFIDENCE_THRESHOLD:
            return Recommendation(
                type="advance",
                target_objective_id=None,
                rationale=(
                    f"Objective mastered (mastery {state.estimated_mastery:.2f}, "
                    f"confidence {state.confidence:.2f}). Advance to next objective."
                ),
                evidence_confidence=state.confidence,
                difficulty="hard",
            )

        # 4. Review / adjust difficulty.
        difficulty = self._select_difficulty(state)
        return Recommendation(
            type="review",
            target_objective_id=objective_id,
            rationale=(
                f"Objective not yet mastered (mastery {state.estimated_mastery:.2f} "
                f"< {MASTERY_THRESHOLD}). Review at {difficulty} difficulty."
            ),
            evidence_confidence=state.confidence,
            difficulty=difficulty,
        )

    def detect_weak_topics(self, states: dict[str, KnowledgeState]) -> list[str]:
        """Return objective IDs below mastery threshold."""
        return [
            oid for oid, s in states.items()
            if s.estimated_mastery < MASTERY_THRESHOLD
        ]

    def schedule_retention(self, objective_id: str) -> str:
        """Return retention review status for a recently mastered objective."""
        state = self.get_state(objective_id)
        if state.estimated_mastery >= MASTERY_THRESHOLD:
            return "due"
        return "none"

    # --- Internal deterministic helpers ---

    @staticmethod
    def _signal_value(evidence: EvidenceRecord) -> float:
        mapping = {
            "correct_answer": 1.0,
            "incorrect_answer": 0.0,
            "partial": 0.5,
            "repeated_mistake": 0.0,
        }
        base = mapping.get(evidence.evidence_type, 0.5)
        # Harder items correct => stronger signal; easier items incorrect => stronger negative.
        if evidence.evidence_type == "correct_answer":
            base = 0.5 + 0.5 * evidence.item_difficulty
        elif evidence.evidence_type == "incorrect_answer":
            base = 0.5 * (1.0 - evidence.item_difficulty)
        return max(0.0, min(1.0, base))

    @staticmethod
    def _evidence_weight(evidence: EvidenceRecord) -> float:
        return 1.0 if evidence.strength == "direct" else 0.4

    @staticmethod
    def _select_difficulty(state: KnowledgeState) -> str:
        if state.estimated_mastery < 0.3:
            return "easy"
        if state.estimated_mastery < 0.6:
            return "medium"
        return "hard"

    @staticmethod
    def _stddev(values: list[float]) -> float:
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / len(values)
        return var ** 0.5
