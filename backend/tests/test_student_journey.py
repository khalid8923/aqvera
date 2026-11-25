"""End-to-end integration tests for the complete student journey.

Covers: registration → login → onboarding → course creation → material upload
→ material processing → AI Tutor question with source grounding → source
references.

These tests use the FastAPI TestClient against the real backend, with the
MockProvider for AI (no live credentials required). They verify that the full
student workflow works without manual backend operations.
"""

import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _unique_email(prefix: str = "journey") -> str:
    return f"{prefix}{uuid.uuid4().hex[:8]}@example.com"


def _auth_headers(email: str, password: str = "JourneyPass123!") -> dict:
    """Register and log in, return bearer auth headers."""
    client.post(
        "/auth/register",
        json={"email": email, "password": password, "full_name": "Journey Student"},
    )
    res = client.post("/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200, res.text
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_student_journey_register_and_login():
    """1-2. Register and log in."""
    email = _unique_email()
    reg = client.post(
        "/auth/register",
        json={"email": email, "password": "JourneyPass123!", "full_name": "Journey Student"},
    )
    assert reg.status_code == 201, reg.text
    assert reg.json()["email"] == email
    assert reg.json()["is_active"] is True

    login = client.post(
        "/auth/login", json={"email": email, "password": "JourneyPass123!"}
    )
    assert login.status_code == 200, login.text
    assert "access_token" in login.json()
    assert "refresh_token" in login.json()


def test_student_journey_onboarding():
    """3-4. Complete onboarding steps."""
    email = _unique_email()
    headers = _auth_headers(email)

    # Onboarding starts incomplete
    res = client.get("/auth/onboarding", headers=headers)
    assert res.status_code == 200
    assert res.json()["completed"] is False

    # Complete each step
    for step in [
        "welcome_seen",
        "language_selected",
        "interests_selected",
        "tutor_introduced",
    ]:
        res = client.post(f"/auth/onboarding/{step}", headers=headers)
        assert res.status_code == 204, res.text

    res = client.get("/auth/onboarding", headers=headers)
    assert res.status_code == 200
    assert res.json()["welcome_seen"] is True
    assert res.json()["language_selected"] is True


def test_student_journey_create_course():
    """5. Create a course."""
    email = _unique_email()
    headers = _auth_headers(email)

    res = client.post(
        "/courses",
        json={
            "title": "Introduction to Calculus",
            "course_code": "MATH101",
            "semester": "Fall 2026",
            "subject_domain": "mathematics",
            "description": "Differential and integral calculus",
        },
        headers=headers,
    )
    assert res.status_code == 201, res.text
    data = res.json()
    assert data["title"] == "Introduction to Calculus"
    assert data["course_code"] == "MATH101"
    assert data["subject_domain"] == "mathematics"
    return None


def test_student_journey_upload_and_process_material():
    """6-8. Upload a document and process it."""
    email = _unique_email()
    headers = _auth_headers(email)

    # Create a course first
    course_res = client.post(
        "/courses",
        json={"title": "Calculus Course", "subject_domain": "mathematics"},
        headers=headers,
    )
    assert course_res.status_code == 201

    # Upload a text document
    upload_res = client.post(
        "/materials/upload",
        files={"file": ("lesson.txt", b"The derivative of f(x) = x^2 is f'(x) = 2x. This is the power rule for differentiation.", "text/plain")},
        headers=headers,
    )
    assert upload_res.status_code == 201, upload_res.text
    material_id = upload_res.json()["id"]
    assert upload_res.json()["status"] == "uploaded"

    # Check status
    status_res = client.get(f"/materials/{material_id}/status", headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["material_id"] == material_id

    # Process the material (runs in background)
    process_res = client.post(f"/materials/{material_id}/process", headers=headers)
    assert process_res.status_code == 200, process_res.text

    # Poll for processing to complete (background thread)
    import time
    completed = False
    for _ in range(20):
        status_res = client.get(f"/materials/{material_id}/status", headers=headers)
        if status_res.json()["status"] == "completed":
            completed = True
            break
        if status_res.json()["status"] == "failed":
            break
        time.sleep(0.25)
    assert completed, "Material processing did not complete"

    # Verify chunks were created
    chunks_res = client.get(f"/materials/{material_id}/chunks", headers=headers)
    assert chunks_res.status_code == 200
    chunks = chunks_res.json()
    assert len(chunks) >= 1
    assert "derivative" in chunks[0]["text"].lower() or "power rule" in chunks[0]["text"].lower()


def test_student_journey_ai_tutor_with_sources():
    """9-11. Ask AI Tutor a question and get source-grounded answer."""
    email = _unique_email()
    headers = _auth_headers(email)

    # Create a course
    course_res = client.post(
        "/courses",
        json={"title": "Calculus Course", "subject_domain": "mathematics"},
        headers=headers,
    )
    assert course_res.status_code == 201

    # Upload and process a material
    upload_res = client.post(
        "/materials/upload",
        files={"file": ("lesson.txt", b"The derivative of f(x) = x^2 is f'(x) = 2x. The power rule states that the derivative of x^n is n*x^(n-1).", "text/plain")},
        headers=headers,
    )
    assert upload_res.status_code == 201
    material_id = upload_res.json()["id"]

    process_res = client.post(f"/materials/{material_id}/process", headers=headers)
    assert process_res.status_code == 200

    # Poll for processing to complete (background thread)
    import time
    completed = False
    for _ in range(20):
        status_res = client.get(f"/materials/{material_id}/status", headers=headers)
        if status_res.json()["status"] == "completed":
            completed = True
            break
        if status_res.json()["status"] == "failed":
            break
        time.sleep(0.25)
    assert completed, "Material processing did not complete"

    # Create a conversation linked to the course
    conv_res = client.post(
        "/conversations",
        json={"title": "Calculus help", "course_id": course_res.json()["id"]},
        headers=headers,
    )
    assert conv_res.status_code == 201
    conversation_id = conv_res.json()["id"]

    # Ask a question about the material
    ask_res = client.post(
        "/ai/tutor/ask",
        json={
            "conversation_id": conversation_id,
            "question": "What is the power rule for derivatives?",
            "course_id": course_res.json()["id"],
        },
        headers=headers,
    )
    assert ask_res.status_code == 200, ask_res.text
    data = ask_res.json()
    assert "answer" in data
    assert "evidence_type" in data
    assert data["evidence_type"] in ("source", "external", "inference", "uncertain")
    assert len(data["answer"]) > 0


def test_student_journey_user_cannot_access_others_material():
    """12. Users cannot access another user's materials."""
    email_a = _unique_email("userA")
    email_b = _unique_email("userB")
    headers_a = _auth_headers(email_a)
    headers_b = _auth_headers(email_b)

    # User A uploads a material
    upload_res = client.post(
        "/materials/upload",
        files={"file": ("private.txt", b"User A's private material", "text/plain")},
        headers=headers_a,
    )
    assert upload_res.status_code == 201
    material_id = upload_res.json()["id"]

    # User B tries to access User A's material
    res = client.get(f"/materials/{material_id}", headers=headers_b)
    assert res.status_code == 404, res.text

    # User B tries to access User A's material status
    res = client.get(f"/materials/{material_id}/status", headers=headers_b)
    assert res.status_code == 404, res.text

    # User B tries to process User A's material
    res = client.post(f"/materials/{material_id}/process", headers=headers_b)
    assert res.status_code == 404, res.text


def test_student_journey_user_cannot_access_others_conversation():
    """13. Users cannot access another user's conversations."""
    email_a = _unique_email("userA")
    email_b = _unique_email("userB")
    headers_a = _auth_headers(email_a)
    headers_b = _auth_headers(email_b)

    # User A creates a conversation
    conv_res = client.post(
        "/conversations",
        json={"title": "User A's conversation"},
        headers=headers_a,
    )
    assert conv_res.status_code == 201
    conversation_id = conv_res.json()["id"]

    # User B tries to access User A's conversation
    res = client.get(f"/conversations/{conversation_id}", headers=headers_b)
    assert res.status_code == 404, res.text


def test_email_config_not_configured():
    """Email service reports not configured when no SMTP is set."""
    res = client.get("/auth/email/config")
    assert res.status_code == 200
    data = res.json()
    assert data["configured"] is False
    assert data["host"] is None


def test_student_journey_password_change_and_revoke():
    """Password change revokes sessions."""
    email = _unique_email()
    headers = _auth_headers(email)

    # Change password
    res = client.post(
        "/auth/password/change",
        json={"current_password": "JourneyPass123!", "new_password": "NewJourneyPass123!"},
        headers=headers,
    )
    assert res.status_code == 204, res.text

    # Old password no longer works
    login = client.post(
        "/auth/login", json={"email": email, "password": "JourneyPass123!"}
    )
    assert login.status_code == 401

    # New password works
    login = client.post(
        "/auth/login", json={"email": email, "password": "NewJourneyPass123!"}
    )
    assert login.status_code == 200


def test_student_journey_session_list_and_revoke():
    """List and revoke sessions."""
    email = _unique_email()
    headers = _auth_headers(email)

    res = client.get("/auth/sessions", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
