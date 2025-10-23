# API Reference - Quick Guide

## 🔐 Authentication

### Get JWT Token
```bash
POST /api/auth/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "your-password"
}

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use Token in Requests
```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 👤 Users

### Get Current User
```bash
GET /api/auth/users/me/
Authorization: Bearer {token}
```

### List Users
```bash
GET /api/auth/users/
Authorization: Bearer {token}
```

### Create User
```bash
POST /api/auth/users/
Authorization: Bearer {token}
Content-Type: application/json

{
  "username": "engineer1",
  "email": "engineer1@company.com",
  "password": "secure-password",
  "password_confirm": "secure-password",
  "first_name": "John",
  "last_name": "Doe",
  "role": "APPSEC_ENGINEER"
}
```

## 📋 Change Requests

### List Change Requests
```bash
GET /api/change-requests/
Authorization: Bearer {token}

# With filters:
GET /api/change-requests/?status=PENDING&priority=HIGH
```

### Get Change Request Details
```bash
GET /api/change-requests/{id}/
Authorization: Bearer {token}
```

### Create Change Request (Manual)
```bash
POST /api/change-requests/
Authorization: Bearer {token}
Content-Type: application/json

{
  "external_id": "CR-001",
  "source": "MANUAL",
  "title": "Deploy new authentication service",
  "description": "Deploying OAuth2 service to production",
  "status": "PENDING",
  "priority": "HIGH",
  "requester": "John Doe",
  "requested_date": "2025-10-23T18:00:00Z"
}
```

### Assign Change Request
```bash
POST /api/change-requests/{id}/assign/
Authorization: Bearer {token}
Content-Type: application/json

{
  "user_id": 2
}
```

### Update Status
```bash
POST /api/change-requests/{id}/update_status/
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "IN_PROGRESS"
}
```

### My Assigned Requests
```bash
GET /api/change-requests/my_requests/
Authorization: Bearer {token}
```

## 🔗 Integrations

### List Integrations
```bash
GET /api/integrations/
Authorization: Bearer {token}
```

### Create Jira Integration
```bash
POST /api/integrations/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Production Jira",
  "type": "JIRA",
  "base_url": "https://company.atlassian.net",
  "is_active": true,
  "sync_enabled": true,
  "sync_interval_minutes": 15,
  "configuration": {
    "url": "https://company.atlassian.net",
    "username": "your-email@company.com",
    "api_token": "your-api-token",
    "project_key": "PROJ",
    "max_results": 50
  }
}
```

### Test Connection
```bash
POST /api/integrations/{id}/test_connection/
Authorization: Bearer {token}
```

### Sync Now
```bash
POST /api/integrations/{id}/sync_now/
Authorization: Bearer {token}
Content-Type: application/json

{
  "async": false
}
```

### View Sync Logs
```bash
GET /api/integrations/sync-logs/
Authorization: Bearer {token}

# Filter by integration:
GET /api/integrations/sync-logs/?integration={id}
```

## 🔍 Security Analysis

### List Security Analyses
```bash
GET /api/security-analysis/
Authorization: Bearer {token}

# Filter by status:
GET /api/security-analysis/?status=IN_PROGRESS
```

### Create Security Analysis
```bash
POST /api/security-analysis/
Authorization: Bearer {token}
Content-Type: application/json

{
  "change_request": 1,
  "notes": "Starting security review"
}
```

### Start Analysis
```bash
POST /api/security-analysis/{id}/start/
Authorization: Bearer {token}
```

### Complete Analysis
```bash
POST /api/security-analysis/{id}/complete/
Authorization: Bearer {token}
Content-Type: application/json

{
  "risk_score": 75,
  "notes": "Found 3 high severity issues. Remediation required."
}
```

## 🔬 Scan Types

### List Scan Types
```bash
GET /api/security-analysis/scan-types/
Authorization: Bearer {token}
```

### Create Scan Type
```bash
POST /api/security-analysis/scan-types/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "SAST",
  "description": "Static Application Security Testing",
  "is_active": true,
  "configuration": {
    "tool": "SonarQube",
    "timeout": 3600
  }
}
```

## 🎯 Scans

### List Scans
```bash
GET /api/security-analysis/scans/
Authorization: Bearer {token}

# Filter by analysis:
GET /api/security-analysis/scans/?security_analysis={id}
```

### Create Scan
```bash
POST /api/security-analysis/scans/
Authorization: Bearer {token}
Content-Type: application/json

{
  "security_analysis": 1,
  "scan_type": 1,
  "status": "QUEUED"
}
```

### Start Scan
```bash
POST /api/security-analysis/scans/{id}/start/
Authorization: Bearer {token}
```

## 🐛 Findings

### List Findings
```bash
GET /api/security-analysis/findings/
Authorization: Bearer {token}

# Filter by severity:
GET /api/security-analysis/findings/?severity=CRITICAL&status=OPEN
```

### Create Finding
```bash
POST /api/security-analysis/findings/
Authorization: Bearer {token}
Content-Type: application/json

{
  "scan": 1,
  "title": "SQL Injection in login endpoint",
  "description": "User input not properly sanitized",
  "severity": "CRITICAL",
  "status": "OPEN",
  "cwe_id": "CWE-89",
  "file_path": "src/auth/login.py",
  "line_number": 45,
  "remediation": "Use parameterized queries"
}
```

### Update Finding Status
```bash
POST /api/security-analysis/findings/{id}/update_status/
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "RESOLVED"
}
```

## 📊 Dashboard

### Get Dashboard Stats
```bash
GET /api/dashboard/stats/
Authorization: Bearer {token}

# Response:
{
  "total_change_requests": 150,
  "pending_change_requests": 25,
  "in_progress_change_requests": 10,
  "completed_change_requests": 115,
  "total_analyses": 100,
  "active_analyses": 8,
  "completed_analyses": 92,
  "total_findings": 450,
  "critical_findings": 12,
  "high_findings": 35,
  "open_findings": 47,
  "avg_analysis_time_hours": 4.5
}
```

### Get My Dashboard
```bash
GET /api/dashboard/my/
Authorization: Bearer {token}

# Response:
{
  "my_change_requests": [
    {"status": "PENDING", "count": 5},
    {"status": "IN_PROGRESS", "count": 3}
  ],
  "my_analyses": [
    {"status": "IN_PROGRESS", "count": 2},
    {"status": "COMPLETED", "count": 15}
  ],
  "recent_change_requests": [...]
}
```

## 🔔 Webhooks

### List Webhooks
```bash
GET /api/integrations/webhooks/
Authorization: Bearer {token}
```

### Create Webhook
```bash
POST /api/integrations/webhooks/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Slack Notifications",
  "url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "events": ["CHANGE_REQUEST_CREATED", "ANALYSIS_COMPLETED"],
  "is_active": true,
  "secret": "your-webhook-secret",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

### Test Webhook
```bash
POST /api/integrations/webhooks/{id}/test/
Authorization: Bearer {token}
```

## 📖 API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔧 Common Filters

Most list endpoints support these query parameters:

### Pagination
```bash
?page=2&page_size=50
```

### Search
```bash
?search=security
```

### Ordering
```bash
?ordering=-created_at  # Descending
?ordering=title        # Ascending
```

### Filtering
```bash
?status=PENDING&priority=HIGH
```

## 📝 Response Formats

### Success Response
```json
{
  "id": 1,
  "field": "value",
  ...
}
```

### List Response
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/resource/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## 🚀 Quick Testing with cURL

### Complete Workflow Example
```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}' \
  | jq -r '.access')

# 2. List change requests
curl -X GET http://localhost:8000/api/change-requests/ \
  -H "Authorization: Bearer $TOKEN"

# 3. Create security analysis
curl -X POST http://localhost:8000/api/security-analysis/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"change_request": 1, "notes": "Starting review"}'

# 4. Start analysis
curl -X POST http://localhost:8000/api/security-analysis/1/start/ \
  -H "Authorization: Bearer $TOKEN"

# 5. Get dashboard stats
curl -X GET http://localhost:8000/api/dashboard/stats/ \
  -H "Authorization: Bearer $TOKEN"
```

## 💡 Pro Tips

1. **Use jq**: Install `jq` for pretty JSON formatting
2. **Save Token**: Store JWT token in environment variable
3. **Postman Collection**: Import OpenAPI schema into Postman
4. **Test in Swagger**: Use the interactive Swagger UI for testing
5. **Check Logs**: Backend logs are in `backend/logs/django.log`

---

**For full API documentation, visit**: http://localhost:8000/api/schema/swagger-ui/
