from rest_framework import viewsets, permissions
from .models import Billing
from .serializers import BillingSerializer

class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all().order_by("-created_at")
    serializer_class = BillingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically capture the user creating the billing
        serializer.save(created_by=self.request.user)

