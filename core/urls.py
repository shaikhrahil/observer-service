from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    # path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", include("core.apis")),
]
