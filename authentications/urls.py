from django.urls import path
from .views import NurseLoginView, PatientLoginView

urlpatterns = [
    path("login/nurse/", NurseLoginView.as_view(), name="nurse-login"),
    path("login/patient/", PatientLoginView.as_view(), name="patient-login"),
]

