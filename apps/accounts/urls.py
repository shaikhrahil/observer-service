from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import UserViewSet, change_password, signup, logout
from django.urls import base, path

from rest_framework import routers

r = routers.SimpleRouter()
r.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path("auth/change-password/", change_password, name="change_password"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/logout/", logout, name="logout"),
] + r.urls
