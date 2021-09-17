from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    # path("devices", include("devices.urls")),
    # path("observers", include("observers.urls")),
]
