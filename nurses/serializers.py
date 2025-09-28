from rest_framework import serializers
from .models import NurseProfile
from users.models import User


class NurseProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    user_id = serializers.CharField(source="user.user_id", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = NurseProfile
        fields = [
            "id",
            "user_id",
            "full_name",
            "role",
            "age",
            "qualification",
            "license_number",
            "gender",
            "telephone",
            "email",
            "speciality",
            "years_of_experience",
            "date_joined",
            "is_active",
        ]


class NurseCreateSerializer(serializers.ModelSerializer):
    # capture user info while creating nurse
    user_id = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = NurseProfile
        fields = [
            "user_id",
            "full_name",
            "password",
            "age",
            "qualification",
            "license_number",
            "gender",
            "telephone",
            "email",
            "speciality",
            "years_of_experience",
        ]

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        full_name = validated_data.pop("full_name")
        password = validated_data.pop("password")

        # ✅ Create the linked User
        user = User.objects.create_user(
            user_id=user_id,        # make sure User model has this field as USERNAME_FIELD
            full_name=full_name,
            role="nurse",
            password=password
        )

        # ✅ Create NurseProfile linked to the User
        nurse = NurseProfile.objects.create(user=user, **validated_data)
        return nurse