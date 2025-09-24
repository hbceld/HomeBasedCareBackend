from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsAdminOrAssignedNurse

# Import profiles to resolve user->profile mapping
from nurses.models import NurseProfile
from patients.models import PatientProfile


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for Appointments.
    Admins see all appointments.
    Nurses see only their assigned appointments.
    Patients see only their own appointments.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrAssignedNurse]

    def get_queryset(self):
        user = self.request.user

        # Admins: return everything
        if user.is_staff or user.is_superuser:
            return Appointment.objects.all().order_by("-created_at")

        # Nurses: find NurseProfile for this user and return those assigned
        try:
            nurse_profile = NurseProfile.objects.get(user=user)
        except NurseProfile.DoesNotExist:
            nurse_profile = None

        if nurse_profile:
            return Appointment.objects.filter(assigned_nurse=nurse_profile).order_by("-created_at")

        # Patients: find PatientProfile for this user and return their appointments
        try:
            patient_profile = PatientProfile.objects.get(user=user)
        except PatientProfile.DoesNotExist:
            patient_profile = None

        if patient_profile:
            return Appointment.objects.filter(patient=patient_profile).order_by("-created_at")

        # Default: empty queryset (user not admin/nurse/patient)
        return Appointment.objects.none()

    # Optionally, enforce object-level permission on retrieve/update/delete
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        return super().destroy(request, *args, **kwargs)
