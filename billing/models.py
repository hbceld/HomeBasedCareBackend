from django.db import models
from patients.models import PatientProfile
from nurses.models import NurseProfile
from users.models import User
import uuid


class Billing(models.Model):
    BILLING_PERIOD_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("mpesa", "M-Pesa"),
        ("airtel_money", "Airtel Money"),
        ("bank_transfer", "Bank Transfer"),
        ("other", "Other"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("partial", "Partially Paid"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
    ]

    # Identifiers
    billing_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)

    # Links/Relationships
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="billings")
    nurse = models.ForeignKey(NurseProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="billings")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_billings")

    # Billing Details
    billing_period = models.CharField(max_length=20, choices=BILLING_PERIOD_CHOICES)
    date_issued = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    agreement = models.TextField(blank=True, null=True)

    # Payment Info
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)

    # Status Tracking
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending")
    notes = models.TextField(blank=True, null=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Auto-calculate balance
        self.balance = self.amount_due - self.amount_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Billing {self.invoice_number or self.billing_id} - {self.patient.user.full_name}"

