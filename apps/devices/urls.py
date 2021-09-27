from django.urls import path
from .views import DeviceViewSet

from rest_framework import routers

r = routers.SimpleRouter()
r.register("", DeviceViewSet, "device_viewset")


urlpatterns = r.urls
