
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NurseListView, NurseDetailView, NurseCreateView,
    NurseUpdateView, NurseDeleteView, NurseLoginView, NurseViewSet
)

router = DefaultRouter()
router.register(r"", NurseViewSet, basename="nurse")

urlpatterns = [
    # keep non-viewset views first
    path("login/", NurseLoginView.as_view(), name="nurse-login"),

    # include router AFTER
    path("", include(router.urls)),
]

