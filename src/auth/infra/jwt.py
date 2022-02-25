from datetime import datetime
from jose import jwt

from main.infra.conf import settings


def generate_access_token(data: dict) -> str:
    to_encode = data.copy()
    expires = datetime.utcnow() + settings.jwt_access_token_lifespan_timedelta

    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
