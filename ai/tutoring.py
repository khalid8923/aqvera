"""AI Tutor: course-aware, lesson-aware, source-grounded conversations.

Distinguishes:
- Evidence from uploaded materials (source-grounded).
- External knowledge.
- Reasoned inference.
- Uncertainty.

Never fabricates page citations. Clearly indicates when materials do not
contain the answer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import AIResponse, Message, TaskType
from ai.orchestration import Orchestrator


@dataclass
class SourceReference:
    document_id: str
    document_title: str
    section: Optional[str] = None
    page: Optional[int] = None
    slide: Optional[int] = None


@dataclass
class TutorTurn:
    role: str  # "user" | "assistant"
    content: str
    sources: list[SourceReference] = field(default_factory=list)
    evidence_type: str = "external"  # "source" | "external" | "inference" | "uncertain"


class Tutor:
    """Course-aware, lesson-aware AI tutor."""

    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator

    async def answer(
        self,
        question: str,
        course_id: str | None,
        lesson_id: str | None,
        sources: list[SourceReference],
        user_id: str | None = None,
        difficulty: str = "intermediate",
        language: str = "en",
    ) -> tuple[str, list[SourceReference], str]:
        """Answer a student question.

        Returns (answer_text, sources_used, evidence_type).

        evidence_type is one of: "source", "external", "inference", "uncertain".
        """
        source_block = ""
        if sources:
            lines = []
            for s in sources:
                loc = []
                if s.section:
                    loc.append(f"section {s.section}")
                if s.page is not None:
                    loc.append(f"page {s.page}")
                if s.slide is not None:
                    loc.append(f"slide {s.slide}")
                loc_str = ", ".join(loc) if loc else "source"
                lines.append(f"- [{s.document_title} ({loc_str})]")
            source_block = "\n".join(lines)

        messages = [
            Message(
                role="system",
                content=(
                    "You are AQVERA's academic tutor. Answer the student's question "
                    f"at {difficulty} difficulty in {language}. "
                    "Ground your answer in the provided sources when available. "
                    "Clearly distinguish: (1) evidence from uploaded sources, "
                    "(2) external knowledge, (3) reasoned inference, (4) uncertainty. "
                    "Never fabricate page citations. If the sources do not contain "
                    "the answer, say so explicitly and offer to answer from external "
                    "knowledge with that caveat."
                ),
            ),
            Message(
                role="user",
                content=(
                    f"Question: {question}\n"
                    f"Course: {course_id or 'general'}\n"
                    f"Lesson: {lesson_id or 'general'}\n"
                    f"Difficulty: {difficulty}\n"
                    f"Language: {language}\n"
                    f"Sources:\n{source_block or 'No sources provided.'}"
                ),
            ),
        ]

        response = await self.orchestrator.generate(
            task_type=TaskType.TUTOR_EXPLANATION,
            messages=messages,
            model="mock-model",
            user_id=user_id,
            temperature=0.3,
            max_tokens=1024,
        )

        evidence_type = self._infer_evidence_type(response, bool(sources))
        return response.content or "I'm unable to answer right now.", sources, evidence_type

    def _infer_evidence_type(self, response: AIResponse, has_sources: bool) -> str:
        content = (response.content or "").lower()
        if response.error is not None:
            return "uncertain"
        if not has_sources:
            return "external"
        # Heuristic: look for source-attribution language.
        if any(p in content for p in ["according to", "source", "page", "section"]):
            return "source"
        if any(p in content for p in ["i don't know", "not in the sources", "not mentioned"]):
            return "uncertain"
        return "external"
