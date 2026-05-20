from __future__ import annotations

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


def create_source(client: TestClient, *, name: str, use_case_id: str, question_text: str, answer_text: str) -> dict:
    response = client.post(
        "/admin/faq-sources",
        headers=ADMIN_HEADERS,
        json={
            "name": name,
            "use_case_id": use_case_id,
            "entries": [
                {
                    "question_text": question_text,
                    "answer_text": answer_text,
                    "keywords": ["policy"],
                }
            ],
        },
    )
    assert response.status_code == 201
    return response.json()


def activate_source(client: TestClient, source_id: str) -> dict:
    response = client.post(f"/admin/faq-sources/{source_id}/activate", headers=ADMIN_HEADERS)
    assert response.status_code == 200
    return response.json()


def test_chat_question_returns_grounded_answer_for_active_source() -> None:
    client = TestClient(create_app())
    source = create_source(
        client,
        name="HR handbook",
        use_case_id="hr",
        question_text="How do I request parental leave?",
        answer_text="Submit the request in Workday.",
    )
    activate_source(client, source["id"])

    response = client.post(
        "/chat/questions",
        headers=END_USER_HEADERS,
        json={"use_case_id": "hr", "question_text": "What is the process for parental leave?"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["answer_state"] == "answered"
    assert payload["source_id"] == source["id"]
    assert payload["source_name"] == "HR handbook"
    assert payload["message"] == "Submit the request in Workday."
    assert len(payload["retrieved_entries"]) == 1
    assert payload["feedback_allowed"] is True


def test_chat_question_returns_unsupported_when_active_source_has_no_match() -> None:
    client = TestClient(create_app())
    source = create_source(
        client,
        name="HR handbook",
        use_case_id="hr",
        question_text="How do I request parental leave?",
        answer_text="Submit the request in Workday.",
    )
    activate_source(client, source["id"])

    response = client.post(
        "/chat/questions",
        headers=END_USER_HEADERS,
        json={"use_case_id": "hr", "question_text": "How do I reset my laptop password?"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["answer_state"] == "unsupported"
    assert payload["message"] == "I couldn't find an answer in the active FAQ source."
    assert payload["retrieved_entries"] == []
    assert payload["feedback_allowed"] is True


def test_chat_question_returns_no_active_source_when_use_case_has_no_active_source() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/chat/questions",
        headers=END_USER_HEADERS,
        json={"use_case_id": "hr", "question_text": "Where do I submit expenses?"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["answer_state"] == "no_active_source"
    assert "No active FAQ source" in payload["message"]
    assert payload["feedback_allowed"] is True


def test_chat_question_excludes_inactive_matching_sources() -> None:
    client = TestClient(create_app())
    inactive_matching_source = create_source(
        client,
        name="HR leave archive",
        use_case_id="hr",
        question_text="How do I reset my password?",
        answer_text="Use the password reset portal.",
    )
    active_unrelated_source = create_source(
        client,
        name="HR handbook",
        use_case_id="hr",
        question_text="How do I book time off?",
        answer_text="Use the time-off portal.",
    )
    activate_source(client, active_unrelated_source["id"])

    response = client.post(
        "/chat/questions",
        headers=END_USER_HEADERS,
        json={"use_case_id": "hr", "question_text": "How do I reset my password?"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["answer_state"] == "unsupported"
    assert payload["source_id"] == active_unrelated_source["id"]
    assert payload["source_id"] != inactive_matching_source["id"]


def test_chat_question_requires_authentication() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/chat/questions",
        json={"use_case_id": "hr", "question_text": "Where do I submit expenses?"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "unauthenticated"
