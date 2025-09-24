from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import NurseLoginSerializer, PatientLoginSerializer, AdminLoginSerializer


def get_tokens_for_user(user):
    """
    Generate JWT tokens for a user
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# ✅ Nurse login
class NurseLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = NurseLoginSerializer(data=request.data)
        if serializer.is_valid():
            nurse = serializer.validated_data["nurse"]
            tokens = get_tokens_for_user(nurse.user)

            return Response(
                {"message": "Login successful", "nurse_id": nurse.id, "tokens": tokens},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Patient login
class PatientLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.validated_data["patient"]
            tokens = get_tokens_for_user(patient.user)

            return Response(
                {"message": "Login successful", "patient_id": patient.id, "tokens": tokens},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Admin login
class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_tokens_for_user(user)

            return Response(
                {"message": "Admin login successful", "user_id": user.id, "tokens": tokens},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
