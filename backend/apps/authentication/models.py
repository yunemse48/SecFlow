"""
Authentication models for user management and permissions.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrator')
        APPSEC_ENGINEER = 'APPSEC_ENGINEER', _('AppSec Engineer')
        DEVELOPER = 'DEVELOPER', _('Developer')
        VIEWER = 'VIEWER', _('Viewer')
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
        help_text=_('User role for permission management')
    )
    
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text=_('Contact phone number')
    )
    
    department = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_('User department')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_appsec_engineer(self):
        return self.role in [self.Role.ADMIN, self.Role.APPSEC_ENGINEER]
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN


class APIKey(models.Model):
    """
    API Key model for programmatic access.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='api_keys'
    )
    
    name = models.CharField(
        max_length=100,
        help_text=_('Descriptive name for the API key')
    )
    
    key = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text=_('API key value')
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text=_('Whether the API key is active')
    )
    
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Expiration date for the API key')
    )
    
    last_used_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_('Last time the API key was used')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'api_keys'
        verbose_name = _('API Key')
        verbose_name_plural = _('API Keys')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
