from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import NurseLoginSerializer, PatientLoginSerializer


class NurseLoginView(APIView):
    def post(self, request):
        serializer = NurseLoginSerializer(data=request.data)
        if serializer.is_valid():
            nurse = serializer.validated_data["nurse"]
            return Response(
                {"message": "Login successful", "nurse_id": nurse.id},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientLoginView(APIView):
    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.validated_data["patient"]
            return Response(
                {"message": "Login successful", "patient_id": patient.id},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
