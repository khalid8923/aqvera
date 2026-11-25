"""Study features service layer: notes, flashcards, assessments, progress."""

from typing import Optional, List
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.models.study import (
    Note, Notebook, Tag, NoteTag, Topic,
    FlashcardDeck, Flashcard, FlashcardReview,
    Assessment, AssessmentQuestion, AssessmentAttempt, AssessmentAnswer,
    TopicMastery,
)
from app.models.course import User, Course
from app.schemas.study import (
    NoteCreate, NoteUpdate,
    NotebookCreate, NotebookUpdate,
    TagCreate, TagUpdate,
    TopicCreate, TopicUpdate,
    FlashcardDeckCreate, FlashcardDeckUpdate,
    FlashcardCreate, FlashcardUpdate,
    FlashcardReviewCreate,
    AssessmentCreate, AssessmentUpdate,
    AssessmentQuestionCreate,
    AssessmentAttemptCreate,
    AssessmentAnswerCreate,
)


# ============================================================
# Notes
# ============================================================

def get_note(db: Session, note_id: int, user_id: int) -> Optional[Note]:
    return (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == user_id)
        .first()
    )


def list_notes(
    db: Session,
    user_id: int,
    course_id: Optional[int] = None,
    topic_id: Optional[int] = None,
    notebook_id: Optional[int] = None,
    include_archived: bool = False,
    pinned_only: bool = False,
    search: Optional[str] = None,
) -> List[Note]:
    query = db.query(Note).filter(Note.user_id == user_id)
    if course_id is not None:
        query = query.filter(Note.course_id == course_id)
    if topic_id is not None:
        query = query.filter(Note.topic_id == topic_id)
    if notebook_id is not None:
        query = query.filter(Note.notebook_id == notebook_id)
    if not include_archived:
        query = query.filter(Note.is_archived == False)  # noqa: E712
    if pinned_only:
        query = query.filter(Note.is_pinned == True)  # noqa: E712
    if search:
        query = query.filter(
            or_(Note.title.ilike(f"%{search}%"), Note.content.ilike(f"%{search}%"))
        )
    return query.order_by(Note.is_pinned.desc(), Note.updated_at.desc()).all()


def create_note(db: Session, note_in: NoteCreate, user_id: int) -> Note:
    db_note = Note(**note_in.model_dump(), user_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(db: Session, note_id: int, note_in: NoteUpdate, user_id: int) -> Optional[Note]:
    note = get_note(db, note_id, user_id)
    if not note:
        return None
    data = note_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(note, field, value)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int, user_id: int) -> bool:
    note = get_note(db, note_id, user_id)
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True


# ============================================================
# Notebooks
# ============================================================

def get_notebook(db: Session, notebook_id: int, user_id: int) -> Optional[Notebook]:
    return (
        db.query(Notebook)
        .filter(Notebook.id == notebook_id, Notebook.user_id == user_id)
        .first()
    )


def list_notebooks(db: Session, user_id: int) -> List[Notebook]:
    return (
        db.query(Notebook)
        .filter(Notebook.user_id == user_id)
        .order_by(Notebook.name)
        .all()
    )


def create_notebook(db: Session, nb_in: NotebookCreate, user_id: int) -> Notebook:
    db_nb = Notebook(**nb_in.model_dump(), user_id=user_id)
    db.add(db_nb)
    db.commit()
    db.refresh(db_nb)
    return db_nb


def update_notebook(
    db: Session, notebook_id: int, nb_in: NotebookUpdate, user_id: int
) -> Optional[Notebook]:
    nb = get_notebook(db, notebook_id, user_id)
    if not nb:
        return None
    data = nb_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(nb, field, value)
    db.add(nb)
    db.commit()
    db.refresh(nb)
    return nb


def delete_notebook(db: Session, notebook_id: int, user_id: int) -> bool:
    nb = get_notebook(db, notebook_id, user_id)
    if not nb:
        return False
    db.delete(nb)
    db.commit()
    return True


# ============================================================
# Tags
# ============================================================

def get_tag(db: Session, tag_id: int, user_id: int) -> Optional[Tag]:
    return (
        db.query(Tag)
        .filter(Tag.id == tag_id, Tag.user_id == user_id)
        .first()
    )


def list_tags(db: Session, user_id: int) -> List[Tag]:
    return db.query(Tag).filter(Tag.user_id == user_id).order_by(Tag.name).all()


