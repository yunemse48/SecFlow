"""
Plugin registry for managing plugins.
"""

from typing import Dict, Type, Optional, List
import logging

from .base import BasePlugin, IntegrationPlugin, ScannerPlugin, NotificationPlugin

logger = logging.getLogger(__name__)


class PluginRegistry:
    """
    Registry for managing plugins.
    """
    
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugin_classes: Dict[str, Type[BasePlugin]] = {}
    
    def register(self, plugin_class: Type[BasePlugin]) -> None:
        """
        Register a plugin class.
        
        Args:
            plugin_class: Plugin class to register
        """
        plugin_instance = plugin_class()
        plugin_name = plugin_instance.name
        
        if plugin_name in self._plugin_classes:
            logger.warning(f"Plugin {plugin_name} is already registered. Overwriting.")
        
        self._plugin_classes[plugin_name] = plugin_class
        logger.info(f"Registered plugin: {plugin_name}")
    
    def load_plugin(self, plugin_name: str, config: Dict) -> bool:
        """
        Load and initialize a plugin.
        
        Args:
            plugin_name: Name of the plugin to load
            config: Plugin configuration
            
        Returns:
            True if plugin loaded successfully, False otherwise
        """
        if plugin_name not in self._plugin_classes:
            logger.error(f"Plugin {plugin_name} not found in registry")
            return False
        
        if plugin_name in self._plugins:
            logger.warning(f"Plugin {plugin_name} is already loaded")
            return True
        
        try:
            plugin_class = self._plugin_classes[plugin_name]
            plugin_instance = plugin_class()
            plugin_instance.initialize(config)
            self._plugins[plugin_name] = plugin_instance
            logger.info(f"Loaded plugin: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {str(e)}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            True if plugin unloaded successfully, False otherwise
        """
        if plugin_name not in self._plugins:
            logger.warning(f"Plugin {plugin_name} is not loaded")
            return False
        
        try:
            plugin = self._plugins[plugin_name]
            plugin.cleanup()
            del self._plugins[plugin_name]
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {str(e)}")
            return False
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """
        Get a loaded plugin instance.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin instance or None if not found
        """
        return self._plugins.get(plugin_name)
    
    def get_integration_plugins(self) -> List[IntegrationPlugin]:
        """
        Get all loaded integration plugins.
        
        Returns:
            List of integration plugin instances
        """
        return [
            plugin for plugin in self._plugins.values()
            if isinstance(plugin, IntegrationPlugin)
        ]
    
    def get_scanner_plugins(self) -> List[ScannerPlugin]:
        """
        Get all loaded scanner plugins.
        
        Returns:
            List of scanner plugin instances
        """
        return [
            plugin for plugin in self._plugins.values()
            if isinstance(plugin, ScannerPlugin)
        ]
    
    def get_notification_plugins(self) -> List[NotificationPlugin]:
        """
        Get all loaded notification plugins.
        
        Returns:
            List of notification plugin instances
        """
        return [
            plugin for plugin in self._plugins.values()
            if isinstance(plugin, NotificationPlugin)
        ]
    
    def list_registered_plugins(self) -> List[Dict[str, str]]:
        """
        List all registered plugin classes.
        
        Returns:
            List of plugin information dictionaries
        """
        plugins_info = []
        for plugin_class in self._plugin_classes.values():
            plugin_instance = plugin_class()
            plugins_info.append(plugin_instance.get_info())
        return plugins_info
    
    def list_loaded_plugins(self) -> List[str]:
        """
        List all loaded plugin names.
        
        Returns:
            List of loaded plugin names
        """
        return list(self._plugins.keys())


# Global plugin registry instance
plugin_registry = PluginRegistry()
