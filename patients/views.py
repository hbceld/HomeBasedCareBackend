from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import PatientProfile
from .serializers import PatientProfileSerializer, PatientCreateSerializer
from reports.models import Report
from reports.serializers import ReportSerializer


from django.shortcuts import get_object_or_404


class PatientListView(generics.ListAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]


class PatientDetailView(RetrieveAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Lookup by logged-in user
        user = self.request.user
        return PatientProfile.objects.get(user=user)
    


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

# patients/views.py
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class PatientLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        password = request.data.get("password")

        if not user_id or not password:
            return Response({"error": "User ID and password required"}, status=400)

        user = authenticate(username=user_id, password=password)

        if user and getattr(user, "role", None) == "patient":
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "user_id": user.user_id,
                    "full_name": user.full_name,
                    "role": user.role,
                }
            }, status=200)

        return Response({"error": "Invalid credentials"}, status=401)
class PatientReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        # Get patient profile from logged-in user
        patient = get_object_or_404(PatientProfile, user=request.user)

        # Fetch reports for this patient
        reports = Report.objects.filter(patient=patient).select_related("nurse")
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
