import uuid
from main.domain.event import Event


class UserWasCreated(Event):
    id: uuid.UUID
    email: str
