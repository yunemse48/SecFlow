"""
Tests for integrations app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Integration

User = get_user_model()


class IntegrationModelTest(TestCase):
    """
    Test cases for Integration model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.integration = Integration.objects.create(
            name='Test Jira',
            type=Integration.Type.JIRA,
            base_url='https://test.atlassian.net',
            is_active=True,
            created_by=self.user
        )
    
    def test_integration_creation(self):
        """Test integration is created successfully."""
        self.assertEqual(self.integration.name, 'Test Jira')
        self.assertEqual(self.integration.type, Integration.Type.JIRA)
        self.assertTrue(self.integration.is_active)
    
    def test_integration_str(self):
        """Test integration string representation."""
        expected = f"{self.integration.name} ({self.integration.get_type_display()})"
        self.assertEqual(str(self.integration), expected)
