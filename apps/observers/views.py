from django.shortcuts import render
from rest_framework import permissions, viewsets

from apps.accounts.permissions import IsOwner

from .models import Observer
from .serializers import ObserverSerializer


class ObserverViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    serializer_class = ObserverSerializer
    queryset = Observer.objects.all()
