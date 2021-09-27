from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Preference, Theme, User


@admin.register(Preference)
class PreferenceAdminForm(admin.ModelAdmin):
    list_display = ["theme"]


@admin.register(User)
class UserAdminForm(UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "preference",
                    "date_joined",
                    "groups",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "last_login",
                    "password",
                    "user_permissions",
                    "username",
                    "devices",
                )
            },
        ),
    )
    list_display = [
        "id",
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    search_fields = ["username"]
    ordering = ["username"]


@admin.register(Theme)
class ThemeAdminForm(admin.ModelAdmin):
    list_filter = ["name", "variant"]
    list_display = ["name", "variant"]
    search_fields = ["name", "variant"]
    ordering = ["name", "variant"]


admin.site.site_header = "observerX"
admin.site.site_title = "observerX"
