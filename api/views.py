from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Address, Vehicle, Service, Schedule, Profile
from .serializers import (UserRegisterSerializer,
  ProfileSerializer, ProfileDetailSerializer,
  AddressSerializer, AddressDetailSerializer,
  VehicleSerializer, VehicleDetailSerializer,
  ServiceSerializer, ScheduleSerializer,
  ScheduleDetailSerializer
  )

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

################### PROFILE VIEW ###################
class ProfileModelViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ProfileSerializer
        else:
            return ProfileDetailSerializer

    def get_queryset(self, pk=None, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.all().filter(user=user)
################### ADDRESS VIEW ###################
class AddressModelViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return AddressSerializer
        else:
            return AddressDetailSerializer

    def get_queryset(self, pk=None, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.all().filter(user=user)

################### VEHICLE VIEW ###################
class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return VehicleSerializer
        else:
            return VehicleDetailSerializer

    def get_queryset(self, pk=None, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.all().filter(user=user)
          
################### SERVICE VIEW ###################
class ServiceReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny, )

################### SCHEDULE VIEW ###################    
class ScheduleModelViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ScheduleSerializer
        else:
            return ScheduleDetailSerializer
             
    def get_queryset(self, pk=None, *args, **kwargs):
        user = self.request.user
        if user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=user)