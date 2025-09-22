from django.db import models
from patients.models import PatientProfile
from nurses.models import NurseProfile
from users.models import User
import uuid


class Appointment(models.Model):
    # Identifiers
    appointment_id = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=""
    )

    # Links / Relationships
    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    assigned_nurse = models.ForeignKey(
        NurseProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_appointments"
    )

    # Scheduling Info
    date_of_appointment = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)

    VISIT_PERIOD_CHOICES = [
        ("morning", "Morning"),
        ("afternoon", "Afternoon"),
        ("evening", "Evening"),
        ("night", "Night"),
    ]
    visit_period = models.CharField(
        max_length=20,
        choices=VISIT_PERIOD_CHOICES,
        null=True,
        blank=True
    )

    RECURRENCE_CHOICES = [
        ("none", "None"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]
    recurrence = models.CharField(
        max_length=20,
        choices=RECURRENCE_CHOICES,
        default="none"
    )

    # Details of Care
    PURPOSE_CHOICES = [
        ("checkup", "Check-up"),
        ("wound_care", "Wound Care"),
        ("medication", "Medication"),
        ("therapy", "Therapy"),
        ("emergency", "Emergency"),
        ("other", "Other"),
    ]
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    location = models.CharField(max_length=255)
    special_requirements = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    # Status Tracking
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("missed", "Missed"),
        ("rescheduled", "Rescheduled"),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled"
    )
    cancellation_reason = models.TextField(null=True, blank=True)
    rescheduled_datetime = models.DateTimeField(null=True, blank=True)

    # Care Integration
    linked_report = models.ForeignKey(
        "reports.Report",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments"
    )
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    # Optional Extras
    PRIORITY_CHOICES = [
        ("normal", "Normal"),
        ("high", "High"),
        ("emergency", "Emergency"),
    ]
    priority_level = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal"
    )
    transportation_required = models.BooleanField(default=False)
    family_notified = models.BooleanField(default=False)
    attachments = models.FileField(
        upload_to="appointment_attachments/",
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            self.appointment_id = f"APT{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.patient.user.full_name} ({self.status})"


