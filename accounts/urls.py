from rest_framework.authtoken.views import obtain_auth_token
from accounts.views import signup
from django.urls import path

urlpatterns = [path("signup/", signup), path("login/", obtain_auth_token)]
