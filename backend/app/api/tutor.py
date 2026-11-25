"""AI tutor endpoints: source-grounded Q&A via the ai/ orchestration layer."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List
from app.core.deps import get_db_session, get_current_user
from app.models.course import User
from app.models.chat import Conversation
from app.models.material import MaterialChunk, UploadedMaterial
from ai.orchestration import Orchestrator
from ai.providers.base import ProviderRegistry
from ai.providers.mock import MockProvider
from ai.routing import Router
from ai.cost_control import CostTracker

router = APIRouter(prefix="/ai", tags=["ai"])

# Build a shared orchestrator with the mock provider (no live credentials configured).
_registry = ProviderRegistry()
_registry.register(MockProvider())
_router = Router(_registry, CostTracker())
_orchestrator = Orchestrator(_router)


class SourceReference(BaseModel):
    document_id: str
    document_title: str
    section: Optional[str] = None
    page: Optional[int] = None
    slide: Optional[int] = None


class TutorAsk(BaseModel):
    conversation_id: int
    question: str
    course_id: int | None = None
    lesson_id: int | None = None


class TutorAnswer(BaseModel):
    answer: str
    sources: List[SourceReference] = Field(default_factory=list)
    evidence_type: str  # source | external | inference | uncertain


@router.post("/tutor/ask", response_model=TutorAnswer)
async def tutor_ask(
    ask: TutorAsk,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    """Answer a student question using the ai/ tutoring module.

    Backed by MockProvider (no live AI key configured). Returns an honest
    "not configured" indication when no provider is available.

    When a course is specified, searches the user's uploaded materials for
    relevant chunks and grounds the answer in those sources (RAG).
    """
    from ai.tutoring import Tutor, SourceReference as TutorSourceReference

    # Determine course context.
    course_id = ask.course_id
    if course_id is None:
        # Try to get course from conversation.
        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == ask.conversation_id,
                Conversation.owner_id == current_user.id,
            )
            .first()
        )
        if conversation:
            course_id = conversation.course_id

    # Gather source-grounded chunks via keyword search (RAG).
    sources: list[TutorSourceReference] = []
    source_texts: list[str] = []

    if course_id is not None:
        chunks = (
            db.query(MaterialChunk)
            .join(UploadedMaterial, MaterialChunk.material_id == UploadedMaterial.id)
            .filter(
                MaterialChunk.user_id == current_user.id,
                UploadedMaterial.status == "completed",
            )
            .all()
        )
        if chunks:
            from app.services import material_processing

            matched = material_processing.keyword_search_chunks(
                ask.question, chunks, top_k=5
            )
            for chunk in matched:
                sources.append(
                    TutorSourceReference(
                        document_id=str(chunk.material_id),
                        document_title=chunk.material.original_filename,
                        section=chunk.section,
                        page=chunk.page,
                    )
                )
                loc = []
                if chunk.section:
                    loc.append(f"section {chunk.section}")
                if chunk.page is not None:
                    loc.append(f"page {chunk.page}")
                loc_str = ", ".join(loc) if loc else "source"
                source_texts.append(
                    f"[{chunk.material.original_filename} ({loc_str})]: {chunk.text}"
                )

    tutor = Tutor(_orchestrator)
    answer, _, evidence_type = await tutor.answer(
        question=ask.question,
        course_id=str(course_id) if course_id else None,
        lesson_id=str(ask.lesson_id) if ask.lesson_id else None,
        sources=sources,
        user_id=str(current_user.id),
    )

    # If we found source chunks but evidence type isn't "source", upgrade it.
    if sources and evidence_type == "external":
        evidence_type = "source"

    return TutorAnswer(
        answer=answer,
        sources=[
            SourceReference(
                document_id=s.document_id,
                document_title=s.document_title,
                section=s.section,
                page=s.page,
                slide=s.slide,
            )
            for s in sources
        ],
        evidence_type=evidence_type,
    )
