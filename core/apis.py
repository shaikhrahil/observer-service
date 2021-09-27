from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("devices/", include("apps.devices.urls")),
    # path("observers", include("observers.urls")),
]
