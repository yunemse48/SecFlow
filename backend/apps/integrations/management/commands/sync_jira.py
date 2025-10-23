"""
Management command to sync Jira integration.
"""

from django.core.management.base import BaseCommand, CommandError
from apps.integrations.models import Integration
from apps.integrations.tasks import sync_integration


class Command(BaseCommand):
    help = 'Sync data from Jira integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--integration-id',
            type=int,
            help='ID of the integration to sync',
        )
        parser.add_argument(
            '--integration-name',
            type=str,
            help='Name of the integration to sync',
        )
        parser.add_argument(
            '--async',
            action='store_true',
            help='Run sync asynchronously using Celery',
        )

    def handle(self, *args, **options):
        integration_id = options.get('integration_id')
        integration_name = options.get('integration_name')
        run_async = options.get('async', False)

        # Find the integration
        try:
            if integration_id:
                integration = Integration.objects.get(id=integration_id)
            elif integration_name:
                integration = Integration.objects.get(name=integration_name)
            else:
                # Get first Jira integration
                integration = Integration.objects.filter(
                    type=Integration.Type.JIRA,
                    is_active=True
                ).first()
                
                if not integration:
                    raise CommandError('No active Jira integration found')
        except Integration.DoesNotExist:
            raise CommandError('Integration not found')

        self.stdout.write(f'Syncing integration: {integration.name}')

        if run_async:
            # Run asynchronously with Celery
            task = sync_integration.delay(integration.id)
            self.stdout.write(
                self.style.SUCCESS(f'Sync task started with ID: {task.id}')
            )
        else:
            # Run synchronously
            result = sync_integration(integration.id)
            
            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Sync completed successfully!\n"
                        f"Records synced: {result['records_synced']}\n"
                        f"Records failed: {result['records_failed']}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Sync failed: {result.get('error', 'Unknown error')}"
                    )
                )
