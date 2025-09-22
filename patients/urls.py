from django.urls import path
from .views import (
    PatientListView,
    PatientDetailView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
)

urlpatterns = [
    path("", PatientListView.as_view(), name="patient-list"),
    path("<int:pk>/", PatientDetailView.as_view(), name="patient-detail"),
    path("create/", PatientCreateView.as_view(), name="patient-create"),
    path("update/<int:pk>/", PatientUpdateView.as_view(), name="patient-update"),
    path("delete/<int:pk>/", PatientDeleteView.as_view(), name="patient-delete"),
]
