import factory
import pytest
from rest_framework import status
from faker import Factory as FakerFactory
from pytest_factoryboy import register
from apps.accounts.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.faker.Faker("name")
    password = factory.faker.Faker("password")


register(UserFactory)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test,username,password,password2,result",
    [
        ("password mismatch", "rahil", "password", "pass", False),
        ("missing username", "", "password", "pass", False),
        ("missing password", "rahil", "", "password", False),
        ("missing password2", "rahil", "password", "", False),
        ("success case", "rahil", "password", "password", True),
    ],
)
def test_signup(test, username, password, password2, result, client, user_factory):
    res = client.post(
        "/api/v1/auth/signup/",
        {"username": username, "password": password, "password2": password2},
    )

    expected = status.HTTP_200_OK if result else status.HTTP_400_BAD_REQUEST
    assert res.status_code == expected


@pytest.mark.django_db
def test_duplicate_signup(client, user_factory):
    user = user_factory.build()
    req = {
        "username": user.username,
        "password": user.password,
        "password2": user.password,
    }
    res = client.post("/api/v1/auth/signup/", req)
    res = client.post("/api/v1/auth/signup/", req)

    expected = status.HTTP_400_BAD_REQUEST
    assert res.status_code == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test,username,password,result",
    [
        ("success case", "rahil", "awesome", status.HTTP_200_OK),
        ("missing password field", "rahil", "", status.HTTP_400_BAD_REQUEST),
        ("missing username and password", "", "", status.HTTP_400_BAD_REQUEST),
        ("missing username", "", "slkmdlkm", status.HTTP_400_BAD_REQUEST),
        ("invalid password", "rahil", "slkmdlkm", status.HTTP_401_UNAUTHORIZED),
        ("invalid username", "rahillskdm", "awesome", status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_login(test, username, password, result, client):
    client.post(
        "/api/v1/auth/signup/",
        {"username": "rahil", "password": "awesome", "password2": "awesome"},
    )
    res = client.post(
        "/api/v1/auth/login/",
        {"username": username, "password": password},
    )
    assert res.status_code == result

    if result == status.HTTP_200_OK:
        res_data = res.data
        assert (
            res_data["refresh"] != ""
            and res_data["refresh"] is not None
            and res_data["access"] != ""
            and res_data["access"] is not None
        )
    elif result == status.HTTP_400_BAD_REQUEST:
        assert res.data
