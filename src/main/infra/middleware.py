from fastapi import FastAPI
from fastapi.middleware import cors, httpsredirect, trustedhost
from .conf import settings


def add_middlewares_to_wsgi_application(app: FastAPI) -> None:
    if settings.USE_CORS_MIDDLEWARE:
        app.add_middleware(
            cors.CORSMiddleware,
            allow_origins=settings.CORS_ALLOW_ORIGINS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        )

    if settings.USE_HTTPS_REDIRECT_MIDDLEWARE:
        app.add_middleware(httpsredirect.HTTPSRedirectMiddleware)

    if settings.USE_TRUSTED_HOST_MIDDLEWARE:
        app.add_middleware(
            trustedhost.TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS,
        )
