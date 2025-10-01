from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NurseListView, NurseDetailView, NurseCreateView,
    NurseUpdateView, NurseDeleteView, NurseLoginView, NurseViewSet
)

router = DefaultRouter()
router.register(r"", NurseViewSet, basename="nurse")

urlpatterns = [
    # Login view
    path("login/", NurseLoginView.as_view(), name="nurse-login"),

    # Create view (fix for your POST)
    path("create/", NurseCreateView.as_view(), name="nurse-create"),

    # Router for list/detail/update/delete
    path("", include(router.urls)),
]

