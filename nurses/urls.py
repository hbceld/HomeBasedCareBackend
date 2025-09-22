from django.urls import path
from .views import (
    NurseListView,
    NurseDetailView,
    NurseCreateView,
    NurseUpdateView,
    NurseDeleteView,
)

urlpatterns = [
    path("", NurseListView.as_view(), name="nurse-list"),
    path("<int:pk>/", NurseDetailView.as_view(), name="nurse-detail"),
    path("create/", NurseCreateView.as_view(), name="nurse-create"),
    path("update/<int:pk>/", NurseUpdateView.as_view(), name="nurse-update"),
    path("delete/<int:pk>/", NurseDeleteView.as_view(), name="nurse-delete"),
]