def create_tag(db: Session, tag_in: TagCreate, user_id: int) -> Tag:
    db_tag = Tag(**tag_in.model_dump(), user_id=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# ============================================================
# Topics
# ============================================================

def get_topic(db: Session, topic_id: int) -> Optional[Topic]:
    return db.query(Topic).filter(Topic.id == topic_id).first()


def list_topics(
    db: Session, course_id: Optional[int] = None
) -> List[Topic]:
    query = db.query(Topic)
    if course_id is not None:
        query = query.filter(Topic.course_id == course_id)
    return query.order_by(Topic.order_index, Topic.title).all()


def create_topic(db: Session, topic_in: TopicCreate, course_id: int) -> Topic:
    db_topic = Topic(**topic_in.model_dump(), course_id=course_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


# ============================================================
# Flashcard Decks
# ============================================================

def get_deck(db: Session, deck_id: int, user_id: int) -> Optional[FlashcardDeck]:
    return (
        db.query(FlashcardDeck)
        .filter(FlashcardDeck.id == deck_id, FlashcardDeck.user_id == user_id)
        .first()
    )


def list_decks(
    db: Session, user_id: int, course_id: Optional[int] = None
) -> List[FlashcardDeck]:
    query = db.query(FlashcardDeck).filter(FlashcardDeck.user_id == user_id)
    if course_id is not None:
        query = query.filter(FlashcardDeck.course_id == course_id)
    return query.order_by(FlashcardDeck.updated_at.desc()).all()


def create_deck(db: Session, deck_in: FlashcardDeckCreate, user_id: int) -> FlashcardDeck:
    db_deck = FlashcardDeck(**deck_in.model_dump(), user_id=user_id)
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck


# ============================================================
# Flashcards
# ============================================================

def get_card(db: Session, card_id: int, user_id: int) -> Optional[Flashcard]:
    return (
        db.query(Flashcard)
        .join(FlashcardDeck, Flashcard.deck_id == FlashcardDeck.id)
        .filter(Flashcard.id == card_id, FlashcardDeck.user_id == user_id)
        .first()
    )


def list_cards(
    db: Session, user_id: int, deck_id: Optional[int] = None, due_only: bool = False
) -> List[Flashcard]:
    query = (
        db.query(Flashcard)
        .join(FlashcardDeck, Flashcard.deck_id == FlashcardDeck.id)
        .filter(FlashcardDeck.user_id == user_id)
    )
    if deck_id is not None:
        query = query.filter(Flashcard.deck_id == deck_id)
    if due_only:
        now = datetime.now(timezone.utc)
        query = query.filter(
            (Flashcard.next_review_at.is_(None)) | (Flashcard.next_review_at <= now)
        )
    return query.order_by(Flashcard.card_order).all()


def create_card(db: Session, card_in: FlashcardCreate, user_id: int) -> Optional[Flashcard]:
    deck = get_deck(db, card_in.deck_id, user_id)
    if not deck:
        return None
    db_card = Flashcard(**card_in.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def update_card(
    db: Session, card_id: int, card_in: FlashcardUpdate, user_id: int
) -> Optional[Flashcard]:
    card = get_card(db, card_id, user_id)
    if not card:
        return None
    data = card_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(card, field, value)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def delete_card(db: Session, card_id: int, user_id: int) -> bool:
    card = get_card(db, card_id, user_id)
    if not card:
        return False
    db.delete(card)
    db.commit()
    return True


# ============================================================
# Spaced Repetition (SM-2)
# ============================================================

def _sm2_next_interval(quality: int, card: Flashcard) -> tuple[int, float, int]:
    """Compute next interval using the SM-2 algorithm.

    Returns (interval_days, new_ease_factor, new_repeat_count).
    """
    ef = card.ease_factor
    if quality < 3:
        repeat_count = 0
        interval = 1
    else:
        if card.repeat_count == 0:
            interval = 1
        elif card.repeat_count == 1:
            interval = 6
        else:
            interval = int(card.interval * ef)
        repeat_count = card.repeat_count + 1

    # Update ease factor
    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, ef)
    return interval, ef, repeat_count


def review_card(
    db: Session,
    card_id: int,
    user_id: int,
    review_in: FlashcardReviewCreate,
) -> Optional[Flashcard]:
    """Record a flashcard review and update spaced-repetition state."""
    card = get_card(db, card_id, user_id)
    if not card:
        return None

    quality = review_in.quality
    interval, ef, repeat_count = _sm2_next_interval(quality, card)

    now = datetime.now(timezone.utc)
    card.interval = interval
    card.ease_factor = ef
    card.repeat_count = repeat_count
    card.next_review_at = now + timedelta(days=interval)
    card.last_reviewed_at = now
    if quality < 3:
        card.lapses += 1

    review = FlashcardReview(
        card_id=card.id,
        user_id=user_id,
        quality=quality,
        reviewed_at=now,
    )
    db.add(card)
    db.add(review)
    db.commit()
    db.refresh(card)
    return card


# ============================================================
# Assessments
# ============================================================

def get_assessment(
    db: Session, assessment_id: int, user_id: int
) -> Optional[Assessment]:
    return (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id, Assessment.user_id == user_id)
        .first()
    )


def list_assessments(
    db: Session, user_id: int, course_id: Optional[int] = None
) -> List[Assessment]:
    query = db.query(Assessment).filter(Assessment.user_id == user_id)
    if course_id is not None:
        query = query.filter(Assessment.course_id == course_id)
    return query.order_by(Assessment.created_at.desc()).all()


def create_assessment(
    db: Session, assessment_in: AssessmentCreate, user_id: int
) -> Assessment:
    db_assessment = Assessment(**assessment_in.model_dump(), user_id=user_id)
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


def add_assessment_question(
    db: Session,
    assessment_id: int,
    user_id: int,
    question_in: AssessmentQuestionCreate,
) -> Optional[AssessmentQuestion]:
    assessment = get_assessment(db, assessment_id, user_id)
    if not assessment:
        return None
    db_q = AssessmentQuestion(**question_in.model_dump(), assessment_id=assessment_id)
    db.add(db_q)
    db.commit()
    db.refresh(db_q)
    return db_q


def get_assessment_with_questions(
    db: Session, assessment_id: int, user_id: int
) -> Optional[Assessment]:
    return get_assessment(db, assessment_id, user_id)


# ============================================================
# Assessment Attempts & Answers
# ============================================================

def create_attempt(
    db: Session, attempt_in: AssessmentAttemptCreate, user_id: int
) -> Optional[AssessmentAttempt]:
    assessment = get_assessment(db, attempt_in.assessment_id, user_id)
    if not assessment:
        return None
    db_attempt = AssessmentAttempt(
        assessment_id=attempt_in.assessment_id,
        user_id=user_id,
        is_complete=False,
    )
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt


def submit_answer(
    db: Session,
    attempt_id: int,
    user_id: int,
    answer_in: AssessmentAnswerCreate,
) -> Optional[AssessmentAnswer]:
    attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.user_id == user_id,
        )
        .first()
    )
    if not attempt:
        return None
    question = (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.id == answer_in.question_id)
        .first()
    )
    if not question:
        return None

    # Deterministic grading where possible
    is_correct = None
    points_earned = 0.0
    if question.correct_answer is not None:
        if question.question_type in ("multiple_choice", "true_false"):
            is_correct = str(answer_in.answer_text or "").strip().lower() == str(
                question.correct_answer
            ).strip().lower()
        else:
            is_correct = str(answer_in.answer_text or "").strip().lower() == str(
                question.correct_answer
            ).strip().lower()
        points_earned = question.points if is_correct else 0.0

    db_answer = AssessmentAnswer(
        attempt_id=attempt_id,
        question_id=answer_in.question_id,
        answer_text=answer_in.answer_text,
        is_correct=is_correct,
        points_earned=points_earned,
        confidence=answer_in.confidence,
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def complete_attempt(
    db: Session, attempt_id: int, user_id: int
) -> Optional[AssessmentAttempt]:
    attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.user_id == user_id,
        )
        .first()
    )
    if not attempt:
        return None

    answers = (
        db.query(AssessmentAnswer)
        .filter(AssessmentAnswer.attempt_id == attempt_id)
        .all()
    )
    questions = (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.assessment_id == attempt.assessment_id)
        .all()
    )

    total_points = sum(q.points for q in questions)
    earned = sum(a.points_earned for a in answers)
    score = (earned / total_points * 100.0) if total_points > 0 else 0.0

    attempt.score = score
    attempt.is_complete = True
    attempt.completed_at = datetime.now(timezone.utc)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # Update topic mastery
    assessment = get_assessment(db, attempt.assessment_id, user_id)
    if assessment and assessment.topic_id:
        _update_topic_mastery(db, user_id, assessment.topic_id, score / 100.0)

    return attempt


