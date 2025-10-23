"""
Django configuration package.
"""

# This will make sure the Celery app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)

# Register plugins on startup
def register_plugins():
    """Register all available plugins."""
    from plugins.registry import plugin_registry
    from plugins.integrations import JiraIntegrationPlugin
    
    # Register integration plugins
    plugin_registry.register(JiraIntegrationPlugin)

# Register plugins when Django starts
register_plugins()
