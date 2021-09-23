from rest_framework import viewsets, permissions

from devices.models import Device
from devices.serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
