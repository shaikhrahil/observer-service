from django.db import models
from observers.models import Observer


class Device(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    observers = models.ManyToManyField(Observer)

    def __str__(self) -> str:
        return f"{self.name}"
