import asyncio
import logging
from logging.config import dictConfig
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.middleware import (
    UUIDMiddleware,
    http_exception_handling_middleware,
    validation_exception_handling_middleware,
)
from config.settings import app_settings
from src.infrastructure.websockets.redis_listener import redis_listener
from src.routers.auth import router as auth_router
from src.routers.health import router as health_router
from src.routers.market_events import router as market_events_router
from src.routers.posts import router as posts_router
from src.routers.users import router as users_router

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "INFO",
            }
        },
        "root": {"handlers": ["console"], "level": "INFO"},
    }
)

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    # Start redis_listener in the background only if configured
    try:
        if app_settings.REDIS_HOST:
            asyncio.create_task(redis_listener())
    except Exception:
        logger.warning("Redis listener not started. Check REDIS_HOST configuration.")
    yield
    logger.info("Shutting down application")


app = FastAPI(
    debug=app_settings.DEBUG,
    lifespan=lifespan,
    title=app_settings.APP_NAME,
    version=app_settings.APP_VERSION,
    redirect_slashes=False,
    docs_url=None if app_settings.ENVIRONMENT == "prod" else "/docs",
    redoc_url=None if app_settings.ENVIRONMENT == "prod" else "/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.CORS_ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=app_settings.CORS_ALLOWED_METHODS.split(","),
    allow_headers=app_settings.CORS_ALLOWED_HEADERS.split(","),
)

app.add_middleware(UUIDMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await validation_exception_handling_middleware(request=request, exc=exc)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return await http_exception_handling_middleware(request=request, exc=exc)


app.include_router(prefix="/api/v1", router=auth_router)
app.include_router(prefix="/api/v1", router=health_router)
app.include_router(prefix="/api/v1", router=market_events_router)
app.include_router(prefix="/api/v1", router=posts_router)
app.include_router(prefix="/api/v1", router=users_router)


@app.get("/{full_path:path}", include_in_schema=False)
async def catch_all(full_path: str):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "success": False,
            "status_code": status.HTTP_404_NOT_FOUND,
            "message": f"The requested resource '/{full_path}' not found",
            "data": None,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
