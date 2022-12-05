from rest_framework import serializers
from .models import Address, Vehicle, Service, HourAvailable, Schedule, Profile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

################### REGISTER USER SERIALIZERS ###################
class UserSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField()

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['is_superuser', 'is_staff', 'is_active', 'last_login','date_joined', 'groups', 'user_permissions', 'password']
        # extra_kwargs = {'username': {'required': True}}
        
class UserDetailSerializer(serializers.ModelSerializer):
    username = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        # fields = ['id']
        exclude = ['is_superuser', 'is_staff', 'is_active', 'last_login','date_joined', 'groups', 'user_permissions', 'password']
        # extra_kwargs = {'username': {'required': True}}

################### PROFILE  USER SERIALIZERS #####################
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ['created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {'user': {'required': True}}

class ProfileDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        # fields = '__all__'
        # fields = ['user_id']
        # fields = ['id', 'birthday', 'phone_number', 'image']
        exclude = ['created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {'user': {'required': True}}
################### CHANGE PASSWORD SERIALIZERS ###################
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
################### REGISTER USER SERIALIZERS ###################
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

################### LOGOUT USER SERIALIZERS ###################
 
################### ADDRESS SERIALIZERS ###################
class AddressSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Address
        # fields = '__all__'
        exclude = ['created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {'user': {'required': True}}

class AddressDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = ['id', 'user', 'cep', 'logradouro','complemento', 'bairro','localidade', 'uf' ]
        extra_kwargs = {'user': {'required': True}}
            
################### VEHICLE SERIALIZERS ###################      
class VehicleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Vehicle
        # fields = '__all__'
        exclude = ['created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {'user': {'required': True}}

class VehicleDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vehicle
        fields = ['id', 'user', 'brand', 'model', 'fuell', 'year', 'odomitter', 'plate']
        extra_kwargs = {'user': {'required': True}}

################### SERVICES SERIALIZERS ################### 
class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        # fields = '__all__'
        exclude = ['created_at', 'updated_at', 'deleted_at']

################### HOUR AVAILABLE SERIALIZERS ################### 
class HourAvailableSerializer(serializers.ModelSerializer):

    class Meta:
        model = HourAvailable
        # fields = '__all__'
        exclude = ['created_at', 'updated_at', 'deleted_at']
            
################### SCHEDULE SERIALIZERS ###################
class ScheduleSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Schedule
        # fields = '__all__'
        # depth = 1
        # exclude = ['created_at', 'updated_at', 'deleted_at']
        # extra_kwargs = {'user': {'required': True}}
        
    def to_representation(self, instance):
      return {
        'id': instance.id,
        'user': instance.user.username,
        'address': instance.address.cep,
        'service': instance.service.name,
        'vehicle': instance.vehicle.brand,
        'hour': instance.hour.hourAvailable,
        'day': instance.day,
      }

class ScheduleDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Schedule
        # # fields = '__all__'
        exclude = ['created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {'user': {'required': True}}
        
    def to_representation(self, instance):
      return {
        'id': instance.id,
        'user': instance.user.username,
        'address': instance.address.cep,
        'service': instance.service.name,
        'vehicle': instance.vehicle.brand,
        'hour': instance.hour.hourAvailable,
        'day': instance.day,
      }
