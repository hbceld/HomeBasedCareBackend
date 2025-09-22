
from rest_framework import serializers
from nurses.models import NurseProfile
from patients.models import PatientProfile
from django.contrib.auth.hashers import check_password


class NurseLoginSerializer(serializers.Serializer):
    license_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        license_number = data.get("license_number")
        password = data.get("password")

        try:
            nurse = NurseProfile.objects.get(license_number=license_number)
        except NurseProfile.DoesNotExist:
            raise serializers.ValidationError("Nurse not found.")

        # validate against related user password
        if not hasattr(nurse, "user") or not check_password(password, nurse.user.password):
            raise serializers.ValidationError("Invalid credentials.")

        data["nurse"] = nurse
        return data


class PatientLoginSerializer(serializers.Serializer):
    patient_id = serializers.CharField()   # use the field you defined in PatientProfile
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        patient_id = data.get("patient_id")
        password = data.get("password")

        try:
            patient = PatientProfile.objects.get(patient_id=patient_id)
        except PatientProfile.DoesNotExist:
            raise serializers.ValidationError("Patient not found.")

        if not hasattr(patient, "user") or not check_password(password, patient.user.password):
            raise serializers.ValidationError("Invalid credentials.")

        data["patient"] = patient
        return data
