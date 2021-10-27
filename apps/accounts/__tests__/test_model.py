from apps.accounts.models import Preference, Theme, User
import pytest
from faker import Faker

fake = Faker()


@pytest.mark.django_db
def test_user_model():
    username = fake.name()
    assert username == str(
        User.objects.create(username=username, password=fake.password())
    )


@pytest.mark.django_db
def test_preference_model():
    theme = Theme.objects.create()
    assert "dark-default" == str(theme)
    assert "dark-default" == str(Preference.objects.create(theme=theme))
