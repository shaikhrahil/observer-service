from django.db import models

from .utils import ObserverStatus


class Observer(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    contraints = models.TextField(max_length=45)
    url = models.URLField()
    status = models.CharField(
        ObserverStatus.choices, default=ObserverStatus.OFFLINE, max_length=8
    )

    def __str__(self) -> str:
        return f"{self.name}"
