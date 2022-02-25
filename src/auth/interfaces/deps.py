from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .http_exc import CredentialsException
from auth.domain.entity import User
from auth.infra.models import UserModel
from auth.infra import crypto, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode_access_token(token)
    except Exception:
        raise CredentialsException()
    user = await UserModel.filter(email=data["sub"]).first()
    if not user:
        raise CredentialsException()
    return user


async def authorize_user(data: OAuth2PasswordRequestForm = Depends()) -> User:
    user = await UserModel.filter(email=data.username).first()
    if not user:
        raise CredentialsException()
    if not crypto.check_password_hash(plain=data.password, hashed=user.password):
        raise CredentialsException()
    return user.to_entity(User)


async def generate_access_token_for_authorized_user(
    user: User = Depends(authorize_user),
):
    return jwt.generate_access_token({"sub": user.email})
