# views.py
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from django.db.models import Q
from .serializers import *


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer


class UserLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class UsersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        query = self.request.query_params.get('search', None)
        role = self.request.query_params.get('role', None)

        # Filter users based on the role and search query
        if role:
            queryset = CustomUser.objects.filter(role=role)
        else:
            queryset = CustomUser.objects.all()

        if query:
            # If a search query is provided, filter by email or phone_number
            queryset = queryset.filter(Q(email__icontains=query) | Q(phone_number__icontains=query))

        return queryset

class BlockUnblockUserView(UpdateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()


            message = " Unblocked" if instance.is_active else "Blocked"
            return Response({'message': f'You are {message}'}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)