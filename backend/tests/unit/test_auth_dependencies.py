from __future__ import annotations

import pytest
from fastapi import HTTPException
from starlette.datastructures import Headers

from app.auth.dependencies import parse_user_from_headers, require_admin_user
from app.domain.enums import Role


def test_parse_user_from_headers_returns_current_user() -> None:
    user = parse_user_from_headers(
        Headers(
            {
                "x-user-id": "user-1",
                "x-user-email": "admin@example.com",
                "x-user-name": "Admin User",
                "x-user-role": "admin",
            }
        )
    )

    assert user.id == "user-1"
    assert user.email == "admin@example.com"
    assert user.display_name == "Admin User"
    assert user.role == Role.ADMIN


def test_parse_user_from_headers_requires_identity() -> None:
    with pytest.raises(HTTPException) as exc_info:
        parse_user_from_headers(Headers({}))

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail["code"] == "unauthenticated"


def test_parse_user_from_headers_rejects_unknown_role() -> None:
    with pytest.raises(HTTPException) as exc_info:
        parse_user_from_headers(
            Headers(
                {
                    "x-user-id": "user-1",
                    "x-user-email": "user@example.com",
                    "x-user-role": "owner",
                }
            )
        )

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail["code"] == "forbidden"


def test_require_admin_user_allows_admin_and_rejects_end_user() -> None:
    admin = parse_user_from_headers(
        Headers(
            {
                "x-user-id": "admin-1",
                "x-user-email": "admin@example.com",
                "x-user-role": "admin",
            }
        )
    )
    end_user = parse_user_from_headers(
        Headers(
            {
                "x-user-id": "user-1",
                "x-user-email": "user@example.com",
                "x-user-role": "end_user",
            }
        )
    )

    assert require_admin_user(admin) is admin
    with pytest.raises(HTTPException) as exc_info:
        require_admin_user(end_user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail["code"] == "forbidden"
