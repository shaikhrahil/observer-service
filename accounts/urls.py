# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import GetUser, UpdateUser, getProfile, signup, logout
from django.urls import path

urlpatterns = [
    path("auth/signup/", signup, name="signup"),
    path("auth/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/logout/", logout, name="logout"),
    path("user/", getProfile, name="get_current_user"),
    path("user/<int:pk>/", GetUser.as_view(), name="get_user"),
    path("user/<int:pk>/", UpdateUser.as_view(), name="update_user"),
]
