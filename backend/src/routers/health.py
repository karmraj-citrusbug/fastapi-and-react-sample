from fastapi import APIRouter

from config.settings import app_settings


router = APIRouter(prefix="/health", tags=["Health"], include_in_schema=False)


@router.get("/")
async def healthcheck():
    return {
        "status": "ok",
        "app": app_settings.APP_NAME,
        "version": app_settings.APP_VERSION,
        "environment": app_settings.ENVIRONMENT,
    }
