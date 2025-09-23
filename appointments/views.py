from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.permissions import AllowAny  # temporarily allow all
from django.contrib.auth import authenticate

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]  # remove custom permissions for now

    def get_queryset(self):
        # Return all appointments, admin can see everything
        return Appointment.objects.all().order_by("-created_at")
