from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .conf import settings


def get_wsgi_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        debug=settings.DEBUG,
    )

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse("/docs")

    return app
