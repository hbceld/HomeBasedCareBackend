from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.user.full_name", read_only=True
    )
    nurse_name = serializers.CharField(
        source="assigned_nurse.user.full_name", read_only=True
    )
    created_by_name = serializers.CharField(
        source="created_by.full_name", read_only=True
    )

    class Meta:
        model = Appointment
        fields = "__all__"
