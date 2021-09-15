from django.contrib import admin

from observers.models import Observer


@admin.register(Observer)
class ObserverAdmin(admin.ModelAdmin):
    pass
