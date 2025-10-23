#!/usr/bin/env python
"""
Quick test script to verify the setup is working.
Run this after migrations to test the basic functionality.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.change_requests.models import ChangeRequest
from apps.integrations.models import Integration
from plugins.registry import plugin_registry

User = get_user_model()

def test_setup():
    """Test basic setup."""
    print("🧪 Testing AppSec Dashboard Setup\n")
    
    # Test 1: Check database connection
    print("1️⃣ Testing database connection...")
    try:
        user_count = User.objects.count()
        print(f"   ✅ Database connected! Found {user_count} users")
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False
    
    # Test 2: Check models
    print("\n2️⃣ Testing models...")
    try:
        cr_count = ChangeRequest.objects.count()
        int_count = Integration.objects.count()
        print(f"   ✅ Models working! {cr_count} change requests, {int_count} integrations")
    except Exception as e:
        print(f"   ❌ Model error: {e}")
        return False
    
    # Test 3: Check plugin registry
    print("\n3️⃣ Testing plugin system...")
    try:
        registered = plugin_registry.list_registered_plugins()
        print(f"   ✅ Plugin registry working! {len(registered)} plugins registered:")
        for plugin in registered:
            print(f"      - {plugin['name']} v{plugin['version']}: {plugin['description']}")
    except Exception as e:
        print(f"   ❌ Plugin error: {e}")
        return False
    
    # Test 4: Check Jira plugin
    print("\n4️⃣ Testing Jira plugin...")
    try:
        from plugins.integrations import JiraIntegrationPlugin
        plugin = JiraIntegrationPlugin()
        info = plugin.get_info()
        print(f"   ✅ Jira plugin loaded!")
        print(f"      Name: {info['name']}")
        print(f"      Version: {info['version']}")
        print(f"      Description: {info['description']}")
    except Exception as e:
        print(f"   ❌ Jira plugin error: {e}")
        return False
    
    print("\n" + "="*60)
    print("✅ All tests passed! Your setup is ready to go!")
    print("="*60)
    
    print("\n📋 Next Steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Start the server: python manage.py runserver")
    print("3. Visit admin: http://localhost:8000/admin")
    print("4. Create a Jira integration in the admin panel")
    print("5. Run sync: python manage.py sync_jira")
    
    return True

if __name__ == '__main__':
    test_setup()
