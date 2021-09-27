from django.db import models

from apps.devices.utils import DeviceStatus
from apps.observers.models import Observer


class Device(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    observers = models.ManyToManyField(Observer, blank=True)
    status = models.CharField(
        DeviceStatus.choices, default=DeviceStatus.OFFLINE, max_length=8
    )

    def __str__(self) -> str:
        return f"{self.name}"
