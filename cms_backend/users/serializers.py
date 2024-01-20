from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import CustomUser, Address, Role
import re


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('city', 'state', 'country', 'pincode')


class UserRegistrationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    role = serializers.ChoiceField(
        choices=[role.value for role in Role], required=False, default=Role.USER.value)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name',
                  'last_name', 'phone_number', 'address', "role")
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email address is already in use.")

        return value

    def validate_password(self, value):
        if len(value) < 8 or not any(char.isupper() for char in value) or not any(char.islower() for char in value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters with 1 uppercase and 1 lowercase.")

        return value

    def validate_phone_number(self, value):
        # Validate phone number format (allowing optional country code and hyphen)
        if not value.startswith('+'):
            value = '+91-' + value
        phone_number_pattern = r'^\+?\d{1,3}-?\d{10}$'
        if not re.match(phone_number_pattern, value):
            raise serializers.ValidationError(
                "Enter a valid phone number with country code.")

        return value

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        user = CustomUser.objects.create_user(**validated_data)

        if address_data:
            Address.objects.create(user=user, **address_data)
        else:
            # If no address data provided, create an empty Address instance for the user
            Address.objects.create(user=user)

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['email'] = user.email
        return token



class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False) 
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone_number','first_name', 'last_name', 'role','address']
