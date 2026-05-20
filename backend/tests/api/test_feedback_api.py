"""
T042 – API tests for POST /answers/{answer_id}/feedback.

Covers:
- Helpful feedback on an answered question
- Unhelpful feedback with an optional comment
- Feedback on an unanswered (no_active_source) response
- Missing answer → 404
- Unauthenticated → 401
- Validation failures (invalid rating)
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

END_USER_HEADERS = {
    "x-user-id": "user-1",
    "x-user-email": "user@example.com",
    "x-user-role": "end_user",
}
ADMIN_HEADERS = {
    "x-user-id": "admin-1",
    "x-user-email": "admin@example.com",
    "x-user-role": "admin",
}


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def _create_and_activate_source(client: TestClient) -> str:
    source = client.post(
        "/admin/faq-sources",
        headers=ADMIN_HEADERS,
        json={
            "name": "HR handbook",
            "use_case_id": "hr",
            "entries": [
                {
                    "question_text": "How do I request parental leave?",
                    "answer_text": "Submit the request in Workday.",
                    "keywords": ["leave", "parental"],
                }
            ],
        },
    )
    assert source.status_code == 201
    source_id = source.json()["id"]
    activate = client.post(f"/admin/faq-sources/{source_id}/activate", headers=ADMIN_HEADERS)
    assert activate.status_code == 200
    return source_id


def _ask_question(client: TestClient, *, question_text: str = "What is the process for parental leave?") -> dict:
    response = client.post(
        "/chat/questions",
        headers=END_USER_HEADERS,
        json={"use_case_id": "hr", "question_text": question_text},
    )
    assert response.status_code == 200
    return response.json()


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_helpful_feedback_returns_201(client: TestClient) -> None:
    _create_and_activate_source(client)
    answer = _ask_question(client)
    answer_id = answer["answer_id"]

    response = client.post(
        f"/answers/{answer_id}/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "helpful"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == "helpful"
    assert data["answer_id"] == answer_id


def test_unhelpful_feedback_with_comment(client: TestClient) -> None:
    _create_and_activate_source(client)
    answer = _ask_question(client)
    answer_id = answer["answer_id"]

    response = client.post(
        f"/answers/{answer_id}/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "unhelpful", "comment": "The answer was too vague."},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == "unhelpful"
    assert data["comment"] == "The answer was too vague."


def test_feedback_response_includes_context_fields(client: TestClient) -> None:
    _create_and_activate_source(client)
    answer = _ask_question(client)
    answer_id = answer["answer_id"]

    response = client.post(
        f"/answers/{answer_id}/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "helpful"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "answer_id" in data
    assert "use_case_id" in data
    assert "rating" in data


def test_feedback_on_no_active_source_answer(client: TestClient) -> None:
    """Feedback is allowed even when answer_state is no_active_source."""
    answer = _ask_question(client, question_text="What is PTO?")
    assert answer["answer_state"] == "no_active_source"
    answer_id = answer["answer_id"]

    response = client.post(
        f"/answers/{answer_id}/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "unhelpful", "comment": "No answer was found."},
    )
    assert response.status_code == 201
    assert response.json()["rating"] == "unhelpful"


def test_admin_can_also_submit_feedback(client: TestClient) -> None:
    _create_and_activate_source(client)
    answer = client.post(
        "/chat/questions",
        headers=ADMIN_HEADERS,
        json={"use_case_id": "hr", "question_text": "What is the process for parental leave?"},
    ).json()

    response = client.post(
        f"/answers/{answer['answer_id']}/feedback",
        headers=ADMIN_HEADERS,
        json={"rating": "helpful"},
    )
    assert response.status_code == 201


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

def test_feedback_on_missing_answer_returns_404(client: TestClient) -> None:
    response = client.post(
        "/answers/nonexistent-id/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "helpful"},
    )
    assert response.status_code == 404
    assert response.json()["code"] == "not_found"


def test_unauthenticated_feedback_returns_401(client: TestClient) -> None:
    response = client.post(
        "/answers/any-id/feedback",
        json={"rating": "helpful"},
    )
    assert response.status_code == 401


def test_invalid_rating_returns_422(client: TestClient) -> None:
    response = client.post(
        "/answers/any-id/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "maybe"},
    )
    assert response.status_code == 422


def test_missing_rating_returns_422(client: TestClient) -> None:
    response = client.post(
        "/answers/any-id/feedback",
        headers=END_USER_HEADERS,
        json={"comment": "nice"},
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# TC01 – add-feedback-reasons: structured reason field
# ---------------------------------------------------------------------------

def test_unhelpful_feedback_with_valid_reason_returns_201(client: TestClient) -> None:
    _create_and_activate_source(client)
    answer = _ask_question(client)

    response = client.post(
        f"/answers/{answer['answer_id']}/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "unhelpful", "reason": "not_specific_enough"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == "unhelpful"
    assert data["reason"] == "not_specific_enough"


def test_unhelpful_feedback_without_reason_has_null_reason(client: TestClient) -> None:
    _create_and_activate_source(client)
    answer = _ask_question(client)

    response = client.post(
        f"/answers/{answer['answer_id']}/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "unhelpful"},
    )
    assert response.status_code == 201
    assert response.json()["reason"] is None


def test_helpful_feedback_with_reason_returns_422(client: TestClient) -> None:
    response = client.post(
        "/answers/any-id/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "helpful", "reason": "not_specific_enough"},
    )
    assert response.status_code == 422


def test_invalid_reason_value_returns_422(client: TestClient) -> None:
    response = client.post(
        "/answers/any-id/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "unhelpful", "reason": "not_a_valid_reason"},
    )
    assert response.status_code == 422


def test_all_five_reason_values_are_accepted(client: TestClient) -> None:
    reasons = [
        "incorrect_answer",
        "not_specific_enough",
        "missing_from_faq",
        "confusing_response",
        "outdated_source",
    ]
    _create_and_activate_source(client)
    for reason in reasons:
        c = TestClient(create_app())
        _create_and_activate_source(c)
        answer = _ask_question(c)
        response = c.post(
            f"/answers/{answer['answer_id']}/feedback",
            headers=END_USER_HEADERS,
            json={"rating": "unhelpful", "reason": reason},
        )
        assert response.status_code == 201, f"reason={reason} failed"
        assert response.json()["reason"] == reason


def test_feedback_response_includes_reason_field(client: TestClient) -> None:
    _create_and_activate_source(client)
    answer = _ask_question(client)

    response = client.post(
        f"/answers/{answer['answer_id']}/feedback",
        headers=END_USER_HEADERS,
        json={"rating": "helpful"},
    )
    assert response.status_code == 201
    assert "reason" in response.json()
