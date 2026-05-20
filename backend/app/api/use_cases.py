from __future__ import annotations

from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.auth.models import CurrentUser
from app.api.faq_sources import get_source_service
from app.schemas.use_case import UseCaseListResponse, UseCaseSummary
from app.services.source_service import SourceService

router = APIRouter(prefix="/use-cases", tags=["Use Cases"])

USE_CASES = [
    ("hr", "HR", "Human resources policies and employee support"),
    ("it_support", "IT Support", "Workplace technology and account support"),
    ("product_support", "Product Support", "Product usage and troubleshooting"),
    ("admissions", "Admissions", "Admissions and enrollment questions"),
]


@router.get("", response_model=UseCaseListResponse)
def list_use_cases(
    _: CurrentUser = Depends(get_current_user),
    source_service: SourceService = Depends(get_source_service),
) -> UseCaseListResponse:
    items: list[UseCaseSummary] = []
    for use_case_id, name, description in USE_CASES:
        active_sources = source_service.list_sources(use_case_id=use_case_id, active=True)
        active_source = active_sources[0] if active_sources else None
        items.append(
            UseCaseSummary(
                id=use_case_id,
                name=name,
                description=description,
                has_active_source=active_source is not None,
                active_source_name=active_source.name if active_source else None,
            )
        )
    return UseCaseListResponse(items=items)
