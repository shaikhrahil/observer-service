from django.db import models

from observers.utils import Constraints


class Observer(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    contraints = models.TextField(max_length=45)
    url = models.URLField()

    def __str__(self) -> str:
        return f"{self.name}"
