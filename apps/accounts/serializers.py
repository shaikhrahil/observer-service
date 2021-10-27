from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import Preference, Theme, User


class ChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["password", "new_password"]

    def update(self, user):
        if self.validated_data["password"] == self.validated_data["new_password"]:
            raise serializers.ValidationError("Old and new password cannot be same")

        if not check_password(self.validated_data["password"], user.password):
            raise AuthenticationFailed("Old password is incorrect")

        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


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


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = "__all__"


class PreferenceSerializer(serializers.ModelSerializer):
    theme = ThemeSerializer(allow_null=True)

    class Meta:
        model = Preference
        fields = ["theme"]


class UserSerializer(serializers.ModelSerializer):
    preference = PreferenceSerializer(allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "is_staff",
            "is_superuser",
            "date_joined",
            "preference",
        ]

    def create(self, validated_data):
        preference = validated_data.pop("preference")
        u = User.objects.create(**validated_data)
        Preference.objects.create(**preference, user=u)
        return u

    def update(self, instance, validated_data):
        preference = validated_data.pop("preference", None)
        instance.username = validated_data.get("username", instance.username)
        # u = User.objects.update(**validated_data)
        instance.save()
        # if preference:
        #     Preference.objects.update_or_create(**preference)
        # Preference.objects.filter(user=u).update(**preference)
        return instance
