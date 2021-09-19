from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["username", "password", "password2"]

    def save(self):
        account = User(
            username=self.validated_data["username"],
        )
        if self.validated_data["password"] != self.validated_data["password2"]:
            raise serializers.ValidationError("Passwords not matching")

        account.set_password(self.validated_data["password"])
        account.save()
        return account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "is_staff", "is_superuser", "date_joined", "preference"]
