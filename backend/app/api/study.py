"""Study features API routes: notes, notebooks, tags, topics, flashcards, assessments, progress."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.deps import get_db_session, get_current_user
from app.models.course import User, Course
from app.models.study import Topic
from app.schemas.study import (
    NoteCreate, NoteUpdate, NoteRead,
    NotebookCreate, NotebookUpdate, NotebookRead,
    TagCreate, TagUpdate, TagRead,
    TopicCreate, TopicUpdate, TopicRead,
    FlashcardDeckCreate, FlashcardDeckUpdate, FlashcardDeckRead,
    FlashcardCreate, FlashcardUpdate, FlashcardRead,
    FlashcardReviewCreate, FlashcardReviewRead,
    AssessmentCreate, AssessmentUpdate, AssessmentRead,
    AssessmentQuestionCreate, AssessmentQuestionRead,
    AssessmentAttemptCreate, AssessmentAttemptRead,
    AssessmentAnswerCreate, AssessmentAnswerRead,
    TopicMasteryRead,
)
from app.services import study as study_service

router = APIRouter(prefix="/study", tags=["study"])


# ============================================================
# Notes
# ============================================================

@router.post("/notes", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.create_note(db, note_in, current_user.id)


@router.get("/notes", response_model=List[NoteRead])
def list_notes(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    course_id: Optional[int] = Query(None),
    topic_id: Optional[int] = Query(None),
    notebook_id: Optional[int] = Query(None),
    include_archived: bool = Query(False),
    pinned_only: bool = Query(False),
    search: Optional[str] = Query(None),
):
    return study_service.list_notes(
        db, current_user.id,
        course_id=course_id, topic_id=topic_id, notebook_id=notebook_id,
        include_archived=include_archived, pinned_only=pinned_only, search=search,
    )


@router.get("/notes/{note_id}", response_model=NoteRead)
def get_note(
    note_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    note = study_service.get_note(db, note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.patch("/notes/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    note = study_service.update_note(db, note_id, note_in, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    ok = study_service.delete_note(db, note_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return None


# ============================================================
# Notebooks
# ============================================================

@router.post("/notebooks", response_model=NotebookRead, status_code=status.HTTP_201_CREATED)
def create_notebook(
    nb_in: NotebookCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.create_notebook(db, nb_in, current_user.id)


@router.get("/notebooks", response_model=List[NotebookRead])
def list_notebooks(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.list_notebooks(db, current_user.id)


@router.patch("/notebooks/{notebook_id}", response_model=NotebookRead)
def update_notebook(
    notebook_id: int,
    nb_in: NotebookUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    nb = study_service.update_notebook(db, notebook_id, nb_in, current_user.id)
    if not nb:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return nb


@router.delete("/notebooks/{notebook_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notebook(
    notebook_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    ok = study_service.delete_notebook(db, notebook_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return None


# ============================================================
# Tags
# ============================================================

@router.post("/tags", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_in: TagCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.create_tag(db, tag_in, current_user.id)


@router.get("/tags", response_model=List[TagRead])
def list_tags(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.list_tags(db, current_user.id)


# ============================================================
# Topics
# ============================================================

@router.post("/courses/{course_id}/topics", response_model=TopicRead, status_code=status.HTTP_201_CREATED)
def create_topic(
    course_id: int,
    topic_in: TopicCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    # Verify course ownership
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.owner_id == current_user.id)
        .first()
    )
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return study_service.create_topic(db, topic_in, course_id)


@router.get("/courses/{course_id}/topics", response_model=List[TopicRead])
def list_topics(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.list_topics(db, course_id=course_id)


# ============================================================
# Flashcard Decks
# ============================================================

@router.post("/flashcards/decks", response_model=FlashcardDeckRead, status_code=status.HTTP_201_CREATED)
def create_deck(
    deck_in: FlashcardDeckCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.create_deck(db, deck_in, current_user.id)


@router.get("/flashcards/decks", response_model=List[FlashcardDeckRead])
def list_decks(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    course_id: Optional[int] = Query(None),
):
    return study_service.list_decks(db, current_user.id, course_id=course_id)


@router.get("/flashcards/decks/{deck_id}", response_model=FlashcardDeckRead)
def get_deck(
    deck_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    deck = study_service.get_deck(db, deck_id, current_user.id)
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck


# ============================================================
# Flashcards
# ============================================================

@router.post("/flashcards", response_model=FlashcardRead, status_code=status.HTTP_201_CREATED)
def create_card(
    card_in: FlashcardCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    card = study_service.create_card(db, card_in, current_user.id)
    if not card:
        raise HTTPException(status_code=404, detail="Deck not found")
    return card


@router.get("/flashcards", response_model=List[FlashcardRead])
def list_cards(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    deck_id: Optional[int] = Query(None),
    due_only: bool = Query(False),
):
    return study_service.list_cards(db, current_user.id, deck_id=deck_id, due_only=due_only)


@router.get("/flashcards/{card_id}", response_model=FlashcardRead)
def get_card(
    card_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    card = study_service.get_card(db, card_id, current_user.id)
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return card


@router.patch("/flashcards/{card_id}", response_model=FlashcardRead)
def update_card(
    card_id: int,
    card_in: FlashcardUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    card = study_service.update_card(db, card_id, card_in, current_user.id)
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return card


@router.delete("/flashcards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    ok = study_service.delete_card(db, card_id, current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return None


@router.post("/flashcards/{card_id}/review", response_model=FlashcardRead)
def review_card(
    card_id: int,
    review_in: FlashcardReviewCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    card = study_service.review_card(db, card_id, current_user.id, review_in)
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return card


# ============================================================
# Assessments
# ============================================================

@router.post("/assessments", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED)
def create_assessment(
    assessment_in: AssessmentCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.create_assessment(db, assessment_in, current_user.id)


@router.get("/assessments", response_model=List[AssessmentRead])
def list_assessments(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    course_id: Optional[int] = Query(None),
):
    return study_service.list_assessments(db, current_user.id, course_id=course_id)


@router.get("/assessments/{assessment_id}", response_model=AssessmentRead)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    assessment = study_service.get_assessment(db, assessment_id, current_user.id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


@router.post("/assessments/{assessment_id}/questions", response_model=AssessmentQuestionRead, status_code=status.HTTP_201_CREATED)
def add_question(
    assessment_id: int,
    question_in: AssessmentQuestionCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    question = study_service.add_assessment_question(db, assessment_id, current_user.id, question_in)
    if not question:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return question


# ============================================================
# Assessment Attempts
# ============================================================

@router.post("/assessments/{assessment_id}/attempts", response_model=AssessmentAttemptRead, status_code=status.HTTP_201_CREATED)
def create_attempt(
    assessment_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    attempt_in = AssessmentAttemptCreate(assessment_id=assessment_id)
    attempt = study_service.create_attempt(db, attempt_in, current_user.id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return attempt


@router.post("/attempts/{attempt_id}/answers", response_model=AssessmentAnswerRead, status_code=status.HTTP_201_CREATED)
def submit_answer(
    attempt_id: int,
    answer_in: AssessmentAnswerCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    answer = study_service.submit_answer(db, attempt_id, current_user.id, answer_in)
    if not answer:
        raise HTTPException(status_code=404, detail="Attempt or question not found")
    return answer


@router.post("/attempts/{attempt_id}/complete", response_model=AssessmentAttemptRead)
def complete_attempt(
    attempt_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    attempt = study_service.complete_attempt(db, attempt_id, current_user.id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt


# ============================================================
# Topic Mastery / Progress
# ============================================================

@router.get("/mastery", response_model=List[TopicMasteryRead])
def list_mastery(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    return study_service.list_topic_mastery(db, current_user.id)


@router.get("/mastery/{topic_id}", response_model=TopicMasteryRead)
def get_mastery(
    topic_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):
    mastery = study_service.get_topic_mastery(db, current_user.id, topic_id)
    if not mastery:
        raise HTTPException(status_code=404, detail="Mastery record not found")
    return mastery
