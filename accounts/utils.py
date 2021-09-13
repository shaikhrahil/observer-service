from django.db import models


class ThemeVariantChoices(models.TextChoices):
    DARK = "dark"
    LIGHT = "light"
