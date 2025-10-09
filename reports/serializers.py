from rest_framework import serializers
from .models import Report
from nurses.models import NurseProfile

# Nested serializer for nurse
class NurseSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = NurseProfile
        fields = ["id", "full_name"]

class ReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.user.full_name", read_only=True)
    nurse = NurseSerializer(read_only=True)  # nested object for frontend
    created_at = serializers.DateTimeField(
        source="date_time",  # map to your model field
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "report_id",
            "patient",
            "patient_name",
            "nurse",           # nested nurse object
            "report_type",
            "created_at",      # frontend-friendly date field
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

