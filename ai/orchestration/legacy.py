"""AI orchestration layer.

Coordinates AI requests across providers for tutoring, RAG, assessment, and
content generation. Business logic (teaching methodology, adaptive decisions)
lives in the backend/ai domain modules; this layer only handles provider
communication, retries, fallback, and structured output validation.
"""

from __future__ import annotations

from typing import Optional

from ai import AIError, AIRequest, AIResponse, AIUsage, Message, TaskType
from ai.routing import Router
from ai.security import PromptInjectionGuard


class Orchestrator:
    """High-level AI orchestration for AQVERA academic tasks."""

    def __init__(
        self,
        router: Router,
        injection_guard: PromptInjectionGuard | None = None,
    ) -> None:
        self.router = router
        self.injection_guard = injection_guard or PromptInjectionGuard()

    async def generate(
        self,
        task_type: TaskType,
        messages: list[Message],
        model: str,
        user_id: Optional[str] = None,
        provider: Optional[str] = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        structured: bool = False,
    ) -> AIResponse:
        """Generate an AI response for an academic task.

        Sanitizes user content for prompt injection, routes to a provider,
        and returns a normalized AIResponse.
        """
        safe_messages = self.injection_guard.sanitize(messages)
        request = AIRequest(
            provider=provider or "",
            model=model,
            messages=safe_messages,
            task_type=task_type,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
        )
        return await self.router.route(request, task_type, user_id=user_id)

    async def explain(
        self,
        concept: str,
        level: str,
        sources: list[str],
        user_id: Optional[str] = None,
    ) -> AIResponse:
        """Produce a source-grounded explanation at a given difficulty level."""
        source_block = "\n".join(f"- {s}" for s in sources) if sources else "No sources provided."
        messages = [
            Message(
                role="system",
                content=(
                    "You are AQVERA's academic tutor. Explain concepts clearly at the "
                    "requested difficulty level. Ground answers in the provided sources. "
                    "Distinguish evidence from sources, external knowledge, reasoned "
                    "inference, and uncertainty. Never fabricate page citations. "
                    "If the sources do not contain the answer, say so explicitly."
                ),
            ),
            Message(
                role="user",
                content=(
                    f"Concept: {concept}\n"
                    f"Difficulty level: {level}\n"
                    f"Sources:\n{source_block}"
                ),
            ),
        ]
        return await self.generate(
            task_type=TaskType.TUTOR_EXPLANATION,
            messages=messages,
            model="mock-model",
            user_id=user_id,
            temperature=0.3,
            max_tokens=1024,
        )

    async def generate_questions(
        self,
        topic: str,
        count: int,
        question_type: str,
        user_id: Optional[str] = None,
    ) -> AIResponse:
        """Generate assessment questions for a topic (to be validated before use)."""
        messages = [
            Message(
                role="system",
                content=(
                    "You generate assessment questions for academic topics. "
                    "Return questions aligned to the topic, unambiguous, with an "
                    "indicated difficulty. Questions will be validated before use."
                ),
            ),
            Message(
                role="user",
                content=(
                    f"Topic: {topic}\n"
                    f"Count: {count}\n"
                    f"Question type: {question_type}"
                ),
            ),
        ]
        return await self.generate(
            task_type=TaskType.QUESTION_GENERATION,
            messages=messages,
            model="mock-model",
            user_id=user_id,
            temperature=0.4,
            max_tokens=1536,
        )

    async def evaluate_answer(
        self,
        question: str,
        answer: str,
        criteria: str,
        user_id: Optional[str] = None,
    ) -> AIResponse:
        """Evaluate a student answer against explicit criteria (subjective)."""
        messages = [
            Message(
                role="system",
                content=(
                    "You evaluate student answers against explicit scoring criteria. "
                    "Return a correctness judgment, score, confidence, and brief "
                    "feedback. State uncertainty where criteria are ambiguous."
                ),
            ),
            Message(
                role="user",
                content=(
                    f"Question: {question}\n"
                    f"Student answer: {answer}\n"
                    f"Criteria: {criteria}"
                ),
            ),
        ]
        return await self.generate(
            task_type=TaskType.ANSWER_EVALUATION,
            messages=messages,
            model="mock-model",
            user_id=user_id,
            temperature=0.2,
            max_tokens=768,
        )
