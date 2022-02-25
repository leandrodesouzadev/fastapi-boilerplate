from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .conf import settings


def register_orm_on_wsgi_application(app: FastAPI) -> None:
    register_tortoise(
        app=app,
        generate_schemas=settings.TORTOISE_GENERATE_SCHEMAS,
        add_exception_handlers=settings.TORTOISE_ADD_EXCEPTION_HANDLERS,
        config={
            "apps": {"models": {"models": settings.TORTOISE_MODELS_MODULES}},
            "connections": {"default": settings.DATABASE_URL},
            "use_tz": settings.TORTOISE_USE_TIMEZONE,
        },
    )
