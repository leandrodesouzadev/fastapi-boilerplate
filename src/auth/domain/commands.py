from pydantic import EmailStr

from main.domain.command import Command


class CreateUser(Command):
    email: EmailStr
    plain_password: str
