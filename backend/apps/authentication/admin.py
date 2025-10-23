"""
Admin configuration for authentication app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, APIKey


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for User model.
    """
    list_display = ['username', 'email', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'department')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'department')}),
    )


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    """
    Admin interface for APIKey model.
    """
    list_display = ['name', 'user', 'is_active', 'expires_at', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'user__username', 'key']
    readonly_fields = ['key', 'last_used_at', 'created_at', 'updated_at']
