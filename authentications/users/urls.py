from django.urls import path
from .views import NurseLoginView, PatientLoginView

urlpatterns = [
    path('nurse-login/', NurseLoginView.as_view(), name='nurse-login'),
    path('patient-login/', PatientLoginView.as_view(), name='patient-login'),
]
