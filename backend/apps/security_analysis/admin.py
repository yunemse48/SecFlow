"""
Admin configuration for security analysis app.
"""

from django.contrib import admin
from .models import SecurityAnalysis, ScanType, Scan, Finding


@admin.register(SecurityAnalysis)
class SecurityAnalysisAdmin(admin.ModelAdmin):
    """
    Admin interface for SecurityAnalysis model.
    """
    list_display = ['change_request', 'analyst', 'status', 'risk_score', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['change_request__external_id', 'analyst__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ScanType)
class ScanTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for ScanType model.
    """
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    """
    Admin interface for Scan model.
    """
    list_display = [
        'scan_type', 'security_analysis', 'status',
        'findings_count', 'critical_count', 'high_count', 'created_at'
    ]
    list_filter = ['status', 'scan_type', 'created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    """
    Admin interface for Finding model.
    """
    list_display = ['title', 'severity', 'status', 'scan', 'created_at']
    list_filter = ['severity', 'status', 'created_at']
    search_fields = ['title', 'description', 'cwe_id']
    readonly_fields = ['created_at', 'updated_at']
