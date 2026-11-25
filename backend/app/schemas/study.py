"""Study features schemas: notes, notebooks, tags, flashcards, assessments, progress."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# --- Notes ---

class NoteBase(BaseModel):
    title: str
    content: str
    course_id: Optional[int] = None
    topic_id: Optional[int] = None
    notebook_id: Optional[int] = None
    is_pinned: Optional[bool] = None


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    course_id: Optional[int] = None
    topic_id: Optional[int] = None
    notebook_id: Optional[int] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None


class NoteRead(NoteBase):
    id: int
    user_id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Notebooks ---

class NotebookBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class NotebookCreate(NotebookBase):
    pass


class NotebookUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class NotebookRead(NotebookBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Tags ---

class TagBase(BaseModel):
    name: str
    color: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None


class TagRead(TagBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Topics ---

class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: Optional[int] = 0


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None


class TopicRead(TopicBase):
    id: int
    course_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Flashcard Decks ---

class FlashcardDeckBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: Optional[int] = None
    topic_id: Optional[int] = None


class FlashcardDeckCreate(FlashcardDeckBase):
    pass


class FlashcardDeckUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    course_id: Optional[int] = None
    topic_id: Optional[int] = None


class FlashcardDeckRead(FlashcardDeckBase):
    id: int
    user_id: int
    is_ai_generated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Flashcards ---

class FlashcardBase(BaseModel):
    deck_id: int
    front: str
    back: str
    card_order: Optional[int] = 0


class FlashcardCreate(FlashcardBase):
    pass


class FlashcardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None
    card_order: Optional[int] = None


class FlashcardRead(FlashcardBase):
    id: int
    interval: int
    repeat_count: int
    ease_factor: float
    next_review_at: Optional[datetime]
    last_reviewed_at: Optional[datetime]
    lapses: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Flashcard Review ---

class FlashcardReviewCreate(BaseModel):
    quality: int = Field(ge=0, le=5)  # SM-2 quality 0-5


class FlashcardReviewRead(BaseModel):
    id: int
    card_id: int
    user_id: int
    quality: int
    reviewed_at: datetime

    class Config:
        from_attributes = True


# --- Assessments ---

class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: Optional[int] = None
    topic_id: Optional[int] = None
    time_limit_minutes: Optional[int] = None
    is_mock_exam: Optional[bool] = None


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    course_id: Optional[int] = None
    topic_id: Optional[int] = None
    time_limit_minutes: Optional[int] = None
    is_mock_exam: Optional[bool] = None


class AssessmentRead(AssessmentBase):
    id: int
    user_id: int
    is_ai_generated: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# --- Assessment Questions ---

class AssessmentQuestionBase(BaseModel):
    question_type: str
    stem: str
    options: Optional[str] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    points: Optional[float] = 1.0
    order_index: Optional[int] = 0


class AssessmentQuestionCreate(AssessmentQuestionBase):
    pass


class AssessmentQuestionRead(AssessmentQuestionBase):
    id: int
    assessment_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Assessment Attempts ---

class AssessmentAttemptBase(BaseModel):
    assessment_id: int


class AssessmentAttemptCreate(AssessmentAttemptBase):
    pass


class AssessmentAttemptRead(AssessmentAttemptBase):
    id: int
    user_id: int
    score: Optional[float] = None
    is_complete: bool
    started_at: datetime
    completed_at: Optional[datetime] = None
    time_spent_seconds: Optional[int] = None

    class Config:
        from_attributes = True


# --- Assessment Answers ---

class AssessmentAnswerBase(BaseModel):
    question_id: int
    answer_text: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0, le=1)


class AssessmentAnswerCreate(AssessmentAnswerBase):
    pass


class AssessmentAnswerRead(AssessmentAnswerBase):
    id: int
    attempt_id: int
    is_correct: Optional[bool] = None
    points_earned: float
    created_at: datetime

    class Config:
        from_attributes = True


# --- Topic Mastery ---

class TopicMasteryRead(BaseModel):
    id: int
    user_id: int
    topic_id: int
    estimated_mastery: float
    confidence: float
    evidence_count: int
    last_interaction_at: Optional[datetime] = None

    class Config:
        from_attributes = True
