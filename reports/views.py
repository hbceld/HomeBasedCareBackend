from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        """
        Override create to ensure all fields are properly saved and the full object
        is returned in the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save()
        # Refresh from DB to get all default/auto-generated fields (like report_id, date_time)
        report.refresh_from_db()
        return Response(ReportSerializer(report).data, status=status.HTTP_201_CREATED)


class ReportUpdateView(generics.UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUser]  # only admins can edit/finalize


class ReportDeleteView(generics.DestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUser]
