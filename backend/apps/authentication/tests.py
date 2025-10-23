"""
Tests for authentication app.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """
    Test cases for User model.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=User.Role.APPSEC_ENGINEER
        )
    
    def test_user_creation(self):
        """Test user is created successfully."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def test_is_appsec_engineer(self):
        """Test is_appsec_engineer property."""
        self.assertTrue(self.user.is_appsec_engineer)
    
    def test_user_str(self):
        """Test user string representation."""
        expected = f"{self.user.username} ({self.user.get_role_display()})"
        self.assertEqual(str(self.user), expected)
