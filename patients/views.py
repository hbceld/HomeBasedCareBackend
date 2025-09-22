from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import PatientProfile
from .serializers import PatientProfileSerializer, PatientCreateSerializer


class PatientListView(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]


class PatientDetailView(generics.RetrieveAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]


class PatientCreateView(generics.CreateAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientCreateSerializer
    permission_classes = [IsAdminUser]  # only admin can add patients


class PatientUpdateView(generics.UpdateAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAdminUser]


class PatientDeleteView(generics.DestroyAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAdminUser]
