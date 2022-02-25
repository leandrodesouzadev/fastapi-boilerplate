from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from auth.domain import commands, entity, exc
from . import deps
from main.infra.bootstrap import bootstrap_message_bus


router = APIRouter(prefix="/auth")
bus = bootstrap_message_bus()


@router.post("/token")
async def login_for_access_token(
    access_token: str = Depends(deps.generate_access_token_for_authorized_user),
):
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", status_code=201)
async def register(
    command: commands.CreateUser, user: entity.User = Depends(deps.get_current_user)
):
    try:
        await bus.handle(command)
    except exc.UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=e.args)
    return
