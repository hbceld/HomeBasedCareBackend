from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .models import NurseProfile
from rest_framework.decorators import action
from patients.models import PatientProfile
from patients.serializers import PatientProfileSerializer 

from .models import NurseProfile
from .serializers import NurseProfileSerializer, NurseCreateSerializer


class NurseListView(generics.ListAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]


class NurseCreateView(generics.CreateAPIView):
    serializer_class = NurseCreateSerializer
    permission_classes = [IsAuthenticated]  # consider IsAdminUser

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nurse = serializer.save()

        read = NurseProfileSerializer(nurse, context={"request": request})
        headers = self.get_success_headers(read.data)
        return Response(read.data, status=status.HTTP_201_CREATED, headers=headers)


class NurseDetailView(generics.RetrieveAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]


class NurseUpdateView(generics.UpdateAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseCreateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance: NurseProfile = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        password = serializer.validated_data.pop("password", None)
        user_id = serializer.validated_data.pop("user_id", None)
        full_name = serializer.validated_data.pop("full_name", None)

        with transaction.atomic():
            for attr, value in serializer.validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            user = instance.user
            if full_name:
                user.full_name = full_name
            if user_id:
                user.user_id = user_id
            if password:
                user.set_password(password)
            user.save()

        read = NurseProfileSerializer(instance, context={"request": request})
        return Response(read.data, status=status.HTTP_200_OK)


class NurseDeleteView(generics.DestroyAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]


class NurseLoginView(APIView):
    permission_classes = [AllowAny]   # 👈 allow public access

    def post(self, request):
        user_id = request.data.get("user_id")
        password = request.data.get("password")

        if not user_id or not password:
            return Response(
                {"error": "User ID and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Django’s authenticate expects username=..., not user_id=...
        user = authenticate(username=user_id, password=password)

        if user and getattr(user, "role", None) == "nurse":
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user": {
                        "id": user.id,
                        "user_id": user.user_id,
                        "full_name": user.full_name,
                        "role": user.role,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import NurseProfile
from .serializers import NurseProfileSerializer
from patients.models import PatientProfile
from patients.serializers import PatientProfileSerializer

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import NurseProfile
from .serializers import NurseProfileSerializer
from patients.models import PatientProfile
from patients.serializers import PatientProfileSerializer

class NurseViewSet(viewsets.ModelViewSet):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='patients')
    def patients(self, request, pk=None):
        """
        Returns all patients assigned to a specific nurse (by user.id OR nurse.id).
        """
        try:
            # First, try NurseProfile.id
            nurse = NurseProfile.objects.filter(pk=pk).first()
            if not nurse:
                # If not found, try matching User.id
                nurse = NurseProfile.objects.filter(user_id=pk).first()

            if not nurse:
                return Response({"detail": "Nurse not found."}, status=404)

            patients = PatientProfile.objects.filter(assigned_nurse=nurse)
            serializer = PatientProfileSerializer(patients, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"detail": str(e)}, status=500)
    @action(detail=True, methods=['get'], url_path='reports', permission_classes=[IsAuthenticated])
    def reports(self, request, pk=None):
        """
        Returns all reports created for a specific nurse (by NurseProfile.id or by User.id).
        Accessible at GET /api/nurses/<pk>/reports/
        """
        # import here to avoid top-level circular imports
        from reports.models import Report
        from reports.serializers import ReportSerializer

        # Try to find nurse by NurseProfile.pk first, then try User.id
        nurse = NurseProfile.objects.filter(pk=pk).first()
        if not nurse:
            nurse = NurseProfile.objects.filter(user_id=pk).first()

        if not nurse:
            return Response({"detail": "Nurse not found."}, status=status.HTTP_404_NOT_FOUND)

        reports_qs = Report.objects.filter(nurse=nurse).order_by("-date_time")
        serializer = ReportSerializer(reports_qs, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
