"""
Models for change request management.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ChangeRequest(models.Model):
    """
    Model representing a change request from ITSM systems.
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        SECURITY_REVIEW = 'SECURITY_REVIEW', _('Security Review')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')
    
    class Priority(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')
        CRITICAL = 'CRITICAL', _('Critical')
    
    class Source(models.TextChoices):
        JIRA = 'JIRA', _('Jira')
        SERVICENOW = 'SERVICENOW', _('ServiceNow')
        MANUAL = 'MANUAL', _('Manual')
    
    # External system reference
    external_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text=_('External system ticket ID')
    )
    
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        help_text=_('Source system of the change request')
    )
    
    # Basic information
    title = models.CharField(
        max_length=255,
        help_text=_('Change request title')
    )
    
    description = models.TextField(
        help_text=_('Detailed description of the change')
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        help_text=_('Current status of the change request')
    )
    
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text=_('Priority level')
    )
    
    # Assignment
    requester = models.CharField(
        max_length=255,
        help_text=_('Person who requested the change')
    )
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_change_requests',
        help_text=_('AppSec engineer assigned to review')
    )
    
    # Technical details
    repository_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('Repository URL')
    )
    
    branch_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Branch name')
    )
    
    pull_request_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('Pull request URL')
    )
    
    jenkins_build_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('Jenkins build URL')
    )
    
    # Metadata
    external_data = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Additional data from external system')
    )
    
    # Timestamps
    requested_date = models.DateTimeField(
        help_text=_('Date when the change was requested')
    )
    
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Due date for the change')
    )
    
    completed_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Date when the change was completed')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'change_requests'
        verbose_name = _('Change Request')
        verbose_name_plural = _('Change Requests')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['external_id', 'source']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.external_id} - {self.title}"


class ChangeRequestComment(models.Model):
    """
    Comments on change requests.
    """
    
    change_request = models.ForeignKey(
        ChangeRequest,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='change_request_comments'
    )
    
    content = models.TextField(
        help_text=_('Comment content')
    )
    
    is_internal = models.BooleanField(
        default=False,
        help_text=_('Whether this is an internal comment')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'change_request_comments'
        verbose_name = _('Change Request Comment')
        verbose_name_plural = _('Change Request Comments')
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.change_request.external_id}"


class ChangeRequestAttachment(models.Model):
    """
    Attachments for change requests.
    """
    
    change_request = models.ForeignKey(
        ChangeRequest,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    
    file = models.FileField(
        upload_to='change_requests/%Y/%m/%d/',
        help_text=_('Attached file')
    )
    
    filename = models.CharField(
        max_length=255,
        help_text=_('Original filename')
    )
    
    file_size = models.IntegerField(
        help_text=_('File size in bytes')
    )
    
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_attachments'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'change_request_attachments'
        verbose_name = _('Change Request Attachment')
        verbose_name_plural = _('Change Request Attachments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.filename} - {self.change_request.external_id}"
