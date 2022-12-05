from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Address, Vehicle, Service, Schedule, Profile
from .serializers import (UserSerializer,UserDetailSerializer,
UserRegisterSerializer,ChangePasswordSerializer,
ProfileSerializer, ProfileDetailSerializer,
AddressSerializer, AddressDetailSerializer,
VehicleSerializer, VehicleDetailSerializer,
ServiceSerializer, ScheduleSerializer,
ScheduleDetailSerializer
  )

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

################### USER VIEW #############################
class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    #serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return UserSerializer
        else:
            return UserDetailSerializer

    def get_queryset(self, pk=None, *args, **kwargs):
        username = self.request.user
        print(username)
        if username.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.all().filter(username=username)

################### PROFILE VIEW #############################
class UserProfileModelViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    # serializer_class = ProfileSerializer
    
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ProfileSerializer
        else:
            return ProfileDetailSerializer
              
    def get_queryset(self, pk=None, *args, **kwargs):
        user = self.request.user
        print(user)
        if user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.all().filter(user=user)
################### CHANGE PASSWORD VIEW ###################
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
################### PROFILE VIEW ###################
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})

################### REGISTER USER VIEW ###################       
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