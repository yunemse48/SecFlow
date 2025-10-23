"""
Admin configuration for change requests app.
"""

from django.contrib import admin
from .models import ChangeRequest, ChangeRequestComment, ChangeRequestAttachment


class ChangeRequestCommentInline(admin.TabularInline):
    model = ChangeRequestComment
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


class ChangeRequestAttachmentInline(admin.TabularInline):
    model = ChangeRequestAttachment
    extra = 0
    readonly_fields = ['created_at']


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    """
    Admin interface for ChangeRequest model.
    """
    list_display = [
        'external_id', 'title', 'status', 'priority',
        'source', 'assigned_to', 'created_at'
    ]
    list_filter = ['status', 'priority', 'source', 'created_at']
    search_fields = ['external_id', 'title', 'description', 'requester']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ChangeRequestCommentInline, ChangeRequestAttachmentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('external_id', 'source', 'title', 'description')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Assignment', {
            'fields': ('requester', 'assigned_to')
        }),
        ('Technical Details', {
            'fields': (
                'repository_url', 'branch_name',
                'pull_request_url', 'jenkins_build_url'
            )
        }),
        ('Dates', {
            'fields': ('requested_date', 'due_date', 'completed_date')
        }),
        ('Metadata', {
            'fields': ('external_data', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChangeRequestComment)
class ChangeRequestCommentAdmin(admin.ModelAdmin):
    """
    Admin interface for ChangeRequestComment model.
    """
    list_display = ['change_request', 'user', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['content', 'user__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ChangeRequestAttachment)
class ChangeRequestAttachmentAdmin(admin.ModelAdmin):
    """
    Admin interface for ChangeRequestAttachment model.
    """
    list_display = ['filename', 'change_request', 'uploaded_by', 'file_size', 'created_at']
    list_filter = ['created_at']
    search_fields = ['filename', 'change_request__external_id']
    readonly_fields = ['created_at']
