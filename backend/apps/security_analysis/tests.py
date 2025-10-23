"""
Tests for security analysis app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.change_requests.models import ChangeRequest
from .models import SecurityAnalysis, ScanType, Scan

User = get_user_model()


class SecurityAnalysisModelTest(TestCase):
    """
    Test cases for SecurityAnalysis model.
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
            requester='John Doe',
            requested_date=timezone.now()
        )
        
        self.analysis = SecurityAnalysis.objects.create(
            change_request=self.change_request,
            analyst=self.user,
            status=SecurityAnalysis.Status.NOT_STARTED
        )
    
    def test_security_analysis_creation(self):
        """Test security analysis is created successfully."""
        self.assertEqual(self.analysis.change_request, self.change_request)
        self.assertEqual(self.analysis.analyst, self.user)
        self.assertEqual(self.analysis.status, SecurityAnalysis.Status.NOT_STARTED)
    
    def test_security_analysis_str(self):
        """Test security analysis string representation."""
        expected = f"Analysis for {self.change_request.external_id} by {self.user.username}"
        self.assertEqual(str(self.analysis), expected)
