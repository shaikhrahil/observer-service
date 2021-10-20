import factory
from apps.accounts.models import User, Preference, Theme


class ThemeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Theme

    variant = "dark"
    name = "default"


class PreferenceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Preference

    theme = factory.SubFactory(ThemeFactory)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.faker.Faker("name")
    password = "awesome"
    preference = factory.SubFactory(PreferenceFactory)
