# serializers.py
from rest_framework import serializers
from .models import CustomUser, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('city', 'state', 'country', 'pincode')

class UserRegistrationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'role', 'address')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        user = CustomUser.objects.create_user(**validated_data)

        if address_data:
            Address.objects.create(user=user, **address_data)

        return user
