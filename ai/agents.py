"""AI agents: domain-specific agents built on top of orchestration.

Agents coordinate retrieval, tutoring, and content generation for specific
academic workflows. The teaching methodology governs instruction; agents
provide AI capabilities within those boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ai import AIResponse, Message, TaskType
from ai.orchestration import Orchestrator


@dataclass
class AgentResult:
    content: str
    sources: list[str]
    evidence_type: str  # "source" | "external" | "inference" | "uncertain"
    response: AIResponse


class TutorAgent:
    """Course-aware tutor agent that preserves academic context."""

    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator

    async def answer_question(
        self,
        question: str,
        course_id: Optional[str],
        lesson_id: Optional[str],
        sources: list[str],
        user_id: Optional[str] = None,
    ) -> AgentResult:
        messages = [
            Message(
                role="system",
                content=(
                    "You are AQVERA's academic tutor. Preserve the academic topic "
                    "and source context. Distinguish evidence from uploaded materials, "
                    "external knowledge, reasoned inference, and uncertainty. "
                    "Never fabricate citations."
                ),
            ),
            Message(
                role="user",
                content=(
                    f"Question: {question}\n"
                    f"Course: {course_id or 'general'}\n"
                    f"Lesson: {lesson_id or 'general'}\n"
                    f"Sources: {sources or 'none'}"
                ),
            ),
        ]
        response = await self.orchestrator.generate(
            task_type=TaskType.TUTOR_EXPLANATION,
            messages=messages,
            model="mock-model",
            user_id=user_id,
            temperature=0.3,
        )
        return AgentResult(
            content=response.content or "Unable to answer.",
            sources=sources,
            evidence_type="source" if sources else "external",
            response=response,
        )


class ContentAgent:
    """Generates lessons, examples, explanations, and practice materials."""

    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator

    async def generate_explanation(
        self,
        concept: str,
        level: str,
        sources: list[str],
        user_id: Optional[str] = None,
    ) -> AgentResult:
        source_block = "\n".join(f"- {s}" for s in sources) if sources else "none"
        messages = [
            Message(
                role="system",
                content=(
                    "Generate an academic explanation at the requested level. "
                    "Ground in sources; mark external knowledge and inference."
                ),
            ),
            Message(
                role="user",
                content=(
                    f"Concept: {concept}\nLevel: {level}\nSources:\n{source_block}"
                ),
            ),
        ]
        response = await self.orchestrator.generate(
            task_type=TaskType.CONTENT_GENERATION,
            messages=messages,
            model="mock-model",
            user_id=user_id,
            temperature=0.4,
        )
        return AgentResult(
            content=response.content or "Unable to generate explanation.",
            sources=sources,
            evidence_type="source" if sources else "external",
            response=response,
        )
