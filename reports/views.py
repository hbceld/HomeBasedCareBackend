from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Report
from .serializers import ReportSerializer


class ReportListView(generics.ListAPIView):
    queryset = Report.objects.all().order_by("-date_time")
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


class ReportDetailView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


class ReportCreateView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]


class ReportUpdateView(generics.UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUser]  # only admins can edit/finalize


class ReportDeleteView(generics.DestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUser]

