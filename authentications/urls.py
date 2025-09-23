from django.urls import path
from .views import NurseLoginView, PatientLoginView, AdminLoginView

urlpatterns = [
    path("login/nurse/", NurseLoginView.as_view(), name="nurse-login"),
    path("login/patient/", PatientLoginView.as_view(), name="patient-login"),
    path("login/admin/", AdminLoginView.as_view(), name="admin-login"),
]

