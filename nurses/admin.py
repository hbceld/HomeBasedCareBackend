from django.contrib import admin
from .models import NurseProfile


@admin.register(NurseProfile)
class NurseProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "license_number",
        "speciality",  # <-- FIXED (was specialization)
        "telephone",
        "email",
        "is_active",
        "date_joined",
    )
    search_fields = ("user__full_name", "license_number", "email", "telephone")
    list_filter = ("gender", "speciality", "is_active")

