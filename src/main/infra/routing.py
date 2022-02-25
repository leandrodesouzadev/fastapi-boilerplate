import importlib
from fastapi import FastAPI

from .conf import settings


def inject_routers_on_wsgi_application(app: FastAPI) -> None:
    for module_path in settings.ROUTER_MODULES:
        module = importlib.import_module(module_path)
        if not module:
            raise ImportError("Cannot import router module: {}".format(module_path))
        router = getattr(module, "router")
        if not router:
            raise ImportError(
                "Cannot find 'router' variable on module: {}".format(module_path)
            )
        app.include_router(router)
