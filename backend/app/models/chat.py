from typing import Optional
from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="New conversation")
    course_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("courses.id"), nullable=True, index=True
    )
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    course: Mapped[Optional["Course"]] = relationship("Course")
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at"
    )
