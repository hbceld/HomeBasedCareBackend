from django.urls import path
from .views import (
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
)

urlpatterns = [
    path("", ReportListView.as_view(), name="report-list"),
    path("<int:pk>/", ReportDetailView.as_view(), name="report-detail"),
    path("create/", ReportCreateView.as_view(), name="report-create"),
    path("update/<int:pk>/", ReportUpdateView.as_view(), name="report-update"),
    path("delete/<int:pk>/", ReportDeleteView.as_view(), name="report-delete"),
]
