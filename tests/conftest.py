import asyncio
import os
import pytest
from typing import Generator

from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer
from dotenv import load_dotenv

load_dotenv()


from auth.domain.commands import CreateUser
from main.infra.conf import settings
from auth.interfaces.deps import get_current_user
from main.infra.bootstrap import bootstrap_message_bus
from main.infra.bus import MessageBus
from auth.infra.models import UserModel
from main.interfaces.http import app
from auth.services.handlers import handle_create_user


@pytest.fixture(scope="function", autouse=True)
def initialize_tests(request):
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(settings.TORTOISE_MODELS_MODULES, db_url=db_url)
    request.addfinalizer(finalizer)


@pytest.fixture()
def public_client() -> TestClient:
    """An TestClient for making http requests"""

    return TestClient(app)


@pytest.fixture()
def client(public_client: TestClient, create_user, user_credentials: CreateUser):
    data = {
        "username": user_credentials.email,
        "password": user_credentials.plain_password,
    }
    response = public_client.post("/auth/token", data=data)
    assert response.status_code == 200
    jsn = response.json()
    public_client.headers.update({"Authorization": f"Bearer {jsn['access_token']}"})
    return public_client


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    yield asyncio.get_event_loop()


@pytest.fixture()
def bus() -> MessageBus:
    return bootstrap_message_bus()


@pytest.fixture()
def user_credentials() -> CreateUser:
    return CreateUser(email="johndoe@email.com", plain_password="JohnRules434")


@pytest.fixture()
def create_user(
    user_credentials: CreateUser,
    event_loop: asyncio.AbstractEventLoop,
) -> UserModel:
    event_loop.run_until_complete(handle_create_user(user_credentials))
    return UserModel.filter(email=user_credentials.email).first()
