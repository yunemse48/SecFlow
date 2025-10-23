"""
Celery tasks for integrations.
"""

import logging
from typing import Dict, Any
from celery import shared_task
from django.utils import timezone

from .models import Integration, SyncLog
from apps.change_requests.models import ChangeRequest
from plugins.registry import plugin_registry

logger = logging.getLogger(__name__)


@shared_task
def sync_integration(integration_id: int) -> Dict[str, Any]:
    """
    Sync data from an external integration.
    
    Args:
        integration_id: ID of the integration to sync
        
    Returns:
        Dictionary with sync results
    """
    try:
        integration = Integration.objects.get(id=integration_id)
        
        if not integration.is_active:
            logger.warning(f"Integration {integration.name} is not active")
            return {'success': False, 'error': 'Integration not active'}
        
        # Load the plugin
        plugin_loaded = plugin_registry.load_plugin(
            integration.type.lower(),
            integration.configuration
        )
        
        if not plugin_loaded:
            error_msg = f"Failed to load plugin for {integration.type}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
        
        # Get the plugin
        plugin = plugin_registry.get_plugin(integration.type.lower())
        
        # Sync data
        sync_config = {
            'project_key': integration.configuration.get('project_key', ''),
            'jql': integration.configuration.get('jql', ''),
            'max_results': integration.configuration.get('max_results', 50),
        }
        
        start_time = timezone.now()
        result = plugin.sync_data(sync_config)
        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        
        # Process synced issues
        records_synced = 0
        records_failed = 0
        
        if result['success']:
            for issue_data in result['issues']:
                try:
                    # Create or update change request
                    change_request, created = ChangeRequest.objects.update_or_create(
                        external_id=issue_data['external_id'],
                        source=integration.type,
                        defaults={
                            'title': issue_data['title'],
                            'description': issue_data['description'],
                            'status': _map_jira_status(issue_data['status']),
                            'priority': _map_jira_priority(issue_data['priority']),
                            'requester': issue_data['requester'],
                            'requested_date': issue_data['requested_date'],
                            'external_data': issue_data['external_data'],
                        }
                    )
                    records_synced += 1
                    logger.info(f"{'Created' if created else 'Updated'} change request: {change_request.external_id}")
                    
                except Exception as e:
                    records_failed += 1
                    logger.error(f"Failed to process issue {issue_data['external_id']}: {str(e)}")
        
        # Create sync log
        sync_log = SyncLog.objects.create(
            integration=integration,
            status=SyncLog.Status.SUCCESS if result['success'] else SyncLog.Status.FAILED,
            records_synced=records_synced,
            records_failed=records_failed,
            duration_seconds=int(duration),
            error_message='\n'.join(result.get('errors', [])),
            details={
                'total_fetched': len(result.get('issues', [])),
                'sync_config': sync_config,
            }
        )
        
        # Update integration last sync time
        if result['success']:
            integration.last_sync_at = timezone.now()
            integration.save()
        
        logger.info(f"Sync completed for {integration.name}: {records_synced} synced, {records_failed} failed")
        
        return {
            'success': result['success'],
            'records_synced': records_synced,
            'records_failed': records_failed,
            'sync_log_id': sync_log.id,
        }
        
    except Integration.DoesNotExist:
        error_msg = f"Integration with ID {integration_id} not found"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}
    except Exception as e:
        error_msg = f"Unexpected error during sync: {str(e)}"
        logger.error(error_msg)
        return {'success': False, 'error': error_msg}


@shared_task
def sync_all_integrations():
    """
    Sync all active integrations with sync enabled.
    """
    integrations = Integration.objects.filter(
        is_active=True,
        sync_enabled=True
    )
    
    results = []
    for integration in integrations:
        result = sync_integration.delay(integration.id)
        results.append({
            'integration_id': integration.id,
            'integration_name': integration.name,
            'task_id': result.id,
        })
    
    logger.info(f"Started sync for {len(results)} integrations")
    return results


def _map_jira_status(jira_status: str) -> str:
    """
    Map Jira status to internal status.
    
    Args:
        jira_status: Jira status name
        
    Returns:
        Internal status value
    """
    status_mapping = {
        'To Do': ChangeRequest.Status.PENDING,
        'Open': ChangeRequest.Status.PENDING,
        'In Progress': ChangeRequest.Status.IN_PROGRESS,
        'In Review': ChangeRequest.Status.SECURITY_REVIEW,
        'Security Review': ChangeRequest.Status.SECURITY_REVIEW,
        'Done': ChangeRequest.Status.COMPLETED,
        'Closed': ChangeRequest.Status.COMPLETED,
        'Cancelled': ChangeRequest.Status.CANCELLED,
        'Rejected': ChangeRequest.Status.REJECTED,
    }
    
    return status_mapping.get(jira_status, ChangeRequest.Status.PENDING)


def _map_jira_priority(jira_priority: str) -> str:
    """
    Map Jira priority to internal priority.
    
    Args:
        jira_priority: Jira priority name
        
    Returns:
        Internal priority value
    """
    priority_mapping = {
        'Highest': ChangeRequest.Priority.CRITICAL,
        'High': ChangeRequest.Priority.HIGH,
        'Medium': ChangeRequest.Priority.MEDIUM,
        'Low': ChangeRequest.Priority.LOW,
        'Lowest': ChangeRequest.Priority.LOW,
    }
    
    return priority_mapping.get(jira_priority, ChangeRequest.Priority.MEDIUM)
