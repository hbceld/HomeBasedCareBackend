from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import NurseLoginSerializer, PatientLoginSerializer
from users.models import User


class NurseLoginView(APIView):
    def post(self, request):
        serializer = NurseLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        password = serializer.validated_data['password']
        user = authenticate(request, username=user_id, password=password)

        if user is not None and user.role == "nurse":
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.user_id,
                'full_name': user.full_name,
                'role': user.role,
            })
        return Response({'detail': 'Invalid nurse credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class PatientLoginView(APIView):
    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        password = serializer.validated_data['password']
        user = authenticate(request, username=user_id, password=password)

        if user is not None and user.role == "patient":
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.user_id,
                'full_name': user.full_name,
                'role': user.role,
            })
        return Response({'detail': 'Invalid patient credentials'}, status=status.HTTP_401_UNAUTHORIZED)
