import pytest
from rest_framework import status


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
def test_get_user(test, user_id, expected, mock_user, auth_client):
    password = "awesome !"
    u = mock_user(password=password)
    client = auth_client(username=u.username, password=password)
    url = f"/api/v1/users/{user_id}/"
    res = client.get(url)
    assert res.status_code == expected
