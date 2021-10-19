from rest_framework import permissions, viewsets

from apps.accounts.permissions import IsOwnerStrict

from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerStrict]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
