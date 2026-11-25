from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.chat import Conversation
from app.models.message import Message
from app.models.course import User
from app.schemas.chat import ConversationCreate, MessageCreate


def get_conversation(db: Session, conversation_id: int, owner_id: int) -> Optional[Conversation]:
    return (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.owner_id == owner_id)
        .first()
    )


def get_conversations(
    db: Session, owner_id: int, course_id: Optional[int] = None, skip: int = 0, limit: int = 100
) -> List[Conversation]:
    query = db.query(Conversation).filter(Conversation.owner_id == owner_id)
    if course_id is not None:
        query = query.filter(Conversation.course_id == course_id)
    return query.order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()


def create_conversation(db: Session, conv_in: ConversationCreate, owner_id: int) -> Conversation:
    db_conv = Conversation(**conv_in.model_dump(), owner_id=owner_id)
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv


def update_conversation_title(db: Session, conversation: Conversation, title: str) -> Conversation:
    conversation.title = title
    db.commit()
    db.refresh(conversation)
    return conversation


def delete_conversation(db: Session, conversation_id: int, owner_id: int) -> bool:
    conversation = get_conversation(db, conversation_id, owner_id)
    if not conversation:
        return False
    db.delete(conversation)
    db.commit()
    return True


def create_message(
    db: Session, conversation_id: int, role: str, content: str
) -> Message:
    db_msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(db_msg)
    # Touch conversation updated_at
    conversation = (
        db.query(Conversation).filter(Conversation.id == conversation_id).first()
    )
    if conversation:
        from sqlalchemy import func
        conversation.updated_at = func.now()
        db.add(conversation)
    db.commit()
    db.refresh(db_msg)
    return db_msg


def get_messages(
    db: Session, conversation_id: int, skip: int = 0, limit: int = 200
) -> List[Message]:
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
