import pytest
from faker import Faker
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

fake = Faker()


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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test,user,expected",
    [
        (
            "should fail with empty new and old password",
            {"new_password": "", "password": ""},
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "should fail with empty old password",
            {"password": "", "new_password": "awesome !"},
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "should fail with empty new password",
            {"new_password": "", "password": "awesome !"},
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "should fail with wrong old password",
            {"new_password": fake.password(), "password": "wrong old password"},
            status.HTTP_401_UNAUTHORIZED,
        ),
        (
            "should change password",
            {"new_password": fake.password(), "password": "awesome !"},
            status.HTTP_200_OK,
        ),
    ],
)
def test_change_password(test, user, expected, mock_user, auth_client):
    password = "awesome !"
    new_password = user["new_password"]
    u = mock_user(password=password)
    url = f"/api/v1/auth/change-password/"
    client = auth_client(username=u.username, password=password)
    res = client.post(url, user)
    assert res.status_code == expected
    if expected == status.HTTP_200_OK:
        client = auth_client(username=u.username, password=new_password)
    elif expected == status.HTTP_401_UNAUTHORIZED:
        with pytest.raises(AuthenticationFailed):
            assert auth_client(username=u.username, password=new_password)
