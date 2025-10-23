"""
Admin configuration for integrations app.
"""

from django.contrib import admin
from .models import Integration, SyncLog, Webhook


@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    """
    Admin interface for Integration model.
    """
    list_display = ['name', 'type', 'is_active', 'sync_enabled', 'last_sync_at', 'created_at']
    list_filter = ['type', 'is_active', 'sync_enabled', 'created_at']
    search_fields = ['name', 'base_url']
    readonly_fields = ['last_sync_at', 'created_at', 'updated_at']


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    """
    Admin interface for SyncLog model.
    """
    list_display = ['integration', 'status', 'records_synced', 'records_failed', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['integration__name', 'error_message']
    readonly_fields = ['created_at']


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    """
    Admin interface for Webhook model.
    """
    list_display = ['name', 'url', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'url']
    readonly_fields = ['created_at', 'updated_at']
