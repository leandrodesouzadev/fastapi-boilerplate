from datetime import timedelta
from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_TITLE: str
    APP_VERSION: str
    APP_DESCRIPTION: str
    DEBUG: bool
    SECRET_KEY: str

    USE_CORS_MIDDLEWARE: bool = False
    CORS_ALLOW_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True

    USE_HTTPS_REDIRECT_MIDDLEWARE: bool = False
    USE_TRUSTED_HOST_MIDDLEWARE: bool = False
    ALLOWED_HOSTS: List[str] = ["*"]

    DATABASE_URL: str
    TORTOISE_MODELS_MODULES: List[str] = ["auth.infra.models"]
    TORTOISE_GENERATE_SCHEMAS: bool = False
    TORTOISE_ADD_EXCEPTION_HANDLERS: bool = False
    TORTOISE_USE_TIMEZONE: bool = True

    JWT_ACCESS_TOKEN_MINUTES_LIFESPAN: float = 15
    JWT_ALGORITHM: str = "HS256"

    ROUTER_MODULES: List[str] = ["auth.interfaces.http"]

    @property
    def jwt_access_token_lifespan_timedelta(self) -> timedelta:
        return timedelta(minutes=self.JWT_ACCESS_TOKEN_MINUTES_LIFESPAN)


settings = Settings()
