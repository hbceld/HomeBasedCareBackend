from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.user.full_name", read_only=True)
    nurse_name = serializers.CharField(source="nurse.user.full_name", read_only=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "report_id",
            "patient",
            "patient_name",
            "nurse",
            "nurse_name",
            "report_type",
            "date_time",
            "shift",
            "observations",
            "care_provided",
            "medication_given",
            "vitals_recorded",
            "recommendations",
            "attachments",
            "created_by",
            "verified_by",
            "is_finalized",
        ]
