from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.core.middleware import request_logging_middleware
from app.core.errors import ApiError, api_error_handler
from app.db.session import ping_database


settings = get_settings()
configure_logging(settings)
logger = get_logger(__name__)
app = FastAPI(title="AI Portal API", version=settings.app_version)
app.add_exception_handler(ApiError, api_error_handler)

app.middleware("http")(request_logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[settings.trace_header],
)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    logger.debug("health_check")
    return {"status": "ok", "service": settings.app_name, "environment": settings.app_env}


app.include_router(api_router, prefix=settings.api_prefix)


@app.on_event("startup")
async def log_startup() -> None:
    await ping_database()
    logger.info(
        "application_started",
        service=settings.app_name,
        environment=settings.app_env,
        log_file=f"{settings.log_dir}/{settings.log_file_name}",
    )
