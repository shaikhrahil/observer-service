from django.shortcuts import render
from rest_framework import permissions, viewsets

from apps.accounts.permissions import OwnProfilePermission

from .models import Observer
from .serializers import ObserverSerializer


class ObserverViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnProfilePermission]
    serializer_class = ObserverSerializer
    queryset = Observer.objects.all()
