from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Billing
from .serializers import BillingSerializer

class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all().order_by("-created_at")
    serializer_class = BillingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "billing_id"  # ✅ Use billing_id (UUID) instead of numeric id

    def perform_create(self, serializer):
        # Automatically capture the user creating the billing
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], url_path="mark_paid")  # 👈 matches frontend
    def mark_paid(self, request, billing_id=None):
        """
        Custom endpoint: POST /api/billings/{billing_id}/mark_paid/
        Sets the payment_status to 'paid' and updates amount fields.
        """
        billing = self.get_object()

        # Update payment status and amounts
        billing.payment_status = "paid"
        billing.amount_paid = billing.amount_due  # auto-clear balance
        billing.balance = 0
        billing.save()

        serializer = self.get_serializer(billing)
        return Response(serializer.data, status=status.HTTP_200_OK)
