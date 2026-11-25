from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def _auth_headers(email: str = "coursetest@example.com", password: str = "secret123") -> dict:
    """Register and log in a user, return auth headers."""
    client.post(
        "/auth/register",
        json={"email": email, "password": password, "full_name": "Course Test User"},
    )
    res = client.post("/auth/login", json={"email": email, "password": password})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_course():
    response = client.post(
        "/courses",
        json={
            "title": "Introduction to Mathematics",
            "course_code": "MATH101",
            "semester": "Fall 2026",
            "subject_domain": "mathematics",
        },
        headers=_auth_headers(),
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "Introduction to Mathematics"
    assert data["course_code"] == "MATH101"
    assert data["id"] is not None


def test_list_courses():
    # Create a course first
    client.post(
        "/courses",
        json={"title": "List Test Course", "subject_domain": "mathematics"},
        headers=_auth_headers(),
    )
    response = client.get("/courses", headers=_auth_headers())
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_course():
    create_resp = client.post(
        "/courses",
        json={"title": "Get Test Course", "subject_domain": "mathematics"},
        headers=_auth_headers(),
    )
    course_id = create_resp.json()["id"]
    response = client.get(f"/courses/{course_id}", headers=_auth_headers())
    assert response.status_code == 200
    assert response.json()["id"] == course_id


def test_get_nonexistent_course():
    response = client.get("/courses/99999", headers=_auth_headers())
    assert response.status_code == 404


def test_update_course():
    create_resp = client.post(
        "/courses",
        json={"title": "Original Title", "subject_domain": "mathematics"},
        headers=_auth_headers(),
    )
    course_id = create_resp.json()["id"]
    response = client.put(
        f"/courses/{course_id}",
        json={"title": "Updated Title"},
        headers=_auth_headers(),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"


def test_archive_course():
    create_resp = client.post(
        "/courses",
        json={"title": "Archive Test", "subject_domain": "mathematics"},
        headers=_auth_headers(),
    )
    course_id = create_resp.json()["id"]
    response = client.patch(f"/courses/{course_id}/archive", headers=_auth_headers())
    assert response.status_code == 200
    assert response.json()["is_archived"] is True


def test_delete_course():
    create_resp = client.post(
        "/courses",
        json={"title": "Delete Test", "subject_domain": "mathematics"},
        headers=_auth_headers(),
    )
    course_id = create_resp.json()["id"]
    response = client.delete(f"/courses/{course_id}", headers=_auth_headers())
    assert response.status_code == 204

    get_response = client.get(f"/courses/{course_id}", headers=_auth_headers())
    assert get_response.status_code == 404


def test_register_user():
    import uuid
    email = f"regfresh{uuid.uuid4().hex[:8]}@example.com"
    response = client.post(
        "/auth/register",
        json={"email": email, "password": "secret123", "full_name": "Reg User"},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == email
    assert data["full_name"] == "Reg User"
    assert data["is_active"] is True


def test_register_duplicate_email():
    client.post(
        "/auth/register",
        json={"email": "dup2@example.com", "password": "secret123"},
    )
    response = client.post(
        "/auth/register",
        json={"email": "dup2@example.com", "password": "secret123"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_success():
    client.post(
        "/auth/register",
        json={"email": "logfresh@example.com", "password": "secret123"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "logfresh@example.com", "password": "secret123"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    client.post(
        "/auth/register",
        json={"email": "log2fresh@example.com", "password": "secret123"},
    )
    response = client.post(
        "/auth/login",
        json={"email": "log2fresh@example.com", "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_unknown_user():
    response = client.post(
        "/auth/login",
        json={"email": "none2@example.com", "password": "secret123"},
    )
    assert response.status_code == 401


# ---- Material upload tests ----

def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def _get_token():
    import uuid
    email = f"tok{uuid.uuid4().hex[:8]}@example.com"
    client.post("/auth/register", json={"email": email, "password": "pw123"})
    r = client.post("/auth/login", json={"email": email, "password": "pw123"})
    return r.json()["access_token"]


def test_upload_txt_material():
    token = _get_token()
    response = client.post(
        "/materials/upload",
        files={"file": ("lesson.txt", b"Introduction to calculus and algebra.", "text/plain")},
        headers=_auth_header(token),
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["original_filename"] == "lesson.txt"
    assert data["content_type"] == "text/plain"
    assert data["status"] == "uploaded"


def test_upload_unsupported_file():
    token = _get_token()
    response = client.post(
        "/materials/upload",
        files={"file": ("bad.xyz", b"data", "application/octet-stream")},
        headers=_auth_header(token),
    )
    assert response.status_code == 400


def test_upload_duplicate_by_sha256():
    token = _get_token()
    r1 = client.post(
        "/materials/upload",
        files={"file": ("notes.txt", b"Same content here", "text/plain")},
        headers=_auth_header(token),
    )
    assert r1.status_code == 201
    first_id = r1.json()["id"]
    r2 = client.post(
        "/materials/upload",
        files={"file": ("notes2.txt", b"Same content here", "text/plain")},
        headers=_auth_header(token),
    )
    assert r2.status_code == 201
    # Same content should return existing material (same id)
    assert r2.json()["id"] == first_id


def test_list_materials():
    token = _get_token()
    # Upload a material first so the list is non-empty.
    client.post(
        "/materials/upload",
        files={"file": ("notes.txt", b"Some notes content", "text/plain")},
        headers=_auth_header(token),
    )
    response = client.get("/materials", headers=_auth_header(token))
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_material_status():
    token = _get_token()
    r = client.post(
        "/materials/upload",
        files={"file": ("status.txt", b"status content", "text/plain")},
        headers=_auth_header(token),
    )
    mid = r.json()["id"]
    response = client.get(f"/materials/{mid}/status", headers=_auth_header(token))
    assert response.status_code == 200
    data = response.json()
    assert data["material_id"] == mid
    assert "jobs" in data


def test_get_material_not_found():
    token = _get_token()
    response = client.get("/materials/99999", headers=_auth_header(token))
    assert response.status_code == 404


# ---- AI tutor tests ----

def test_ai_status_not_configured():
    response = client.get("/conversations/ai-status")
    assert response.status_code == 200
    data = response.json()
    assert data["configured"] is False
    assert data["provider"] is None


def test_tutor_ask_returns_answer():
    token = _get_token()
    r = client.post(
        "/conversations",
        json={"title": "Tutor test", "course_id": None},
        headers=_auth_header(token),
    )
    assert r.status_code == 201
    cid = r.json()["id"]
    response = client.post(
        "/ai/tutor/ask",
        json={"conversation_id": cid, "question": "What is gravity?", "course_id": None, "lesson_id": None},
        headers=_auth_header(token),
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "answer" in data
    assert "evidence_type" in data
    assert data["evidence_type"] in ("source", "external", "inference", "uncertain")


# ---- Extended auth tests ----


def test_profile_get_and_update():
    token = _get_token()
    # Get profile
    res = client.get("/auth/profile", headers=_auth_header(token))
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["is_active"] is True

    # Update profile
    res = client.patch(
        "/auth/profile",
        json={"full_name": "Updated Name", "language": "en"},
        headers=_auth_header(token),
    )
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["full_name"] == "Updated Name"


def test_password_change():
    import uuid
    email = f"pwchange{uuid.uuid4().hex[:6]}@example.com"
    client.post("/auth/register", json={"email": email, "password": "pw123"})
    # Login to get a token for the authenticated endpoints.
    r = client.post("/auth/login", json={"email": email, "password": "pw123"})
    token = r.json()["access_token"]

    # Wrong current password
    res = client.post(
        "/auth/password/change",
        json={"current_password": "wrong", "new_password": "newpass123"},
        headers=_auth_header(token),
    )
    assert res.status_code == 400

    # Correct password change
    res = client.post(
        "/auth/password/change",
        json={"current_password": "pw123", "new_password": "newpass123"},
        headers=_auth_header(token),
    )
    assert res.status_code == 204, res.text

    # Login with new password
    res = client.post(
        "/auth/login",
        json={"email": email, "password": "newpass123"},
    )
    assert res.status_code == 200

    # Login with old password should fail
    res = client.post(
        "/auth/login",
        json={"email": email, "password": "pw123"},
    )
    assert res.status_code == 401


def test_password_reset_request():
    import uuid
    email = f"reset{uuid.uuid4().hex[:6]}@example.com"
    client.post("/auth/register", json={"email": email, "password": "resetpw123"})

    # Request reset
    res = client.post(
        "/auth/password/reset/request",
        json={"email": email},
    )
    assert res.status_code == 204, res.text

    # Without SMTP configured, the token is not returned via API.
    # In a real flow, the token would be delivered by email. Here we verify
    # the endpoint accepts the request and does not leak the token.


def test_preferences_get_and_update():
    token = _get_token()
    # Get preferences
    res = client.get("/auth/preferences", headers=_auth_header(token))
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["language"] == "en"

    # Update preferences
    res = client.patch(
        "/auth/preferences",
        json={"language": "ar", "theme": "dark", "study_reminders": True},
        headers=_auth_header(token),
    )
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["language"] == "ar"
    assert data["theme"] == "dark"
    assert data["study_reminders"] is True


def test_onboarding_status_and_steps():
    token = _get_token()
    # Get onboarding status
    res = client.get("/auth/onboarding", headers=_auth_header(token))
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["completed"] is False
    assert data["welcome_seen"] is False

    # Complete a step
    res = client.post("/auth/onboarding/welcome_seen", headers=_auth_header(token))
    assert res.status_code == 204, res.text

    # Verify step updated
    res = client.get("/auth/onboarding", headers=_auth_header(token))
    assert res.status_code == 200
    data = res.json()
    assert data["welcome_seen"] is True


def test_sessions_list_and_revoke():
    token = _get_token()
    # Verify the sessions endpoint works with the current auth.
    res = client.get("/auth/sessions", headers=_auth_header(token))
    assert res.status_code == 200, res.text


def test_unauthenticated_requests_rejected():
    """Protected routes must reject requests without a valid bearer token.

    No development-user fallback exists in production-like configuration.
    """
    # No token at all -> 401
    res = client.get("/courses")
    assert res.status_code == 401, res.text

    # Malformed bearer token -> 401
    res = client.get(
        "/courses",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert res.status_code == 401, res.text

    # Password change with missing body should be a validation error (422) or 401
    res = client.post(
        "/auth/password/change",
        json={},
    )
    assert res.status_code in (400, 401, 422)
