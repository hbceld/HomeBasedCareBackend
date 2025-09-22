from django.contrib import admin
from .models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "patient_id",
        "gender",
        "age",
        "illness_type",
        "severity_level",
        "care_needed",
        "assigned_nurse",
        "is_active",
    )
    search_fields = ("user__full_name", "patient_id", "illness_type")
    list_filter = ("severity_level", "care_needed", "is_active", "gender")


