"""
Serializers for authentication app.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import APIKey

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone_number', 'department', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users.
    """
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone_number', 'department'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class APIKeySerializer(serializers.ModelSerializer):
    """
    Serializer for API Key model.
    """
    
    class Meta:
        model = APIKey
        fields = [
            'id', 'name', 'key', 'is_active', 'expires_at',
            'last_used_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'key', 'last_used_at', 'created_at', 'updated_at']
