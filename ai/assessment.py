"""Assessment module: question generation, evaluation, grading.

Deterministic grading where possible (MCQ, numerical). AI grading only with
explicit criteria and transparent uncertainty. Questions validated before use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from ai import TaskType
from ai.orchestration import Orchestrator


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_SELECT = "multiple_select"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    NUMERICAL = "numerical"
    MATH_EXPRESSION = "math_expression"
    CONCEPTUAL = "conceptual"


class ValidationMethod(str, Enum):
    DETERMINISTIC = "deterministic"
    SUBJECTIVE = "subjective"
    REGEX = "regex"
    NUMERIC_TOLERANCE = "numeric_tolerance"


@dataclass
class QuestionOption:
    option_key: str
    option_text: str
    is_correct: bool = False


@dataclass
class AnswerKey:
    question_id: str
    correct_answer: str | None = None
    validation_method: ValidationMethod = ValidationMethod.DETERMINISTIC
    tolerance: float | None = None
    scoring_criteria: str | None = None


@dataclass
class Question:
    id: str
    stem: str
    question_type: QuestionType
    options: list[QuestionOption] = field(default_factory=list)
    answer_key: Optional[AnswerKey] = None
    difficulty: str = "medium"
    source_reference_id: Optional[str] = None
    is_ambiguous: bool = False
    is_reported: bool = False


@dataclass
class EvaluationResult:
    question_id: str
    is_correct: bool
    score: float  # 0.0 to 1.0
    confidence: float  # system confidence
    method: ValidationMethod
    feedback: str
    criteria_met: list[str] = field(default_factory=list)


class QuestionValidator:
    """Validates generated questions before they are presented to students."""

    def validate(self, question: Question) -> list[str]:
        """Return list of validation problems (empty if valid)."""
        problems: list[str] = []
        if not question.stem or not question.stem.strip():
            problems.append("Question stem is empty")
        if question.question_type in (QuestionType.MULTIPLE_CHOICE, QuestionType.MULTIPLE_SELECT):
            if not question.options:
                problems.append("Multiple-choice question has no options")
            correct = [o for o in question.options if o.is_correct]
            if question.question_type == QuestionType.MULTIPLE_CHOICE and len(correct) != 1:
                problems.append("Multiple-choice question must have exactly one correct option")
        if question.answer_key is None:
            problems.append("Question has no answer key")
        return problems


class AssessmentEngine:
    """Assessment generation, evaluation, and grading."""

    def __init__(self, orchestrator: Orchestrator | None = None) -> None:
        self.orchestrator = orchestrator
        self.validator = QuestionValidator()

    def evaluate_deterministic(
        self,
        question: Question,
        student_answer: str | list[str],
    ) -> EvaluationResult:
        """Grade using deterministic rules (MCQ, numerical, T/F). No AI."""
        if question.answer_key is None:
            return EvaluationResult(
                question_id=question.id,
                is_correct=False,
                score=0.0,
                confidence=0.0,
                method=ValidationMethod.DETERMINISTIC,
                feedback="No answer key available.",
            )

        key = question.answer_key
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            correct = student_answer == key.correct_answer
        elif question.question_type == QuestionType.TRUE_FALSE:
            correct = str(student_answer).lower() == str(key.correct_answer).lower()
        elif question.question_type == QuestionType.NUMERICAL:
            correct = self._numeric_match(student_answer, key.correct_answer, key.tolerance)
        else:
            correct = str(student_answer).strip().lower() == str(key.correct_answer).strip().lower()

        return EvaluationResult(
            question_id=question.id,
            is_correct=correct,
            score=1.0 if correct else 0.0,
            confidence=1.0,  # deterministic = full confidence
            method=key.validation_method,
            feedback="Correct." if correct else "Incorrect.",
        )

    async def evaluate_subjective(
        self,
        question: Question,
        student_answer: str,
        criteria: str,
        user_id: Optional[str] = None,
    ) -> EvaluationResult:
        """Grade subjective answers using AI with explicit criteria and confidence."""
        if self.orchestrator is None:
            return EvaluationResult(
                question_id=question.id,
                is_correct=False,
                score=0.0,
                confidence=0.0,
                method=ValidationMethod.SUBJECTIVE,
                feedback="AI evaluator not configured.",
            )
        response = await self.orchestrator.evaluate_answer(
            question=question.stem,
            answer=student_answer,
            criteria=criteria,
            user_id=user_id,
        )
        # Parse AI response (would use structured output in production).
        is_correct = "correct" in (response.content or "").lower()
        return EvaluationResult(
            question_id=question.id,
            is_correct=is_correct,
            score=1.0 if is_correct else 0.0,
            confidence=0.6,  # transparent uncertainty for subjective AI grading
            method=ValidationMethod.SUBJECTIVE,
            feedback=response.content or "Unable to evaluate.",
            criteria_met=[],
        )

    def validate_question(self, question: Question) -> list[str]:
        return self.validator.validate(question)

    @staticmethod
    def _numeric_match(answer: str | list[str], correct: str | None, tolerance: float | None) -> bool:
        if correct is None:
            return False
        try:
            val = float(answer if isinstance(answer, str) else answer[0])
            target = float(correct)
        except (ValueError, TypeError, IndexError):
            return False
        if tolerance is None:
            return abs(val - target) < 1e-9
        return abs(val - target) <= tolerance
