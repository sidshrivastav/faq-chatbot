from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.auth.dependencies import require_admin
from app.auth.models import CurrentUser
from app.repositories.faq_sources import InMemoryFaqSourceRepository
from app.schemas.faq_source import FaqSourceCreate, FaqSourceDetail, FaqSourceListResponse, FaqSourceUpdate
from app.services.source_service import ActiveSourceDeletionError, SourceNotFoundError, SourceNotReadyError, SourceService

router = APIRouter(prefix="/admin/faq-sources", tags=["FAQ Sources"])

_repository = InMemoryFaqSourceRepository()


def get_source_service() -> SourceService:
    return SourceService(_repository)


def reset_source_repository() -> None:
    _repository.clear()


def _not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"code": "not_found", "message": "FAQ source not found", "details": None},
    )


@router.get("", response_model=FaqSourceListResponse)
def list_sources(
    use_case_id: str | None = None,
    source_status: str | None = Query(default=None, alias="status"),
    active: bool | None = None,
    _: CurrentUser = Depends(require_admin),
    service: SourceService = Depends(get_source_service),
) -> FaqSourceListResponse:
    return FaqSourceListResponse(items=service.list_sources(use_case_id=use_case_id, status=source_status, active=active))


@router.post("", response_model=FaqSourceDetail, status_code=status.HTTP_201_CREATED)
def create_source(
    payload: FaqSourceCreate,
    current_user: CurrentUser = Depends(require_admin),
    service: SourceService = Depends(get_source_service),
) -> FaqSourceDetail:
    return service.create_source(payload, user_id=current_user.id)


@router.get("/{source_id}", response_model=FaqSourceDetail)
def get_source(
    source_id: str,
    _: CurrentUser = Depends(require_admin),
    service: SourceService = Depends(get_source_service),
) -> FaqSourceDetail:
    try:
        return service.get_source(source_id)
    except SourceNotFoundError as exc:
        raise _not_found() from exc


@router.patch("/{source_id}", response_model=FaqSourceDetail)
def update_source(
    source_id: str,
    payload: FaqSourceUpdate,
    current_user: CurrentUser = Depends(require_admin),
    service: SourceService = Depends(get_source_service),
) -> FaqSourceDetail:
    try:
        return service.update_source(source_id, payload, user_id=current_user.id)
    except SourceNotFoundError as exc:
        raise _not_found() from exc


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(
    source_id: str,
    _: CurrentUser = Depends(require_admin),
    service: SourceService = Depends(get_source_service),
) -> Response:
    try:
        service.delete_source(source_id)
    except SourceNotFoundError as exc:
        raise _not_found() from exc
    except ActiveSourceDeletionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "source_active", "message": "FAQ source is currently active and cannot be deleted. Deactivate or archive it first.", "details": None},
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{source_id}/activate", response_model=FaqSourceDetail)
def activate_source(
    source_id: str,
    _: CurrentUser = Depends(require_admin),
    service: SourceService = Depends(get_source_service),
) -> FaqSourceDetail:
    try:
        return service.activate_source(source_id)
    except SourceNotFoundError as exc:
        raise _not_found() from exc
    except SourceNotReadyError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "source_not_ready", "message": "FAQ source is not ready for activation", "details": None},
        ) from exc


@router.post("/{source_id}/deactivate", response_model=FaqSourceDetail)
def deactivate_source(
    source_id: str,
    _: CurrentUser = Depends(require_admin),
    service: SourceService = Depends(get_source_service),
) -> FaqSourceDetail:
    try:
        return service.deactivate_source(source_id)
    except SourceNotFoundError as exc:
        raise _not_found() from exc


@router.post("/{source_id}/archive", response_model=FaqSourceDetail)
def archive_source(
    source_id: str,
    _: CurrentUser = Depends(require_admin),
    service: SourceService = Depends(get_source_service),
) -> FaqSourceDetail:
    try:
        return service.archive_source(source_id)
    except SourceNotFoundError as exc:
        raise _not_found() from exc
