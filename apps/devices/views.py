from rest_framework import permissions, viewsets

from apps.accounts.permissions import StrictProfilePermission

from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, StrictProfilePermission]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
