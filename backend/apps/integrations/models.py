"""
Models for external system integrations.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Integration(models.Model):
    """
    Model representing an external system integration.
    """
    
    class Type(models.TextChoices):
        JIRA = 'JIRA', _('Jira')
        SERVICENOW = 'SERVICENOW', _('ServiceNow')
        GITHUB = 'GITHUB', _('GitHub')
        GITLAB = 'GITLAB', _('GitLab')
        JENKINS = 'JENKINS', _('Jenkins')
        SONARQUBE = 'SONARQUBE', _('SonarQube')
        SNYK = 'SNYK', _('Snyk')
        CHECKMARX = 'CHECKMARX', _('Checkmarx')
        VERACODE = 'VERACODE', _('Veracode')
    
    name = models.CharField(
        max_length=100,
        help_text=_('Integration name')
    )
    
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        help_text=_('Integration type')
    )
    
    base_url = models.URLField(
        help_text=_('Base URL of the external system')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this integration is active')
    )
    
    configuration = models.JSONField(
        default=dict,
        help_text=_('Integration configuration (encrypted credentials, etc.)')
    )
    
    sync_enabled = models.BooleanField(
        default=False,
        help_text=_('Enable bidirectional sync')
    )
    
    sync_interval_minutes = models.IntegerField(
        default=15,
        help_text=_('Sync interval in minutes')
    )
    
    last_sync_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Last successful sync timestamp')
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_integrations'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'integrations'
        verbose_name = _('Integration')
        verbose_name_plural = _('Integrations')
        ordering = ['name']
        unique_together = [['name', 'type']]
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class SyncLog(models.Model):
    """
    Model for tracking integration sync operations.
    """
    
    class Status(models.TextChoices):
        SUCCESS = 'SUCCESS', _('Success')
        FAILED = 'FAILED', _('Failed')
        PARTIAL = 'PARTIAL', _('Partial Success')
    
    integration = models.ForeignKey(
        Integration,
        on_delete=models.CASCADE,
        related_name='sync_logs'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        db_index=True
    )
    
    records_synced = models.IntegerField(
        default=0,
        help_text=_('Number of records synced')
    )
    
    records_failed = models.IntegerField(
        default=0,
        help_text=_('Number of records that failed to sync')
    )
    
    duration_seconds = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Sync duration in seconds')
    )
    
    error_message = models.TextField(
        blank=True,
        help_text=_('Error message if sync failed')
    )
    
    details = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Additional sync details')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sync_logs'
        verbose_name = _('Sync Log')
        verbose_name_plural = _('Sync Logs')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.integration.name} - {self.status} - {self.created_at}"


class Webhook(models.Model):
    """
    Model for webhook configurations.
    """
    
    class Event(models.TextChoices):
        CHANGE_REQUEST_CREATED = 'CHANGE_REQUEST_CREATED', _('Change Request Created')
        CHANGE_REQUEST_UPDATED = 'CHANGE_REQUEST_UPDATED', _('Change Request Updated')
        ANALYSIS_COMPLETED = 'ANALYSIS_COMPLETED', _('Analysis Completed')
        SCAN_COMPLETED = 'SCAN_COMPLETED', _('Scan Completed')
        FINDING_CREATED = 'FINDING_CREATED', _('Finding Created')
    
    name = models.CharField(
        max_length=100,
        help_text=_('Webhook name')
    )
    
    url = models.URLField(
        help_text=_('Webhook URL')
    )
    
    events = models.JSONField(
        default=list,
        help_text=_('List of events to trigger this webhook')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this webhook is active')
    )
    
    secret = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Webhook secret for signature verification')
    )
    
    headers = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Custom headers to send with webhook')
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_webhooks'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'webhooks'
        verbose_name = _('Webhook')
        verbose_name_plural = _('Webhooks')
        ordering = ['name']
    
    def __str__(self):
        return self.name
