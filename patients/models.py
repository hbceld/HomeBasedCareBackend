from django.db import models
from users.models import User
from nurses.models import NurseProfile
import uuid


class PatientProfile(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    SEVERITY_CHOICES = [
        ("mild", "Mild"),
        ("moderate", "Moderate"),
        ("severe", "Severe"),
        ("critical", "Critical"),
    ]

    CARE_TYPE_CHOICES = [
        ("general", "General Care"),
        ("palliative", "Palliative Care"),
        ("post_surgery", "Post-Surgery"),
        ("daily_monitoring", "Daily Monitoring"),
        ("specialized", "Specialized Care"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )
    patient_id = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=""
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    caregiver_contact = models.CharField(max_length=20, null=True, blank=True)

    illness_type = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)  # e.g. "6 months"
    severity_level = models.CharField(max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True)
    care_needed = models.CharField(max_length=50, choices=CARE_TYPE_CHOICES, null=True, blank=True)
    speciality_required = models.CharField(max_length=255, null=True, blank=True)

    location = models.CharField(max_length=255, null=True, blank=True)
    time_of_care = models.CharField(max_length=100, null=True, blank=True)  # e.g. "Morning, Evening"
    rotations = models.CharField(max_length=100, null=True, blank=True)  # e.g. "Weekly rotation"

    assigned_nurse = models.ForeignKey(
        NurseProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="patients",
    )

    date_registered = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = f"PAT{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient: {self.user.full_name} ({self.patient_id})"


