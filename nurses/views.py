from rest_framework import generics
from .models import NurseProfile
from .serializers import NurseProfileSerializer, NurseCreateSerializer
from rest_framework.permissions import IsAuthenticated  # <- changed

class NurseListView(generics.ListAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]  # <- changed

class NurseCreateView(generics.CreateAPIView):
    serializer_class = NurseCreateSerializer
    permission_classes = [IsAuthenticated]  # <- changed

class NurseDetailView(generics.RetrieveAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]  # <- changed

class NurseUpdateView(generics.UpdateAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseCreateSerializer
    permission_classes = [IsAuthenticated]  # <- changed

class NurseDeleteView(generics.DestroyAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]  # <- changed


