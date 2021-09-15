from django.db import models

class Constraints(models.TextChoices):
    CAMERA = 'camera'
    GPS = 'gps'
    MIC = 'mic'