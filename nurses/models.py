from django.db import models
from users.models import User


class NurseProfile(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="nurse_profile"
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    qualification = models.CharField(max_length=255, null=True, blank=True)
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    telephone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    speciality = models.CharField(max_length=255, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)  # can deactivate without deleting

    def __str__(self):
        return f"Nurse: {self.user.full_name} ({self.license_number or 'No License'})"



