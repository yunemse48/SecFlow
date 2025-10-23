"""
URL configuration for integrations app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IntegrationViewSet, SyncLogViewSet, WebhookViewSet

router = DefaultRouter()
router.register(r'', IntegrationViewSet, basename='integration')
router.register(r'sync-logs', SyncLogViewSet, basename='sync-log')
router.register(r'webhooks', WebhookViewSet, basename='webhook')

urlpatterns = [
    path('', include(router.urls)),
]
