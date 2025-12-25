"""
account/serializers.py - Yangilangan versiya
Token'ga role ma'lumotini qo'shish uchun
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from account.models import User


class CreateAndUpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'status', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'status', 'role']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT token yaratishda role ma'lumotini ham qo'shish
    """

    @classmethod
    def get_token(cls, user):
        """Token'ga custom ma'lumotlar qo'shish"""
        token = super().get_token(user)

        # Token payload'ga role qo'shish
        token['role'] = user.role

        return token

    def validate(self, attrs):
        """Login qilganda role ma'lumotini ham qaytarish"""
        data = super().validate(attrs)

        # User role'ini response'ga qo'shish
        data['role'] = self.user.role

        return {
            'access_token': data['access'],
            'refresh_token': data['refresh'],
            'role': data['role']
        }


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Token yangilashda ham role ma'lumotini qaytarish
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        # Refresh token'dan user ma'lumotlarini olish
        refresh = self.token_class(attrs['refresh'])

        return {
            'access_token': data['access'],
            'refresh_token': attrs['refresh'],
            'role': refresh.get('role', 'moderator')  # Token'dan role olish
        }