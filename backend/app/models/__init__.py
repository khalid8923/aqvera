from app.models.base import Base  # noqa: F401
from app.models.auth import (
    UserSession,
    PasswordReset,
    EmailVerification,
    UserPreference,
    OnboardingRecord,
)  # noqa: F401
from app.models.course import User, Course  # noqa: F401
from app.models.chat import Conversation  # noqa: F401
from app.models.message import Message  # noqa: F401
from app.models.material import UploadedMaterial, ProcessingJob, MaterialChunk  # noqa: F401
from app.models.study import (  # noqa: F401
    Note,
    Notebook,
    Tag,
    NoteTag,
    Topic,
    FlashcardDeck,
    Flashcard,
    FlashcardReview,
    Assessment,
    AssessmentQuestion,
    AssessmentAttempt,
    AssessmentAnswer,
    TopicMastery,
)

__all__ = [
    "User",
    "Course",
    "Conversation",
    "Message",
    "UploadedMaterial",
    "ProcessingJob",
    "MaterialChunk",
    "UserSession",
    "PasswordReset",
    "EmailVerification",
    "UserPreference",
    "OnboardingRecord",
    "Note",
    "Notebook",
    "Tag",
    "NoteTag",
    "Topic",
    "FlashcardDeck",
    "Flashcard",
    "FlashcardReview",
    "Assessment",
    "AssessmentQuestion",
    "AssessmentAttempt",
    "AssessmentAnswer",
    "TopicMastery",
]
