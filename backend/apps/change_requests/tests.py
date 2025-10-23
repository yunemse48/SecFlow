"""
Tests for change requests app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import ChangeRequest

User = get_user_model()


class ChangeRequestModelTest(TestCase):
    """
    Test cases for ChangeRequest model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.change_request = ChangeRequest.objects.create(
            external_id='CR-12345',
            source=ChangeRequest.Source.JIRA,
            title='Test Change Request',
            description='Test description',
            status=ChangeRequest.Status.PENDING,
            priority=ChangeRequest.Priority.MEDIUM,
            requester='John Doe',
            requested_date=timezone.now()
        )
    
    def test_change_request_creation(self):
        """Test change request is created successfully."""
        self.assertEqual(self.change_request.external_id, 'CR-12345')
        self.assertEqual(self.change_request.source, ChangeRequest.Source.JIRA)
        self.assertEqual(self.change_request.status, ChangeRequest.Status.PENDING)
    
    def test_change_request_str(self):
        """Test change request string representation."""
        expected = f"{self.change_request.external_id} - {self.change_request.title}"
        self.assertEqual(str(self.change_request), expected)
    
    def test_change_request_assignment(self):
        """Test assigning a change request to a user."""
        self.change_request.assigned_to = self.user
        self.change_request.save()
        self.assertEqual(self.change_request.assigned_to, self.user)
