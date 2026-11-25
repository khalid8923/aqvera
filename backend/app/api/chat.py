from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db_session, get_current_user
from app.models.chat import Conversation
from app.models.message import Message
from app.models.course import Course, User
from app.schemas.chat import (
    ConversationCreate,
    ConversationRead,
    ConversationWithMessages,
    MessageRead,
    MessageCreate,
    AIStatus,
)
from app.services import chat as chat_service
from app.core.config import settings

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("/ai-status", response_model=AIStatus)
def ai_status():
    """Return whether a real AI provider is configured.

    AQVERA does not depend on a single commercial AI API. No provider has been
    selected yet (see docs/architecture/AI_ARCHITECTURE.md — Initial Provider
    Selection is OPEN), so assistant generation is unavailable until a provider
    is configured. This endpoint never fabricates AI responses.
    """
    return AIStatus(
        configured=False,
        provider=None,
        message=(
            "No AI provider is configured. Select and configure a provider "
            "(OpenAI, Anthropic, Ollama, Azure OpenAI, or custom) before "
            "assistant responses can be generated."
        ),
    )


@router.post("", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
def create_conversation(
    conv_in: ConversationCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    # Validate optional course ownership
    if conv_in.course_id is not None:
        course = (
            db.query(Course)
            .filter(Course.id == conv_in.course_id, Course.owner_id == current_user.id)
            .first()
        )
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
    return chat_service.create_conversation(db, conv_in, current_user.id)


@router.get("", response_model=List[ConversationRead])
def list_conversations(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    course_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    return chat_service.get_conversations(
        db, current_user.id, course_id=course_id, skip=skip, limit=limit
    )


@router.get("/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    conversation = chat_service.get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    conversation_id: int,
    message_in: MessageCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    conversation = chat_service.get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    user_message = chat_service.create_message(
        db, conversation_id, message_in.role, message_in.content
    )
    return user_message


@router.get("/{conversation_id}/messages", response_model=List[MessageRead])
def list_messages(
    conversation_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(200, ge=1, le=1000),
):
    conversation = chat_service.get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return chat_service.get_messages(db, conversation_id, skip=skip, limit=limit)


@router.patch("/{conversation_id}", response_model=ConversationRead)
def update_conversation(
    conversation_id: int,
    title: str,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    conversation = chat_service.get_conversation(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return chat_service.update_conversation_title(db, conversation, title)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    success = chat_service.delete_conversation(db, conversation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return None
