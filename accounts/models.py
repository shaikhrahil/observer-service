from django.contrib.auth.base_user import BaseUserManager
from django.utils.tree import Node
from accounts.utils import ThemeVariantChoices
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Theme(models.Model):
    variants = models.CharField(
        choices=ThemeVariantChoices.choices, max_length=5, default=ThemeVariantChoices.DARK)
    name = models.CharField(max_length=12)

    class Meta:
        unique_together = ('variants', 'name')


class Preference(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)


class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, password):
        if not user_name:
            raise ValueError('user_name is missing')
        if not password:
            raise ValueError('password is missing')

        user = self.model(user_name)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, user_name, password):
        if not user_name:
            raise ValueError('user_name is missing')
        if not password:
            raise ValueError('password is missing')

        user = self.model(user_name)
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, user_name, password):
        print(user_name, password)
        if not user_name:
            raise ValueError('user_name is missing')
        if not password:
            raise ValueError('password is missing')

        user = self.model(user_name)
        user.set_password(password)
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):

    user_name = models.CharField(unique=True, max_length=12)
    first_name = None
    last_name = None
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_name

    object = CustomUserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []
