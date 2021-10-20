import pytest
from pytest_factoryboy import register
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .factories import UserFactory

register(UserFactory)


@pytest.fixture
def mock_user():
    def mock(**kwargs):
        u = UserFactory.create(**kwargs)
        u.set_password(u.password)
        u.save()
        return u

    return mock


@pytest.fixture
def auth_client():
    from rest_framework.test import APIClient

    def get(**kwargs):
        client = APIClient()
        res = client.post(
            "/api/v1/auth/login/",
            {"username": kwargs["username"], "password": kwargs["password"]},
        )
        if "access" in res.data:
            client.credentials(HTTP_AUTHORIZATION=f"JWT {res.data['access']}")
        else:
            raise AuthenticationFailed
        return client

    return get
