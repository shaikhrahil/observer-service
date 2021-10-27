from django.urls import reverse
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
        reverse("signup"),
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
    res = client.post(reverse("signup"), req)
    res = client.post(reverse("signup"), req)

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
        reverse("signup"),
        {"username": "rahil", "password": "awesome", "password2": "awesome"},
    )
    res = client.post(
        reverse("login"),
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
    url = reverse("change_password")
    client, _res = auth_client(username=u.username, password=password)
    res = client.post(url, user)
    assert res.status_code == expected
    if expected == status.HTTP_200_OK:
        client = auth_client(username=u.username, password=new_password)
    elif expected == status.HTTP_401_UNAUTHORIZED:
        with pytest.raises(AuthenticationFailed):
            assert auth_client(username=u.username, password=new_password)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test,user_id,expected",
    [
        (
            "should fail with no user with userid=0",
            0,
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "should succeed",
            1,
            status.HTTP_200_OK,
        ),
    ],
)
def test_get_my_profile(test, user_id, expected, mock_user, auth_client):
    password = "awesome !"
    u = mock_user(password=password)
    client, _res = auth_client(username=u.username, password=password)
    url = reverse("users-detail", kwargs={"pk": user_id})
    res = client.get(url)
    assert res.status_code == expected


@pytest.mark.django_db
def test_logout(mock_user, auth_client, client):
    password = fake.password()
    user = mock_user(password=password)
    authenticated_client, res = auth_client(username=user.username, password=password)
    logout_path = reverse("logout")
    assert client.post(logout_path).status_code == status.HTTP_401_UNAUTHORIZED
    assert (
        authenticated_client.post(
            logout_path, {"refresh_token": res["refresh"]}
        ).status_code
        == status.HTTP_202_ACCEPTED
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test,new_user,response",
    [
        ("should update username", {"username": "awesomeRahil"}, status.HTTP_200_OK),
        (
            "should fail to update username",
            {"username": "lk"},
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "should create prefences",
            {
                "username": "new username",
                "preference": {"theme": {"variant": "light", "name": "default"}},
            },
            status.HTTP_200_OK,
        ),
        ("should reset prefences", {"preference": None}, status.HTTP_200_OK),
        (
            "should update theme name to 'awesome theme !'",
            {
                "username": "new username",
                "preference": {"theme": {"name": "awesome the", "variant": "light"}},
            },
            status.HTTP_200_OK,
        ),
        (
            "should update theme variant to 'light'",
            {
                "username": "new username",
                "preference": {"theme": {"variant": "light", "name": "default"}},
            },
            status.HTTP_200_OK,
        ),
        (
            "should fail to update theme variant to 'invalid variant'",
            {
                "username": "new username",
                "preference": {
                    "theme": {"variant": "invalid variant", "name": "default"}
                },
            },
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_update_my_profile(test, new_user, response, mock_user, auth_client):
    password = fake.password()
    u = mock_user(password=password)
    client, _res = auth_client(username=u.username, password=password)
    assert (
        client.patch(
            reverse("users-detail", kwargs={"pk": u.id}),
            new_user,
            format="json",
        ).status_code
        == response
    )


@pytest.mark.django_db
def test_deactivate_my_account(mock_user, auth_client):
    password = fake.password()
    u = mock_user(password=password)
    client, _res = auth_client(username=u.username, password=password)
    assert client.delete(reverse("users-detail", kwargs={"pk": u.id}))
    with pytest.raises(AuthenticationFailed):
        auth_client(username=u.username, password=u.password)
