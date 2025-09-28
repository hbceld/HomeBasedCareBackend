from rest_framework import serializers
from .models import PatientProfile
from users.models import User
from nurses.models import NurseProfile   # ✅ import NurseProfile


class PatientProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    user_id = serializers.CharField(source="user.user_id", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    
    # Send assigned nurse as an object with id and full_name
    assigned_nurse = serializers.SerializerMethodField(read_only=True)

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
            "date_registered",
            "is_active",
        ]

    def get_assigned_nurse(self, obj):
        if obj.assigned_nurse:
            return {
                "id": obj.assigned_nurse.id,
                "full_name": obj.assigned_nurse.user.full_name
            }
        return None


class PatientCreateSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {
            "assigned_nurse": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        full_name = validated_data.pop("full_name")
        password = validated_data.pop("password")

        # create patient user
        user = User.objects.create_user(
            user_id=user_id,
            full_name=full_name,
            role="patient",
            password=password,
        )

        # handle assigned nurse correctly
        assigned_nurse = validated_data.pop("assigned_nurse", None)
        if assigned_nurse:
            try:
                nurse = NurseProfile.objects.get(pk=assigned_nurse.id)
            except NurseProfile.DoesNotExist:
                raise serializers.ValidationError(
                    {"assigned_nurse": "Selected nurse does not exist."}
                )
            validated_data["assigned_nurse"] = nurse
        else:
            validated_data["assigned_nurse"] = None

        # create patient profile
        patient = PatientProfile.objects.create(user=user, **validated_data)
        return patient
