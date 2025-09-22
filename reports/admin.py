from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "report_id",
        "patient",
        "nurse",
        "report_type",
        "date_time",
        "shift",
        "is_finalized",
    )
    search_fields = ("report_id", "patient__user__full_name", "nurse__user__full_name")
    list_filter = ("report_type", "shift", "is_finalized", "date_time")

