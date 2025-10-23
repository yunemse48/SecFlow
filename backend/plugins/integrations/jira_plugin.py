"""
Jira Integration Plugin for fetching and syncing change requests.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

from jira import JIRA
from jira.exceptions import JIRAError

from plugins.base import IntegrationPlugin

logger = logging.getLogger(__name__)


class JiraIntegrationPlugin(IntegrationPlugin):
    """
    Plugin for integrating with Atlassian Jira.
    """
    
    name = "jira"
    version = "1.0.0"
    description = "Integration with Atlassian Jira for change request management"
    integration_type = "JIRA"
    
    def __init__(self):
        super().__init__()
        self.client = None
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize Jira client with configuration.
        
        Args:
            config: Dictionary containing:
                - url: Jira instance URL
                - username: Jira username/email
                - api_token: Jira API token
        """
        try:
            self.client = JIRA(
                server=config['url'],
                basic_auth=(config['username'], config['api_token'])
            )
            logger.info(f"Jira plugin initialized for {config['url']}")
        except Exception as e:
            logger.error(f"Failed to initialize Jira plugin: {str(e)}")
            raise
    
    def cleanup(self) -> None:
        """
        Cleanup Jira client resources.
        """
        if self.client:
            self.client.close()
            self.client = None
            logger.info("Jira plugin cleaned up")
    
    def test_connection(self, config: Dict[str, Any]) -> bool:
        """
        Test connection to Jira instance.
        
        Args:
            config: Connection configuration
            
        Returns:
            True if connection successful, False otherwise
        """
        try:
            temp_client = JIRA(
                server=config['url'],
                basic_auth=(config['username'], config['api_token'])
            )
            # Try to get server info to verify connection
            temp_client.server_info()
            temp_client.close()
            logger.info(f"Jira connection test successful for {config['url']}")
            return True
        except JIRAError as e:
            logger.error(f"Jira connection test failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Jira connection test error: {str(e)}")
            return False
    
    def sync_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sync change requests from Jira.
        
        Args:
            config: Sync configuration containing:
                - project_key: Jira project key (e.g., 'PROJ')
                - jql: Optional JQL query for filtering
                - max_results: Maximum number of results to fetch
                
        Returns:
            Dictionary with sync results:
                - success: bool
                - records_synced: int
                - records_failed: int
                - issues: List of issue data
                - errors: List of error messages
        """
        if not self.client:
            return {
                'success': False,
                'records_synced': 0,
                'records_failed': 0,
                'issues': [],
                'errors': ['Jira client not initialized']
            }
        
        try:
            # Build JQL query
            project_key = config.get('project_key', '')
            custom_jql = config.get('jql', '')
            max_results = config.get('max_results', 50)
            
            if custom_jql:
                jql = custom_jql
            elif project_key:
                jql = f'project = {project_key} ORDER BY updated DESC'
            else:
                jql = 'ORDER BY updated DESC'
            
            # Fetch issues from Jira
            issues = self.client.search_issues(
                jql,
                maxResults=max_results,
                fields='summary,description,status,priority,assignee,reporter,created,updated,comment'
            )
            
            # Parse issues into standardized format
            parsed_issues = []
            for issue in issues:
                parsed_issue = self._parse_jira_issue(issue)
                parsed_issues.append(parsed_issue)
            
            logger.info(f"Successfully synced {len(parsed_issues)} issues from Jira")
            
            return {
                'success': True,
                'records_synced': len(parsed_issues),
                'records_failed': 0,
                'issues': parsed_issues,
                'errors': []
            }
            
        except JIRAError as e:
            error_msg = f"Jira API error: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'records_synced': 0,
                'records_failed': 1,
                'issues': [],
                'errors': [error_msg]
            }
        except Exception as e:
            error_msg = f"Unexpected error during sync: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'records_synced': 0,
                'records_failed': 1,
                'issues': [],
                'errors': [error_msg]
            }
    
    def push_data(self, data: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """
        Push updates back to Jira.
        
        Args:
            data: Data to push containing:
                - issue_key: Jira issue key (e.g., 'PROJ-123')
                - fields: Dictionary of fields to update
                - comment: Optional comment to add
                
            config: Push configuration
            
        Returns:
            True if push successful, False otherwise
        """
        if not self.client:
            logger.error("Jira client not initialized")
            return False
        
        try:
            issue_key = data.get('issue_key')
            if not issue_key:
                logger.error("No issue_key provided for push")
                return False
            
            issue = self.client.issue(issue_key)
            
            # Update fields if provided
            fields = data.get('fields', {})
            if fields:
                issue.update(fields=fields)
                logger.info(f"Updated Jira issue {issue_key} with fields: {fields.keys()}")
            
            # Add comment if provided
            comment_text = data.get('comment')
            if comment_text:
                self.client.add_comment(issue, comment_text)
                logger.info(f"Added comment to Jira issue {issue_key}")
            
            return True
            
        except JIRAError as e:
            logger.error(f"Failed to push data to Jira: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during push: {str(e)}")
            return False
    
    def _parse_jira_issue(self, issue) -> Dict[str, Any]:
        """
        Parse a Jira issue into standardized format.
        
        Args:
            issue: Jira issue object
            
        Returns:
            Dictionary with standardized issue data
        """
        return {
            'external_id': issue.key,
            'title': issue.fields.summary,
            'description': issue.fields.description or '',
            'status': issue.fields.status.name,
            'priority': issue.fields.priority.name if issue.fields.priority else 'Medium',
            'requester': issue.fields.reporter.displayName if issue.fields.reporter else 'Unknown',
            'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
            'requested_date': self._parse_jira_datetime(issue.fields.created),
            'updated_date': self._parse_jira_datetime(issue.fields.updated),
            'external_data': {
                'issue_type': issue.fields.issuetype.name,
                'project_key': issue.fields.project.key,
                'project_name': issue.fields.project.name,
                'url': f"{self.client.server_url}/browse/{issue.key}",
                'labels': getattr(issue.fields, 'labels', []),
                'components': [c.name for c in getattr(issue.fields, 'components', [])],
            }
        }
    
    def _parse_jira_datetime(self, jira_datetime: str) -> datetime:
        """
        Parse Jira datetime string to Python datetime.
        
        Args:
            jira_datetime: Jira datetime string
            
        Returns:
            Python datetime object
        """
        try:
            # Jira uses ISO 8601 format
            return datetime.fromisoformat(jira_datetime.replace('Z', '+00:00'))
        except Exception as e:
            logger.warning(f"Failed to parse Jira datetime: {str(e)}")
            return datetime.now()
    
    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Get a single issue from Jira.
        
        Args:
            issue_key: Jira issue key (e.g., 'PROJ-123')
            
        Returns:
            Parsed issue data or None if not found
        """
        if not self.client:
            logger.error("Jira client not initialized")
            return None
        
        try:
            issue = self.client.issue(issue_key)
            return self._parse_jira_issue(issue)
        except JIRAError as e:
            logger.error(f"Failed to get Jira issue {issue_key}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting issue: {str(e)}")
            return None
    
    def create_issue(self, data: Dict[str, Any]) -> str:
        """
        Create a new issue in Jira.
        
        Args:
            data: Issue data containing:
                - project_key: Jira project key
                - summary: Issue summary/title
                - description: Issue description
                - issue_type: Issue type (e.g., 'Task', 'Bug')
                - priority: Priority name (optional)
                
        Returns:
            Created issue key or None if failed
        """
        if not self.client:
            logger.error("Jira client not initialized")
            return None
        
        try:
            issue_dict = {
                'project': {'key': data['project_key']},
                'summary': data['summary'],
                'description': data.get('description', ''),
                'issuetype': {'name': data.get('issue_type', 'Task')},
            }
            
            if 'priority' in data:
                issue_dict['priority'] = {'name': data['priority']}
            
            new_issue = self.client.create_issue(fields=issue_dict)
            logger.info(f"Created Jira issue: {new_issue.key}")
            return new_issue.key
            
        except JIRAError as e:
            logger.error(f"Failed to create Jira issue: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating issue: {str(e)}")
            return None
