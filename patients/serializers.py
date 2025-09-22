from rest_framework import serializers
from .models import PatientProfile
from users.models import User


class PatientProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    user_id = serializers.CharField(source="user.user_id", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    assigned_nurse_name = serializers.CharField(source="assigned_nurse.user.full_name", read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            "id",
            "patient_id",
            "user_id",
            "full_name",
            "role",
            "age",
            "gender",
            "contact",
            "caregiver_contact",
            "illness_type",
            "duration",
            "severity_level",
            "care_needed",
            "speciality_required",
            "location",
            "time_of_care",
            "rotations",
            "assigned_nurse",
            "assigned_nurse_name",
            "date_registered",
            "is_active",
        ]


class PatientCreateSerializer(serializers.ModelSerializer):
    # collect user info during patient creation
    user_id = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            "user_id",
            "full_name",
            "password",
            "age",
            "gender",
            "contact",
            "caregiver_contact",
            "illness_type",
            "duration",
            "severity_level",
            "care_needed",
            "speciality_required",
            "location",
            "time_of_care",
            "rotations",
            "assigned_nurse",
        ]

    def create(self, validated_data):
        from users.models import User

        user_id = validated_data.pop("user_id")
        full_name = validated_data.pop("full_name")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            user_id=user_id,
            full_name=full_name,
            role="patient",
            password=password
        )

        patient = PatientProfile.objects.create(user=user, **validated_data)
        return patient
