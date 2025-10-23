"""
Base plugin classes for the plugin system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BasePlugin(ABC):
    """
    Base class for all plugins.
    """
    
    name: str = ""
    version: str = "1.0.0"
    description: str = ""
    
    def __init__(self):
        if not self.name:
            raise ValueError("Plugin must have a name")
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration.
        
        Args:
            config: Plugin configuration dictionary
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """
        Cleanup resources when plugin is unloaded.
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """
        Get plugin information.
        
        Returns:
            Dictionary with plugin metadata
        """
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
        }


class IntegrationPlugin(BasePlugin):
    """
    Base class for integration plugins.
    """
    
    integration_type: str = ""
    
    @abstractmethod
    def test_connection(self, config: Dict[str, Any]) -> bool:
        """
        Test connection to the external system.
        
        Args:
            config: Connection configuration
            
        Returns:
            True if connection successful, False otherwise
        """
        pass
    
    @abstractmethod
    def sync_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sync data from the external system.
        
        Args:
            config: Sync configuration
            
        Returns:
            Dictionary with sync results
        """
        pass
    
    @abstractmethod
    def push_data(self, data: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """
        Push data to the external system.
        
        Args:
            data: Data to push
            config: Push configuration
            
        Returns:
            True if push successful, False otherwise
        """
        pass


class ScannerPlugin(BasePlugin):
    """
    Base class for security scanner plugins.
    """
    
    scanner_type: str = ""
    supported_languages: List[str] = []
    
    @abstractmethod
    def configure_scan(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure a security scan.
        
        Args:
            config: Scan configuration
            
        Returns:
            Validated scan configuration
        """
        pass
    
    @abstractmethod
    def execute_scan(self, target: str, config: Dict[str, Any]) -> str:
        """
        Execute a security scan.
        
        Args:
            target: Scan target (repository URL, file path, etc.)
            config: Scan configuration
            
        Returns:
            Scan job ID or identifier
        """
        pass
    
    @abstractmethod
    def get_scan_status(self, scan_id: str) -> Dict[str, Any]:
        """
        Get the status of a running scan.
        
        Args:
            scan_id: Scan identifier
            
        Returns:
            Dictionary with scan status information
        """
        pass
    
    @abstractmethod
    def get_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """
        Get the results of a completed scan.
        
        Args:
            scan_id: Scan identifier
            
        Returns:
            Dictionary with scan results
        """
        pass
    
    @abstractmethod
    def parse_findings(self, raw_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse raw scan results into standardized findings.
        
        Args:
            raw_results: Raw scan results
            
        Returns:
            List of standardized finding dictionaries
        """
        pass


class NotificationPlugin(BasePlugin):
    """
    Base class for notification plugins.
    """
    
    notification_type: str = ""
    
    @abstractmethod
    def send_notification(
        self,
        recipients: List[str],
        subject: str,
        message: str,
        config: Dict[str, Any]
    ) -> bool:
        """
        Send a notification.
        
        Args:
            recipients: List of recipient identifiers
            subject: Notification subject
            message: Notification message
            config: Notification configuration
            
        Returns:
            True if notification sent successfully, False otherwise
        """
        pass
