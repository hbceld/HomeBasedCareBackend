from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.user.full_name", read_only=True, default=""
    )
    nurse_name = serializers.SerializerMethodField(read_only=True)
    created_by_name = serializers.CharField(
        source="created_by.full_name", read_only=True, default=""
    )

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("appointment_id", "created_at", "updated_at")

    def get_nurse_name(self, obj):
        if obj.assigned_nurse and getattr(obj.assigned_nurse, "user", None):
            return getattr(obj.assigned_nurse.user, "full_name", "")
        return ""
