from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "appointment_id",
        "patient",
        "assigned_nurse",
        "date_of_appointment",
        "start_time",
        "status",
        "priority_level",
    )
    list_filter = ("status", "priority_level", "visit_period", "recurrence")
    search_fields = (
        "appointment_id",
        "patient__user__full_name",
        "assigned_nurse__user__full_name",
    )
    ordering = ("-created_at",)
