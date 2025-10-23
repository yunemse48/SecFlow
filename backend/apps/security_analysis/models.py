"""
Models for security analysis workflow.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.change_requests.models import ChangeRequest

User = get_user_model()


class SecurityAnalysis(models.Model):
    """
    Model representing a security analysis session for a change request.
    """
    
    class Status(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', _('Not Started')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
    
    change_request = models.ForeignKey(
        ChangeRequest,
        on_delete=models.CASCADE,
        related_name='security_analyses'
    )
    
    analyst = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='security_analyses'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_STARTED,
        db_index=True
    )
    
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('When the analysis was started')
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('When the analysis was completed')
    )
    
    notes = models.TextField(
        blank=True,
        help_text=_('Analysis notes and findings')
    )
    
    risk_score = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Risk score (0-100)')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'security_analyses'
        verbose_name = _('Security Analysis')
        verbose_name_plural = _('Security Analyses')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Analysis for {self.change_request.external_id} by {self.analyst.username}"


class ScanType(models.Model):
    """
    Model representing different types of security scans.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('Scan type name (e.g., SAST, DAST, SCA)')
    )
    
    description = models.TextField(
        help_text=_('Description of the scan type')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether this scan type is active')
    )
    
    configuration = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Scan configuration parameters')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'scan_types'
        verbose_name = _('Scan Type')
        verbose_name_plural = _('Scan Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Scan(models.Model):
    """
    Model representing an individual security scan execution.
    """
    
    class Status(models.TextChoices):
        QUEUED = 'QUEUED', _('Queued')
        RUNNING = 'RUNNING', _('Running')
        COMPLETED = 'COMPLETED', _('Completed')
        FAILED = 'FAILED', _('Failed')
        CANCELLED = 'CANCELLED', _('Cancelled')
    
    security_analysis = models.ForeignKey(
        SecurityAnalysis,
        on_delete=models.CASCADE,
        related_name='scans'
    )
    
    scan_type = models.ForeignKey(
        ScanType,
        on_delete=models.PROTECT,
        related_name='scans'
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.QUEUED,
        db_index=True
    )
    
    started_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    duration_seconds = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Scan duration in seconds')
    )
    
    findings_count = models.IntegerField(
        default=0,
        help_text=_('Number of findings discovered')
    )
    
    critical_count = models.IntegerField(
        default=0,
        help_text=_('Number of critical findings')
    )
    
    high_count = models.IntegerField(
        default=0,
        help_text=_('Number of high severity findings')
    )
    
    medium_count = models.IntegerField(
        default=0,
        help_text=_('Number of medium severity findings')
    )
    
    low_count = models.IntegerField(
        default=0,
        help_text=_('Number of low severity findings')
    )
    
    report_url = models.URLField(
        blank=True,
        null=True,
        help_text=_('URL to the scan report')
    )
    
    raw_results = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Raw scan results')
    )
    
    error_message = models.TextField(
        blank=True,
        help_text=_('Error message if scan failed')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'scans'
        verbose_name = _('Scan')
        verbose_name_plural = _('Scans')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.scan_type.name} scan for {self.security_analysis.change_request.external_id}"


class Finding(models.Model):
    """
    Model representing a security finding from a scan.
    """
    
    class Severity(models.TextChoices):
        CRITICAL = 'CRITICAL', _('Critical')
        HIGH = 'HIGH', _('High')
        MEDIUM = 'MEDIUM', _('Medium')
        LOW = 'LOW', _('Low')
        INFO = 'INFO', _('Informational')
    
    class Status(models.TextChoices):
        OPEN = 'OPEN', _('Open')
        IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
        RESOLVED = 'RESOLVED', _('Resolved')
        FALSE_POSITIVE = 'FALSE_POSITIVE', _('False Positive')
        ACCEPTED_RISK = 'ACCEPTED_RISK', _('Accepted Risk')
    
    scan = models.ForeignKey(
        Scan,
        on_delete=models.CASCADE,
        related_name='findings'
    )
    
    title = models.CharField(
        max_length=255,
        help_text=_('Finding title')
    )
    
    description = models.TextField(
        help_text=_('Detailed description')
    )
    
    severity = models.CharField(
        max_length=20,
        choices=Severity.choices,
        db_index=True
    )
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True
    )
    
    cwe_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text=_('CWE identifier')
    )
    
    file_path = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text=_('File path where the finding was discovered')
    )
    
    line_number = models.IntegerField(
        null=True,
        blank=True,
        help_text=_('Line number in the file')
    )
    
    remediation = models.TextField(
        blank=True,
        help_text=_('Remediation guidance')
    )
    
    external_ticket_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('External ticketing system ID (e.g., Jira)')
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text=_('Additional metadata')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'findings'
        verbose_name = _('Finding')
        verbose_name_plural = _('Findings')
        ordering = ['-severity', '-created_at']
        indexes = [
            models.Index(fields=['severity', 'status']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.severity} - {self.title}"
