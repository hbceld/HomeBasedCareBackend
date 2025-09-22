from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import NurseProfile
from .serializers import NurseProfileSerializer, NurseCreateSerializer


class NurseListView(generics.ListAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]


class NurseDetailView(generics.RetrieveAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAuthenticated]


class NurseCreateView(generics.CreateAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseCreateSerializer
    permission_classes = [IsAdminUser]  # only admin can add nurse


class NurseUpdateView(generics.UpdateAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAdminUser]


class NurseDeleteView(generics.DestroyAPIView):
    queryset = NurseProfile.objects.all()
    serializer_class = NurseProfileSerializer
    permission_classes = [IsAdminUser]

