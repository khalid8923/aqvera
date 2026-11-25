from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ConversationBase(BaseModel):
    title: str
    course_id: Optional[int] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    role: str
    content: str


class MessageRead(MessageBase):
    id: int
    conversation_id: int

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    role: str
    content: str


class ConversationWithMessages(ConversationRead):
    messages: List[MessageRead] = []

    class Config:
        from_attributes = True


class AIStatus(BaseModel):
    configured: bool
    provider: Optional[str] = None
    message: Optional[str] = None
