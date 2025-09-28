from django.urls import path
from .views import (
    PatientListView,
    PatientDetailView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
    PatientLoginView,
    PatientReportsView,
)

urlpatterns = [
    path("", PatientListView.as_view(), name="patient-list"),
    path("create/", PatientCreateView.as_view(), name="patient-create"),
    path("update/<int:pk>/", PatientUpdateView.as_view(), name="patient-update"),
    path("delete/<int:pk>/", PatientDeleteView.as_view(), name="patient-delete"),
    path("login/", PatientLoginView.as_view(), name="patient-login"),

    # ✅ Place reports before the generic <int:pk>/ route
   path("reports/", PatientReportsView.as_view(), name="patient-reports"),


    # keep this at the bottom so it doesn’t override others
    path("<int:pk>/", PatientDetailView.as_view(), name="patient-detail"),
]

