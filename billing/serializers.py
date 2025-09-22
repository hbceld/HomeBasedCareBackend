from rest_framework import serializers
from .models import Billing

class BillingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.user.full_name", read_only=True)
    nurse_name = serializers.CharField(source="nurse.user.full_name", read_only=True)
    created_by_name = serializers.CharField(source="created_by.full_name", read_only=True)

    class Meta:
        model = Billing
        fields = [
            "billing_id",
            "invoice_number",
            "patient",
            "patient_name",
            "nurse",
            "nurse_name",
            "created_by",
            "created_by_name",
            "billing_period",
            "date_issued",
            "due_date",
            "agreement",
            "amount_due",
            "amount_paid",
            "balance",
            "payment_method",
            "transaction_reference",
            "payment_date",
            "payment_status",
            "notes",
            "created_at",
            "updated_at",
            "is_active",
        ]
        read_only_fields = ["billing_id", "balance", "created_at", "updated_at"]
