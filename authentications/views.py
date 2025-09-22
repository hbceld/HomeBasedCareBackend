from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import NurseLoginSerializer, PatientLoginSerializer


class NurseLoginView(APIView):
    def post(self, request):
        serializer = NurseLoginSerializer(data=request.data)
        if serializer.is_valid():
            nurse = serializer.validated_data["nurse"]
            user = nurse.user

            # Create or retrieve token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "nurse_id": nurse.id,
                "full_name": user.full_name,
                "license_number": nurse.license_number,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientLoginView(APIView):
    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.validated_data["patient"]
            user = patient.user

            # Create or retrieve token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "patient_id": patient.patient_id,
                "full_name": user.full_name,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
