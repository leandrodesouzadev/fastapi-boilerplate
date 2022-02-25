from fastapi.routing import APIRouter
from auth.interfaces.deps import get_current_user


class RequiresAuthenticationRouter(APIRouter):
    def __init__(self, **kwargs):
        """Check `APIRouter` for kwargs specs"""
        dependencies = kwargs.get("dependencies", [])
        dependencies.append(get_current_user)
        kwargs["dependencies"] = dependencies
        super().__init__(**kwargs)
