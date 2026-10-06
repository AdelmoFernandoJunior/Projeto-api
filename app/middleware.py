"""Middleware de observabilidade das requisições HTTP."""
import logging
import time
from uuid import uuid4

from fastapi import Request
from starlette.responses import Response


logger = logging.getLogger("api.requests")


async def log_requests(request: Request, call_next) -> Response:
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    inicio = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        duracao_ms = (time.perf_counter() - inicio) * 1000
        logger.exception(
            "request_failed request_id=%s method=%s path=%s duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            duracao_ms,
        )
        raise

    duracao_ms = (time.perf_counter() - inicio) * 1000
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_completed request_id=%s method=%s path=%s status_code=%s duration_ms=%.2f",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duracao_ms,
    )
    return response
