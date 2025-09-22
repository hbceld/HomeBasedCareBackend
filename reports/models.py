from django.db import models
from nurses.models import NurseProfile
from patients.models import PatientProfile
import uuid


class Report(models.Model):
    REPORT_TYPES = [
        ("daily", "Daily Care Report"),
        ("incident", "Incident Report"),
        ("progress", "Progress Report"),
        ("followup", "Follow-up Report"),
        ("discharge", "Discharge/Completion Report"),
    ]

    SHIFT_CHOICES = [
        ("morning", "Morning"),
        ("afternoon", "Afternoon"),
        ("evening", "Evening"),
        ("night", "Night"),
    ]

    report_id = models.CharField(
        max_length=15,
        unique=True,
        editable=False,
        default="",
    )
    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="reports"
    )
    nurse = models.ForeignKey(
        NurseProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports"
    )
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    date_time = models.DateTimeField(auto_now_add=True)
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES, null=True, blank=True)

    observations = models.TextField(null=True, blank=True)
    care_provided = models.TextField(null=True, blank=True)
    medication_given = models.TextField(null=True, blank=True)

    # vitals can be JSON to allow flexible structure
    vitals_recorded = models.JSONField(null=True, blank=True)

    recommendations = models.TextField(null=True, blank=True)
    attachments = models.FileField(upload_to="report_attachments/", null=True, blank=True)

    created_by = models.ForeignKey(
        NurseProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_reports"
    )
    verified_by = models.CharField(max_length=255, null=True, blank=True)  # can be admin/family name

    is_finalized = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.report_id:
            self.report_id = f"REP{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Report {self.report_id} for {self.patient}"
