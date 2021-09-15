from django.contrib import admin

from devices.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass
