# Getting Started - Your First Steps

## 🎉 Welcome! You're Ready to Build

I've just created the **Jira Integration Plugin** - your first major feature! Here's what to do next.

## 📋 Step-by-Step Guide

### Step 1: Set Up Your Environment (10 minutes)

```bash
cd /Users/yunemse48/Development/ASPM/CascadeProjects/windsurf-project

# Option A: Using Docker (Recommended)
docker-compose up -d

# Wait for services to start (30 seconds)
sleep 30

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Option B: Local Development
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Edit .env file with your settings
# Then:
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Step 2: Configure Jira Integration (5 minutes)

1. **Get Jira Credentials:**
   - Go to your Jira instance
   - Create an API token: https://id.atlassian.com/manage-profile/security/api-tokens
   - Note your Jira URL and email

2. **Login to Admin Panel:**
   - Visit: http://localhost:8000/admin
   - Login with your superuser credentials

3. **Create Integration:**
   - Go to "Integrations" → "Add Integration"
   - Fill in:
     - **Name**: "My Jira"
     - **Type**: "JIRA"
     - **Base URL**: Your Jira URL (e.g., https://yourcompany.atlassian.net)
     - **Is Active**: ✓
     - **Configuration**: 
       ```json
       {
         "url": "https://yourcompany.atlassian.net",
         "username": "your-email@company.com",
         "api_token": "your-api-token-here",
         "project_key": "PROJ",
         "max_results": 50
       }
       ```
   - Click "Save"

### Step 3: Test the Integration (2 minutes)

```bash
# Test connection
curl -X POST http://localhost:8000/api/integrations/1/test_connection/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"

# Sync data from Jira
python manage.py sync_jira --integration-id 1

# Or via API
curl -X POST http://localhost:8000/api/integrations/1/sync_now/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"async": false}'
```

### Step 4: Verify It Worked (2 minutes)

1. **Check Change Requests:**
   - Admin: http://localhost:8000/admin/change_requests/changerequest/
   - API: http://localhost:8000/api/change-requests/
   - You should see issues from Jira!

2. **Check Sync Logs:**
   - Admin: http://localhost:8000/admin/integrations/synclog/
   - See the sync results

## 🎯 What You've Built So Far

✅ **Complete Backend Structure**
- Django REST API with authentication
- 5 Django apps (auth, change requests, security analysis, integrations, dashboard)
- Plugin system architecture

✅ **Jira Integration** (NEW!)
- Full Jira API client
- Bidirectional sync capability
- Automatic status/priority mapping
- Celery task for background syncing
- Management command for easy testing

✅ **Infrastructure**
- Docker setup
- PostgreSQL + Redis
- Celery workers

## 🚀 Next Steps (Choose Your Path)

### Path A: Continue Backend (Recommended First)

**Week 2-3: Enhance Jira Integration**
```bash
# Add these features:
1. Bidirectional sync (push updates back to Jira)
2. Comment syncing
3. Attachment handling
4. Webhook receiver for real-time updates
```

**Week 4: Add Scan Execution**
```bash
# Create a simple scanner plugin:
1. SonarQube integration
2. Or a mock scanner for testing
3. Parse findings and store them
```

### Path B: Start Frontend

**Week 2-3: Build Core UI**
```bash
cd frontend
npm install
npm run dev

# Build these components:
1. Login page
2. Dashboard layout
3. Change request list view
4. Integration management UI
```

### Path C: Test & Validate

**Week 2: Get Feedback**
```bash
# Show it to 2-3 AppSec engineers:
1. Demo the Jira sync
2. Show the admin panel
3. Get their feedback
4. Adjust based on needs
```

## 📚 Key Files to Know

### Backend
- `backend/plugins/integrations/jira_plugin.py` - Jira integration logic
- `backend/apps/integrations/tasks.py` - Sync tasks
- `backend/apps/integrations/views.py` - API endpoints
- `backend/apps/change_requests/models.py` - Data models

### Configuration
- `backend/.env` - Environment variables
- `docker-compose.yml` - Docker services
- `backend/config/settings.py` - Django settings

### Documentation
- `TODO.md` - Full development roadmap
- `PROJECT_SUMMARY.md` - Business analysis
- `ARCHITECTURE.md` - Technical architecture

## 🐛 Troubleshooting

### Jira Connection Fails
```bash
# Check your credentials
# Verify API token is correct
# Ensure Jira URL doesn't have trailing slash
# Check firewall/network access
```

### No Issues Synced
```bash
# Verify project_key in configuration
# Check JQL query if using custom one
# Look at sync logs in admin panel
# Check Django logs: backend/logs/django.log
```

### Celery Not Working
```bash
# Make sure Redis is running
redis-cli ping

# Start Celery worker manually
cd backend
celery -A config worker -l info
```

## 💡 Pro Tips

1. **Use the Admin Panel**: It's your best friend for testing and debugging
2. **Check the Logs**: `backend/logs/django.log` has all the details
3. **Test with Postman**: Use the Swagger UI to explore the API
4. **Start Small**: Get one feature working perfectly before moving on
5. **Commit Often**: Use git to track your progress

## 🎓 Learning Resources

### Django
- Official Tutorial: https://docs.djangoproject.com/en/5.0/intro/tutorial01/
- DRF Quickstart: https://www.django-rest-framework.org/tutorial/quickstart/

### React
- Official Tutorial: https://react.dev/learn
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/

### Jira API
- Documentation: https://developer.atlassian.com/cloud/jira/platform/rest/v3/

## 🤝 Need Help?

### Common Questions

**Q: How do I get a JWT token for API testing?**
```bash
# Login to get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

**Q: How do I add more integrations?**
```bash
# Create a new plugin in: backend/plugins/integrations/
# Follow the pattern in jira_plugin.py
# Register it in the plugin registry
```

**Q: Can I test without Jira?**
```bash
# Yes! Create change requests manually in admin panel
# Or use the API to create test data
```

## ✅ Today's Checklist

- [ ] Environment is running (Docker or local)
- [ ] Migrations completed
- [ ] Superuser created
- [ ] Jira integration configured
- [ ] First sync completed successfully
- [ ] Change requests visible in admin panel
- [ ] Decided on next steps (backend, frontend, or validation)

## 🎯 Your Current Status

**✅ COMPLETED:**
- Project structure
- Backend foundation
- Jira integration plugin
- Sync functionality
- Management commands

**🚧 IN PROGRESS:**
- Setting up development environment
- Testing Jira integration

**📋 NEXT UP:**
- Choose your path (backend, frontend, or validation)
- Build next feature
- Get user feedback

---

**You're doing great! The hardest part (setup) is done. Now it's time to build and iterate.** 🚀

**Remember**: Ship fast, get feedback, iterate. Don't aim for perfection on the first try!
