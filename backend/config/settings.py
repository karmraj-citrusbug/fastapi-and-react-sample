import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    # CORS Configurations
    CORS_ALLOWED_ORIGINS: str = ""
    CORS_ALLOWED_METHODS: str = ""
    CORS_ALLOWED_HEADERS: str = ""

    # APP Configurations
    APP_NAME: str = ""
    APP_VERSION: str = ""
    DEBUG: bool = True
    ENVIRONMENT: str = ""

    # Logger Configurations
    LOGGER_NAME: str = ""

    # Database Configurations
    DB_NAME: str = ""
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: str = ""

    # Auth Configurations
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = ""
    RESET_TOKEN_EXPIRY_HOURS: int = 0
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0

    # OpenAI Configurations
    OPENAI_API_KEY: str = ""

    # ThirdParty News API Configurations
    API_CALL_INTERVAL_DURATION_IN_SECONDS: int = 5
    ALPHAVANTAGE_API_KEY: str = ""
    ALPHAVANTAGE_API_BASE_URL: str = ""
    NEWS_API_KEY: str = ""
    NEWS_API_BASE_URL: str = ""
    FETCH_STATIC_DATA: bool = True

    # Sendgrid Configurations
    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = ""
    SENDGRID_FORGOT_PASSWORD_TEMPLATE_ID: str = ""
    SENDGRID_VERIFY_EMAIL_TEMPLATE_ID: str = ""

    # Frontend Configurations
    FRONTEND_URL: str = ""

    # Redis Configurations
    REDIS_BROKER_URL: str = ""
    REDIS_HOST: str = ""

    # Dynamically set the environment file
    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT', 'local')}"
    )


# Load settings
app_settings = AppSettings()
