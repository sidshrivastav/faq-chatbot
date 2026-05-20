from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app
from tests.api.test_faq_sources_api import ADMIN_HEADERS, valid_source_payload


def test_activate_ready_source_deactivates_previous_active_source_for_use_case() -> None:
    client = TestClient(create_app())

    first = client.post(
        "/admin/faq-sources",
        json=valid_source_payload("HR FAQ v1"),
        headers=ADMIN_HEADERS,
    ).json()
    second = client.post(
        "/admin/faq-sources",
        json=valid_source_payload("HR FAQ v2"),
        headers=ADMIN_HEADERS,
    ).json()

    first_activation = client.post(
        f"/admin/faq-sources/{first['id']}/activate",
        headers=ADMIN_HEADERS,
    )
    assert first_activation.status_code == 200
    assert first_activation.json()["is_active"] is True
    assert first_activation.json()["status"] == "active"

    second_activation = client.post(
        f"/admin/faq-sources/{second['id']}/activate",
        headers=ADMIN_HEADERS,
    )
    assert second_activation.status_code == 200
    assert second_activation.json()["is_active"] is True

    first_detail = client.get(f"/admin/faq-sources/{first['id']}", headers=ADMIN_HEADERS).json()
    assert first_detail["is_active"] is False
    assert first_detail["status"] == "inactive"


def test_cannot_activate_invalid_source() -> None:
    client = TestClient(create_app())

    invalid = client.post(
        "/admin/faq-sources",
        json={"name": "Empty FAQ", "use_case_id": "facilities", "entries": []},
        headers=ADMIN_HEADERS,
    ).json()

    response = client.post(f"/admin/faq-sources/{invalid['id']}/activate", headers=ADMIN_HEADERS)

    assert response.status_code == 409
    assert response.json()["code"] == "source_not_ready"


def test_deactivate_and_archive_source_update_state() -> None:
    client = TestClient(create_app())
    source = client.post(
        "/admin/faq-sources",
        json=valid_source_payload("Device support FAQ"),
        headers=ADMIN_HEADERS,
    ).json()

    client.post(f"/admin/faq-sources/{source['id']}/activate", headers=ADMIN_HEADERS)

    deactivated = client.post(
        f"/admin/faq-sources/{source['id']}/deactivate",
        headers=ADMIN_HEADERS,
    )
    assert deactivated.status_code == 200
    assert deactivated.json()["is_active"] is False
    assert deactivated.json()["status"] == "inactive"

    archived = client.post(f"/admin/faq-sources/{source['id']}/archive", headers=ADMIN_HEADERS)
    assert archived.status_code == 200
    assert archived.json()["status"] == "archived"
