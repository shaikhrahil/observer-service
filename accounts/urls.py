from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import UserController, signup, logout
from django.urls import path

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/logout/", logout, name="logout"),
    path("user/", UserController.as_view(), name="get_update_user"),
]