def _update_topic_mastery(
    db: Session, user_id: int, topic_id: int, signal: float
) -> None:
    """Deterministic mastery update using a simple learning-rate rule."""
    mastery = (
        db.query(TopicMastery)
        .filter(TopicMastery.user_id == user_id, TopicMastery.topic_id == topic_id)
        .first()
    )
    now = datetime.now(timezone.utc)
    if not mastery:
        mastery = TopicMastery(
            user_id=user_id,
            topic_id=topic_id,
            estimated_mastery=0.0,
            confidence=0.0,
            evidence_count=0,
            last_interaction_at=now,
        )
        db.add(mastery)

    lr = 0.2 / (1.0 + 0.1 * mastery.evidence_count)
    mastery.estimated_mastery = max(
        0.0,
        min(1.0, mastery.estimated_mastery + lr * (signal - mastery.estimated_mastery)),
    )
    mastery.evidence_count += 1
    mastery.confidence = min(1.0, mastery.evidence_count / 10.0)
    mastery.last_interaction_at = now
    db.add(mastery)
    db.commit()


# ============================================================
# Topic Mastery
# ============================================================

def get_topic_mastery(
    db: Session, user_id: int, topic_id: int
) -> Optional[TopicMastery]:
    return (
        db.query(TopicMastery)
        .filter(TopicMastery.user_id == user_id, TopicMastery.topic_id == topic_id)
        .first()
    )


def list_topic_mastery(db: Session, user_id: int) -> List[TopicMastery]:
    return (
        db.query(TopicMastery)
        .filter(TopicMastery.user_id == user_id)
        .order_by(TopicMastery.estimated_mastery)
        .all()
    )
