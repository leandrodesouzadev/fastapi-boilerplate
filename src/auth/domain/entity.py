from pydantic import EmailStr
from main.domain import entity


class User(entity.Entity):
    email: EmailStr
    password: str
