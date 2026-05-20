from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import create_app


def test_health_endpoint_returns_status_ok() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_unknown_route_uses_shared_error_response_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json() == {
        "code": "not_found",
        "message": "Resource not found",
        "details": None,
    }


def test_validation_error_uses_shared_error_response_shape() -> None:
    client = TestClient(create_app())

    response = client.get("/__test__/validation-error")

    assert response.status_code == 422
    payload = response.json()
    assert payload["code"] == "validation_error"
    assert payload["message"] == "Request validation failed"
    assert "errors" in payload["details"]
