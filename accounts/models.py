from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from accounts.utils import ThemeVariantChoices


class Theme(models.Model):
    variant = models.CharField(
        choices=ThemeVariantChoices.choices,
        max_length=5,
        default=ThemeVariantChoices.DARK,
    )
    name = models.CharField(max_length=12, default="default")

    def __str__(self):
        return f"{self.variant}-{self.name}"

    class Meta:
        unique_together = ("variant", "name")


class Preference(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.theme}"


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("username is missing")
        if not password:
            raise ValueError("password is missing")

        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, username, password):
        if not username:
            raise ValueError("username is missing")
        if not password:
            raise ValueError("password is missing")

        user = self.model(username=username)
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, username, password):
        print(username, password)
        if not username:
            raise ValueError("username is missing")
        if not password:
            raise ValueError("password is missing")

        user = self.model(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(unique=True, max_length=12)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    email = None
    first_name = None
    last_name = None

    preference = models.OneToOneField(Preference, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username

    object = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
