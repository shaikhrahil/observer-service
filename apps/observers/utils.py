from django.db import models


class Constraints(models.TextChoices):
    CAMERA = "camera"
    GPS = "gps"
    MIC = "mic"


class ObserverStatus(models.TextChoices):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ONLINE = "online"
    OFFLINE = "offline"
