"""HTTP middleware shared by every API route."""

from __future__ import annotations

from time import perf_counter
from uuid import uuid4

from fastapi import Request
from structlog.contextvars import bind_contextvars, clear_contextvars

from app.core.config import get_settings
from app.core.logging import get_logger


logger = get_logger(__name__)


async def request_logging_middleware(request: Request, call_next):
    """Attach a trace ID and log one structured record for every request."""

    trace_header = get_settings().trace_header
    trace_id = request.headers.get(trace_header) or uuid4().hex
    clear_contextvars()
    bind_contextvars(trace_id=trace_id)
    started_at = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception(
            "http_request_failed",
            method=request.method,
            path=request.url.path,
            duration_ms=round((perf_counter() - started_at) * 1000, 2),
        )
        clear_contextvars()
        raise

    duration_ms = round((perf_counter() - started_at) * 1000, 2)
    response.headers[trace_header] = trace_id
    logger.info(
        "http_request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=duration_ms,
    )
    clear_contextvars()
    return response
