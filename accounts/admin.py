from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from django.db.models import fields

from accounts.models import Preference, Theme, User

# from django.forms.models import ModelForm


@admin.register(Preference)
class PreferenceAdminForm(admin.ModelAdmin):
    # class Meta:
    #     model = Preference
    #     fields = ["theme"]

    # fields = ["username", "password", "preferences"]
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
    list_display = ["username", "preference"]
    search_fields = ["username"]
    ordering = ["username"]
    # exclude = ["email", "first_name", "last_name"]
    # inlines = (PreferenceAdminForm,)


@admin.register(Theme)
class ThemeAdminForm(admin.ModelAdmin):
    list_filter = ["name", "variant"]
    # fields = ["username", "password", "preferences"]
    list_display = ["name", "variant"]
    search_fields = ["name", "variant"]
    ordering = ["name", "variant"]


admin.site.site_header = "observerX"
admin.site.site_title = "observerX"
