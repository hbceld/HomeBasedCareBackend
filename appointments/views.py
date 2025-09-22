from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint to manage Appointments
    """
    queryset = Appointment.objects.all().order_by("-created_at")
    serializer_class = AppointmentSerializer

