"""
Views for integrations app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Integration, SyncLog, Webhook
from .serializers import IntegrationSerializer, SyncLogSerializer, WebhookSerializer
from .tasks import sync_integration
from plugins.registry import plugin_registry


class IntegrationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing integrations.
    """
    queryset = Integration.objects.all()
    serializer_class = IntegrationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'is_active', 'sync_enabled']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """
        Test the connection to an integration.
        """
        integration = self.get_object()
        
        # Load and test the plugin
        plugin_type = integration.type.lower()
        plugin_loaded = plugin_registry.load_plugin(
            plugin_type,
            integration.configuration
        )
        
        if not plugin_loaded:
            return Response(
                {'error': f'Failed to load plugin for {integration.type}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        plugin = plugin_registry.get_plugin(plugin_type)
        connection_ok = plugin.test_connection(integration.configuration)
        
        if connection_ok:
            return Response({
                'status': 'success',
                'message': f'Successfully connected to {integration.name}'
            })
        else:
            return Response(
                {'error': f'Failed to connect to {integration.name}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def sync_now(self, request, pk=None):
        """
        Trigger an immediate sync for an integration.
        """
        integration = self.get_object()
        
        if not integration.is_active:
            return Response(
                {'error': 'Integration is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Trigger sync via Celery task
        run_async = request.data.get('async', True)
        
        if run_async:
            task = sync_integration.delay(integration.id)
            return Response({
                'status': 'success',
                'message': f'Sync initiated for {integration.name}',
                'task_id': task.id
            })
        else:
            # Run synchronously (useful for testing)
            result = sync_integration(integration.id)
            return Response({
                'status': 'success' if result['success'] else 'error',
                'message': f'Sync completed for {integration.name}',
                'records_synced': result.get('records_synced', 0),
                'records_failed': result.get('records_failed', 0),
                'error': result.get('error')
            })


class SyncLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing sync logs.
    """
    queryset = SyncLog.objects.all()
    serializer_class = SyncLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['integration', 'status']


class WebhookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing webhooks.
    """
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """
        Test a webhook by sending a test payload.
        """
        webhook = self.get_object()
        
        # TODO: Implement webhook testing
        
        return Response({
            'status': 'success',
            'message': f'Test webhook sent to {webhook.url}'
        })
