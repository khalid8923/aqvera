"""RAG pipeline: retrieval, context construction, source attribution.

Retrieval is separate from generation. The LLM is never the source of truth
for document references — source references come from the retrieval index.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ai import Message, TaskType
from ai.orchestration import Orchestrator


@dataclass
class Chunk:
    id: str
    text: str
    document_id: str
    document_title: str
    section: Optional[str] = None
    page: Optional[int] = None
    slide: Optional[int] = None
    score: float = 0.0


@dataclass
class RetrievalResult:
    chunks: list[Chunk]
    query: str
    total_found: int


class RAGPipeline:
    """Retrieval-augmented generation for source-grounded answers."""

    def __init__(self, orchestrator: Orchestrator, retrieval: "RetrievalService") -> None:
        self.orchestrator = orchestrator
        self.retrieval = retrieval

    async def retrieve_and_answer(
        self,
        question: str,
        course_id: str | None,
        user_id: str | None = None,
        top_k: int = 5,
        language: str = "en",
    ) -> tuple[str, list[Chunk], str]:
        """Retrieve relevant chunks, then answer grounded in them.

        Returns (answer, chunks_used, evidence_type).
        """
        results = await self.retrieval.retrieve(question, course_id=course_id, top_k=top_k)
        chunks = results.chunks

        if not chunks:
            # No relevant source material — answer from external knowledge with caveat.
            messages = [
                Message(
                    role="system",
                    content=(
                        "You are AQVERA's tutor. No relevant uploaded material was "
                        "found for this question. Answer from external knowledge if "
                        "appropriate, but clearly state that the answer is NOT grounded "
                        "in the student's uploaded sources and that the sources do not "
                        "contain the answer."
                    ),
                ),
                Message(role="user", content=f"Question: {question}"),
            ]
            response = await self.orchestrator.generate(
                task_type=TaskType.TUTOR_EXPLANATION,
                messages=messages,
                model="mock-model",
                user_id=user_id,
                temperature=0.3,
                max_tokens=1024,
            )
            return response.content or "No relevant sources found.", [], "uncertain"

        context_blocks = []
        for c in chunks:
            loc = []
            if c.section:
                loc.append(f"section {c.section}")
            if c.page is not None:
                loc.append(f"page {c.page}")
            if c.slide is not None:
                loc.append(f"slide {c.slide}")
            loc_str = ", ".join(loc) if loc else "source"
            context_blocks.append(
                f"[{c.document_title} ({loc_str})]: {c.text}"
            )
        context = "\n\n".join(context_blocks)

        messages = [
            Message(
                role="system",
                content=(
                    "You are AQVERA's tutor. Answer using ONLY the provided source "
                    "context. Cite the source title and location (page/section/slide) "
                    "for every claim. If the sources do not contain the answer, say so "
                    "explicitly. Never fabricate citations."
                ),
            ),
            Message(
                role="user",
                content=(
                    f"Question: {question}\n\n"
                    f"Source context:\n{context}"
                ),
            ),
        ]
        response = await self.orchestrator.generate(
            task_type=TaskType.TUTOR_EXPLANATION,
            messages=messages,
            model="mock-model",
            user_id=user_id,
            temperature=0.2,
            max_tokens=1024,
        )
        return response.content or "Unable to generate answer.", chunks, "source"


class RetrievalService:
    """Abstract retrieval service — concrete implementations query the vector store.

    This is the interface; the concrete vector-store-backed implementation lives
    in the backend content-processing domain (or ai.retrieval when a vector index
    is available locally).
    """

    async def retrieve(
        self,
        query: str,
        course_id: str | None = None,
        top_k: int = 5,
    ) -> RetrievalResult:
        """Return chunks relevant to the query, optionally filtered by course."""
        raise NotImplementedError
