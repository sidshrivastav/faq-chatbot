from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from starlette.datastructures import Headers

from app.auth.models import CurrentUser
from app.domain.enums import Role


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"code": code, "message": message, "details": None},
    )


def parse_user_from_headers(headers: Headers) -> CurrentUser:
    user_id = headers.get("x-user-id")
    email = headers.get("x-user-email")
    role_value = headers.get("x-user-role")

    if not user_id or not email or not role_value:
        raise _error(
            status.HTTP_401_UNAUTHORIZED,
            "unauthenticated",
            "Authentication is required",
        )

    try:
        role = Role(role_value)
    except ValueError as exc:
        raise _error(status.HTTP_403_FORBIDDEN, "forbidden", "Unsupported user role") from exc

    return CurrentUser(
        id=user_id,
        email=email,
        display_name=headers.get("x-user-name"),
        role=role,
    )


def get_current_user(request: Request) -> CurrentUser:
    return parse_user_from_headers(request.headers)


def require_admin_user(current_user: CurrentUser) -> CurrentUser:
    if current_user.role != Role.ADMIN:
        raise _error(status.HTTP_403_FORBIDDEN, "forbidden", "Admin role required")
    return current_user


def require_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    return require_admin_user(current_user)
