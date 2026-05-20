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


def valid_source_payload(name: str = "Employee handbook FAQ") -> dict:
    return {
        "name": name,
        "description": "Approved HR answers",
        "use_case_id": "hr",
        "entries": [
            {
                "question_text": "How do I update my tax declaration?",
                "answer_text": "Open payroll self-service and submit changes before cutoff.",
                "keywords": ["tax", "payroll"],
            }
        ],
    }


def test_admin_can_create_list_update_detail_and_delete_source() -> None:
    client = TestClient(create_app())

    create_response = client.post(
        "/admin/faq-sources",
        json=valid_source_payload(),
        headers=ADMIN_HEADERS,
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"]
    assert created["name"] == "Employee handbook FAQ"
    assert created["use_case_id"] == "hr"
    assert created["status"] == "ready"
    assert created["readiness_state"] == "ready"
    assert created["is_active"] is False

    list_response = client.get("/admin/faq-sources?use_case_id=hr", headers=ADMIN_HEADERS)
    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()["items"]] == [created["id"]]

    detail_response = client.get(f"/admin/faq-sources/{created['id']}", headers=ADMIN_HEADERS)
    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["entries"][0]["question_text"] == "How do I update my tax declaration?"
    assert detail["warnings"] == []

    update_response = client.patch(
        f"/admin/faq-sources/{created['id']}",
        json={"name": "Updated HR FAQ"},
        headers=ADMIN_HEADERS,
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated HR FAQ"

    delete_response = client.delete(f"/admin/faq-sources/{created['id']}", headers=ADMIN_HEADERS)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/admin/faq-sources/{created['id']}", headers=ADMIN_HEADERS)
    assert missing_response.status_code == 404
    assert missing_response.json()["code"] == "not_found"


def test_end_user_cannot_access_admin_source_routes() -> None:
    client = TestClient(create_app())

    response = client.get("/admin/faq-sources", headers=END_USER_HEADERS)

    assert response.status_code == 403
    assert response.json()["code"] == "forbidden"


def test_delete_active_source_returns_409() -> None:
    client = TestClient(create_app())

    create_resp = client.post("/admin/faq-sources", json=valid_source_payload(), headers=ADMIN_HEADERS)
    source_id = create_resp.json()["id"]

    client.post(f"/admin/faq-sources/{source_id}/activate", headers=ADMIN_HEADERS)

    delete_resp = client.delete(f"/admin/faq-sources/{source_id}", headers=ADMIN_HEADERS)
    assert delete_resp.status_code == 409
    body = delete_resp.json()
    assert body["code"] == "source_active"


def test_delete_inactive_source_returns_204() -> None:
    client = TestClient(create_app())

    create_resp = client.post("/admin/faq-sources", json=valid_source_payload(), headers=ADMIN_HEADERS)
    source_id = create_resp.json()["id"]

    client.post(f"/admin/faq-sources/{source_id}/activate", headers=ADMIN_HEADERS)
    client.post(f"/admin/faq-sources/{source_id}/deactivate", headers=ADMIN_HEADERS)

    delete_resp = client.delete(f"/admin/faq-sources/{source_id}", headers=ADMIN_HEADERS)
    assert delete_resp.status_code == 204


def test_create_source_validates_required_entries() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/admin/faq-sources",
        json={"name": "Broken FAQ", "use_case_id": "hr", "entries": []},
        headers=ADMIN_HEADERS,
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "invalid"
    assert payload["readiness_state"] == "invalid"
    assert "At least one valid FAQ entry is required" in payload["readiness_message"]
