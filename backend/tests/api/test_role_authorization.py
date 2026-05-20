"""
T060 – Role-based authorization tests (harness trace task).

Covers:
- Unauthenticated → 401 on all protected routes
- End user → 403 on all admin-only routes
- Admin → 2xx on admin routes
- End user → 2xx on allowed routes (chat, /me)
- Admin → 2xx on /me
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

ADMIN_HEADERS = {
    "x-user-id": "admin-1",
    "x-user-email": "admin@example.com",
    "x-user-role": "admin",
}
END_USER_HEADERS = {
    "x-user-id": "user-1",
    "x-user-email": "user@example.com",
    "x-user-role": "end_user",
}

ADMIN_ROUTES: list[tuple[str, str]] = [
    ("GET", "/admin/faq-sources"),
    ("POST", "/admin/faq-sources"),
]

END_USER_ALLOWED_ROUTES: list[tuple[str, str, dict]] = [
    ("GET", "/me", {}),
    ("POST", "/chat/questions", {
        "use_case_id": "hr",
        "question_text": "What is the leave policy?",
    }),
]


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


# ---------------------------------------------------------------------------
# Unauthenticated → 401
# ---------------------------------------------------------------------------

def test_unauthenticated_cannot_access_admin_faq_sources_list(client: TestClient) -> None:
    response = client.get("/admin/faq-sources")
    assert response.status_code == 401
    assert response.json()["code"] == "unauthenticated"


def test_unauthenticated_cannot_create_faq_source(client: TestClient) -> None:
    response = client.post("/admin/faq-sources", json={})
    assert response.status_code == 401


def test_unauthenticated_cannot_access_me(client: TestClient) -> None:
    response = client.get("/me")
    assert response.status_code == 401


def test_unauthenticated_cannot_submit_chat_question(client: TestClient) -> None:
    response = client.post(
        "/chat/questions",
        json={"use_case_id": "hr", "question_text": "What is PTO?"},
    )
    assert response.status_code == 401


# ---------------------------------------------------------------------------
# End user → 403 on admin routes
# ---------------------------------------------------------------------------

def test_end_user_forbidden_from_faq_sources_list(client: TestClient) -> None:
    response = client.get("/admin/faq-sources", headers=END_USER_HEADERS)
    assert response.status_code == 403
    assert response.json()["code"] == "forbidden"


def test_end_user_forbidden_from_creating_faq_source(client: TestClient) -> None:
    response = client.post(
        "/admin/faq-sources",
        json={"name": "HR", "use_case_id": "hr", "entries": []},
        headers=END_USER_HEADERS,
    )
    assert response.status_code == 403
    assert response.json()["code"] == "forbidden"


def test_end_user_forbidden_from_faq_source_detail(client: TestClient) -> None:
    response = client.get("/admin/faq-sources/nonexistent-id", headers=END_USER_HEADERS)
    assert response.status_code == 403


def test_end_user_forbidden_from_activating_source(client: TestClient) -> None:
    response = client.post(
        "/admin/faq-sources/nonexistent-id/activate",
        headers=END_USER_HEADERS,
    )
    assert response.status_code == 403


def test_end_user_forbidden_from_deactivating_source(client: TestClient) -> None:
    response = client.post(
        "/admin/faq-sources/nonexistent-id/deactivate",
        headers=END_USER_HEADERS,
    )
    assert response.status_code == 403


def test_end_user_forbidden_from_archiving_source(client: TestClient) -> None:
    response = client.post(
        "/admin/faq-sources/nonexistent-id/archive",
        headers=END_USER_HEADERS,
    )
    assert response.status_code == 403


def test_end_user_forbidden_from_deleting_source(client: TestClient) -> None:
    response = client.delete(
        "/admin/faq-sources/nonexistent-id",
        headers=END_USER_HEADERS,
    )
    assert response.status_code == 403


# ---------------------------------------------------------------------------
# Admin → 2xx on admin routes
# ---------------------------------------------------------------------------

def test_admin_can_list_faq_sources(client: TestClient) -> None:
    response = client.get("/admin/faq-sources", headers=ADMIN_HEADERS)
    assert response.status_code == 200


def test_admin_can_access_me_endpoint(client: TestClient) -> None:
    response = client.get("/me", headers=ADMIN_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "admin-1"
    assert data["role"] == "admin"


# ---------------------------------------------------------------------------
# End user → 2xx on allowed routes
# ---------------------------------------------------------------------------

def test_end_user_can_access_me_endpoint(client: TestClient) -> None:
    response = client.get("/me", headers=END_USER_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "user-1"
    assert data["role"] == "end_user"


def test_me_response_includes_required_fields(client: TestClient) -> None:
    response = client.get("/me", headers=ADMIN_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "role" in data


def test_end_user_can_submit_chat_question(client: TestClient) -> None:
    """End user is allowed to use chat even without an active source (returns no_active_source)."""
    response = client.post(
        "/chat/questions",
        json={"use_case_id": "hr", "question_text": "What is the leave policy?"},
        headers=END_USER_HEADERS,
    )
    # Route is accessible; answer_state may be no_active_source but not 403
    assert response.status_code == 200
    assert response.json()["answer_state"] in ("answered", "unsupported", "no_active_source", "error")


def test_admin_can_also_submit_chat_question(client: TestClient) -> None:
    """Admins can also use chat — same grounding rules apply."""
    response = client.post(
        "/chat/questions",
        json={"use_case_id": "hr", "question_text": "What is the leave policy?"},
        headers=ADMIN_HEADERS,
    )
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Invalid role header → 403
# ---------------------------------------------------------------------------

def test_unknown_role_is_rejected(client: TestClient) -> None:
    headers = {
        "x-user-id": "u1",
        "x-user-email": "u@example.com",
        "x-user-role": "superuser",
    }
    response = client.get("/me", headers=headers)
    assert response.status_code == 403
