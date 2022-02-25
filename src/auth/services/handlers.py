from auth.domain import commands, events, exc
from auth.infra import crypto, models


async def handle_create_user(command: commands.CreateUser):
    hashed_password = crypto.hash_password(command.plain_password)
    try:
        user = await models.UserModel.create(
            email=command.email, password=hashed_password
        )
    except Exception:
        raise exc.UserAlreadyExistsError("An user with this email already exists")

    return [
        events.UserWasCreated(id=user.id, email=user.email),
    ]


async def handle_user_was_created_event(event: events.UserWasCreated):
    print("Handling event")


COMMAND_HANDLERS = {commands.CreateUser: handle_create_user}

EVENT_HANDLERS = {events.UserWasCreated: [handle_user_was_created_event]}
