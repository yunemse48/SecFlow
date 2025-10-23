"""
Serializers for integrations app.
"""

from rest_framework import serializers
from .models import Integration, SyncLog, Webhook


class IntegrationSerializer(serializers.ModelSerializer):
    """
    Serializer for Integration model.
    """
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Integration
        fields = [
            'id', 'name', 'type', 'base_url', 'is_active',
            'configuration', 'sync_enabled', 'sync_interval_minutes',
            'last_sync_at', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_sync_at', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'configuration': {'write_only': True}
        }


class SyncLogSerializer(serializers.ModelSerializer):
    """
    Serializer for SyncLog model.
    """
    integration_name = serializers.CharField(source='integration.name', read_only=True)
    
    class Meta:
        model = SyncLog
        fields = [
            'id', 'integration', 'integration_name', 'status',
            'records_synced', 'records_failed', 'duration_seconds',
            'error_message', 'details', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class WebhookSerializer(serializers.ModelSerializer):
    """
    Serializer for Webhook model.
    """
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Webhook
        fields = [
            'id', 'name', 'url', 'events', 'is_active',
            'secret', 'headers', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'secret': {'write_only': True}
        }
