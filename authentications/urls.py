from django.urls import path
from .views import NurseLoginView, PatientLoginView, AdminLoginView

urlpatterns = [
    path("login/nurse/", NurseLoginView.as_view(), name="nurse_login"),
    path("login/patient/", PatientLoginView.as_view(), name="patient_login"),
    path("login/admin/", AdminLoginView.as_view(), name="admin_login"),
]

