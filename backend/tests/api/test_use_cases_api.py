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


def test_use_cases_reports_active_source_for_end_user() -> None:
    client = TestClient(create_app())
    create_response = client.post(
        "/admin/faq-sources",
        headers=ADMIN_HEADERS,
        json={
            "name": "HR handbook",
            "use_case_id": "hr",
            "entries": [
                {
                    "question_text": "How do I request parental leave?",
                    "answer_text": "Submit the request in Workday.",
                }
            ],
        },
    )
    assert create_response.status_code == 201
    source_id = create_response.json()["id"]
    activate_response = client.post(f"/admin/faq-sources/{source_id}/activate", headers=ADMIN_HEADERS)
    assert activate_response.status_code == 200

    response = client.get("/use-cases", headers=END_USER_HEADERS)

    assert response.status_code == 200
    hr = next(item for item in response.json()["items"] if item["id"] == "hr")
    assert hr["name"] == "HR"
    assert hr["has_active_source"] is True
    assert hr["active_source_name"] == "HR handbook"


def test_use_cases_requires_authentication() -> None:
    client = TestClient(create_app())

    response = client.get("/use-cases")

    assert response.status_code == 401
