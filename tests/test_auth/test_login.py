from fastapi import status
from fastapi.testclient import TestClient

from auth.domain.commands import CreateUser


def test_bad_credentials(public_client: TestClient, create_user):
    response = public_client.post(
        "/auth/token",
        data={
            "username": "username",
            "password": "password",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_good_credentials(
    public_client: TestClient, user_credentials: CreateUser, create_user
):
    response = public_client.post(
        "/auth/token",
        data={
            "username": user_credentials.email,
            "password": user_credentials.plain_password,
        },
    )
    assert response.status_code == status.HTTP_200_OK
