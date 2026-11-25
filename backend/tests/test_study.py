"""Tests for study features: notes, flashcards, assessments, progress."""

import uuid
from typing import Optional
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _unique_email(prefix: str = "study") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}@example.com"


def _auth_headers(email: Optional[str] = None, password: str = "StudyPass123!") -> dict:
    if email is None:
        email = _unique_email()
    client.post(
        "/auth/register",
        json={"email": email, "password": password, "full_name": "Study User"},
    )
    res = client.post("/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200, res.text
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_course(headers: dict) -> int:
    res = client.post(
        "/courses",
        json={"title": "Test Course", "subject_domain": "mathematics"},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    return res.json()["id"]


# --- Notes ---

def test_create_and_list_notes():
    headers = _auth_headers()
    course_id = _create_course(headers)

    res = client.post(
        "/study/notes",
        json={"title": "My Note", "content": "Note content here", "course_id": course_id},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    assert res.json()["title"] == "My Note"
    assert res.json()["course_id"] == course_id

    res = client.get("/study/notes", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_note_ownership_isolation():
    headers_a = _auth_headers()
    headers_b = _auth_headers()

    res = client.post(
        "/study/notes",
        json={"title": "Private Note", "content": "secret"},
        headers=headers_a,
    )
    assert res.status_code == 201, res.text
    note_id = res.json()["id"]

    # User B cannot access User A's note
    res = client.get(f"/study/notes/{note_id}", headers=headers_b)
    assert res.status_code == 404, res.text

    res = client.delete(f"/study/notes/{note_id}", headers=headers_b)
    assert res.status_code == 404, res.text


def test_pin_note():
    headers = _auth_headers()
    res = client.post(
        "/study/notes",
        json={"title": "Pin Test", "content": "content"},
        headers=headers,
    )
    note_id = res.json()["id"]

    res = client.patch(
        f"/study/notes/{note_id}",
        json={"is_pinned": True},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["is_pinned"] is True


# --- Notebooks ---

def test_create_and_list_notebooks():
    headers = _auth_headers()
    res = client.post(
        "/study/notebooks",
        json={"name": "Math Notebook", "description": "For calculus notes"},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    assert res.json()["name"] == "Math Notebook"

    res = client.get("/study/notebooks", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


# --- Tags ---

def test_create_and_list_tags():
    headers = _auth_headers()
    res = client.post(
        "/study/tags",
        json={"name": "important", "color": "red"},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    assert res.json()["name"] == "important"

    res = client.get("/study/tags", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


# --- Topics ---

def test_create_and_list_topics():
    headers = _auth_headers()
    course_id = _create_course(headers)

    res = client.post(
        f"/study/courses/{course_id}/topics",
        json={"title": "Derivatives", "description": "Differentiation rules"},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    assert res.json()["title"] == "Derivatives"

    res = client.get(f"/study/courses/{course_id}/topics", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


# --- Flashcards ---

def test_create_deck_and_cards():
    headers = _auth_headers()
    course_id = _create_course(headers)

    # Create deck
    res = client.post(
        "/study/flashcards/decks",
        json={"title": "Calculus Deck", "course_id": course_id},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    deck_id = res.json()["id"]

    # Create card
    res = client.post(
        "/study/flashcards",
        json={"deck_id": deck_id, "front": "What is a derivative?", "back": "Rate of change"},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    assert res.json()["front"] == "What is a derivative?"

    # List cards
    res = client.get("/study/flashcards", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_flashcard_spaced_repetition():
    headers = _auth_headers()
    # Create deck and card
    res = client.post(
        "/study/flashcards/decks",
        json={"title": "SR Deck"},
        headers=headers,
    )
    deck_id = res.json()["id"]

    res = client.post(
        "/study/flashcards",
        json={"deck_id": deck_id, "front": "Q", "back": "A"},
        headers=headers,
    )
    card_id = res.json()["id"]

    # Review with quality 5 (easy)
    res = client.post(
        f"/study/flashcards/{card_id}/review",
        json={"quality": 5},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["repeat_count"] == 1
    assert res.json()["interval"] == 1

    # Review with quality 1 (hard - forget)
    res = client.post(
        f"/study/flashcards/{card_id}/review",
        json={"quality": 1},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["repeat_count"] == 0
    assert res.json()["lapses"] == 1


def test_due_flashcards():
    headers = _auth_headers()
    res = client.post(
        "/study/flashcards/decks",
        json={"title": "Due Deck"},
        headers=headers,
    )
    deck_id = res.json()["id"]
    client.post(
        "/study/flashcards",
        json={"deck_id": deck_id, "front": "Q", "back": "A"},
        headers=headers,
    )

    # New cards have no next_review_at, so they're due
    res = client.get("/study/flashcards?due_only=true", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


# --- Assessments ---

def test_create_assessment_and_questions():
    headers = _auth_headers()
    course_id = _create_course(headers)

    res = client.post(
        "/study/assessments",
        json={"title": "Calculus Quiz", "course_id": course_id},
        headers=headers,
    )
    assert res.status_code == 201, res.text
    assessment_id = res.json()["id"]

    res = client.post(
        f"/study/assessments/{assessment_id}/questions",
        json={
            "question_type": "multiple_choice",
            "stem": "What is 2+2?",
            "options": '[{"text": "3", "is_correct": false}, {"text": "4", "is_correct": true}]',
            "correct_answer": "4",
            "points": 1.0,
        },
        headers=headers,
    )
    assert res.status_code == 201, res.text
    assert res.json()["stem"] == "What is 2+2?"


def test_complete_assessment_attempt():
    headers = _auth_headers()
    course_id = _create_course(headers)

    res = client.post(
        "/study/assessments",
        json={"title": "Quiz", "course_id": course_id},
        headers=headers,
    )
    assessment_id = res.json()["id"]

    res = client.post(
        f"/study/assessments/{assessment_id}/questions",
        json={
            "question_type": "multiple_choice",
            "stem": "What is 2+2?",
            "options": '[{"text": "4", "is_correct": true}]',
            "correct_answer": "4",
            "points": 1.0,
        },
        headers=headers,
    )
    question_id = res.json()["id"]

    # Start attempt
    res = client.post(
        f"/study/assessments/{assessment_id}/attempts",
        headers=headers,
    )
    assert res.status_code == 201
    attempt_id = res.json()["id"]

    # Submit answer
    res = client.post(
        f"/study/attempts/{attempt_id}/answers",
        json={"question_id": question_id, "answer_text": "4"},
        headers=headers,
    )
    assert res.status_code == 201

    # Complete attempt
    res = client.post(
        f"/study/attempts/{attempt_id}/complete",
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json()["is_complete"] is True
    assert res.json()["score"] == 100.0


# --- Topic Mastery ---

def test_topic_mastery_after_assessment():
    headers = _auth_headers()
    course_id = _create_course(headers)

    # Create topic
    res = client.post(
        f"/study/courses/{course_id}/topics",
        json={"title": "Algebra"},
        headers=headers,
    )
    topic_id = res.json()["id"]

    # Create and complete assessment for the topic
    res = client.post(
        "/study/assessments",
        json={"title": "Algebra Quiz", "course_id": course_id, "topic_id": topic_id},
        headers=headers,
    )
    assessment_id = res.json()["id"]

    res = client.post(
        f"/study/assessments/{assessment_id}/questions",
        json={
            "question_type": "multiple_choice",
            "stem": "What is 2+2?",
            "options": '[{"text": "4", "is_correct": true}]',
            "correct_answer": "4",
            "points": 1.0,
        },
        headers=headers,
    )
    question_id = res.json()["id"]

    res = client.post(
        f"/study/assessments/{assessment_id}/attempts",
        headers=headers,
    )
    attempt_id = res.json()["id"]

    client.post(
        f"/study/attempts/{attempt_id}/answers",
        json={"question_id": question_id, "answer_text": "4"},
        headers=headers,
    )
    client.post(
        f"/study/attempts/{attempt_id}/complete",
        headers=headers,
    )

    # Check mastery
    res = client.get(f"/study/mastery/{topic_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["estimated_mastery"] > 0.0

    # List all mastery
    res = client.get("/study/mastery", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1


# --- Assessment ownership isolation ---

def test_assessment_ownership_isolation():
    headers_a = _auth_headers()
    headers_b = _auth_headers()

    res = client.post(
        "/study/assessments",
        json={"title": "Private Quiz"},
        headers=headers_a,
    )
    assert res.status_code == 201, res.text
    assessment_id = res.json()["id"]

    res = client.get(f"/study/assessments/{assessment_id}", headers=headers_b)
    assert res.status_code == 404, res.text
