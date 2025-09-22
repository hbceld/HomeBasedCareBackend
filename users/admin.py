from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ("user_id", "full_name", "role", "is_active", "is_staff")
    search_fields = ("user_id", "full_name", "role")
    list_filter = ("role", "is_active", "is_staff")
    ordering = ("user_id",)

    fieldsets = (
        (None, {"fields": ("user_id", "password")}),
        ("Personal info", {"fields": ("full_name", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("user_id", "full_name", "role", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, UserAdmin)
