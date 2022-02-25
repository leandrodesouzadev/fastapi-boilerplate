from fastapi import status
from fastapi.testclient import TestClient

from auth.domain.commands import CreateUser
from auth.infra.models import UserModel

REGISTER_ENDPOINT = "/auth/register"


def test_register_requires_login(public_client: TestClient):
    response = public_client.post(REGISTER_ENDPOINT)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_register_fails_for_existent_user(
    client: TestClient, user_credentials: CreateUser
):
    response = client.post(REGISTER_ENDPOINT, json=user_credentials.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()


def test_register_suceeds_for_new_user(
    client: TestClient, user_credentials: CreateUser
):
    user_credentials.email = "New" + user_credentials.email
    response = client.post(REGISTER_ENDPOINT, json=user_credentials.dict())

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert UserModel.filter(email=user_credentials.email).exists()
