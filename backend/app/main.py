"""FastAPI application entrypoint for the FAQ Knowledge Assistant."""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status
from starlette.requests import Request

from app.api.faq_sources import reset_source_repository
from app.api.faq_sources import router as faq_sources_router
from app.api.chat import reset_chat_repository
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.feedback import reset_feedback_repository
from app.api.feedback import router as feedback_router
from app.api.me import router as me_router
from app.api.use_cases import router as use_cases_router
from app.schemas.common import ErrorResponse


def _error_response(status_code: int, code: str, message: str, details: dict | None = None) -> JSONResponse:
    payload = ErrorResponse(code=code, message=message, details=details)
    return JSONResponse(status_code=status_code, content=payload.model_dump())


def create_app() -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(title="Configurable FAQ Knowledge Assistant")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(404)
    async def not_found_handler(_: Request, __: Exception) -> JSONResponse:
        return _error_response(status.HTTP_404_NOT_FOUND, "not_found", "Resource not found")

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict) and {"code", "message"}.issubset(exc.detail):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        return _error_response(exc.status_code, "http_error", str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        def _sanitize(errors: list) -> list:
            # Pydantic v2 model_validator ctx may contain non-serializable Exception
            # instances — convert to safe strings so JSONResponse can encode them.
            safe = []
            for err in errors:
                e = dict(err)
                if "ctx" in e:
                    e["ctx"] = {k: str(v) for k, v in e["ctx"].items()}
                e.pop("url", None)
                safe.append(e)
            return safe

        return _error_response(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "validation_error",
            "Request validation failed",
            {"errors": _sanitize(exc.errors())},
        )

    app.include_router(health_router)
    app.include_router(me_router)
    app.include_router(use_cases_router)
    app.include_router(faq_sources_router)
    app.include_router(chat_router)
    app.include_router(feedback_router)
    reset_source_repository()
    reset_chat_repository()
    reset_feedback_repository()

    @app.get("/__test__/validation-error", include_in_schema=False)
    def validation_error_probe(required: int) -> dict[str, int]:
        return {"required": required}

    return app


app = create_app()
