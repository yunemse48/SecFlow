# AppSec Management Dashboard - Architecture

## Overview

The AppSec Management Dashboard is built as a modern, API-first application with a clear separation between backend and frontend. The architecture is designed to be modular, scalable, and extensible through a plugin system.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  (React + TypeScript + TailwindCSS + React Query)           │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ REST API / GraphQL
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                             │
│              (Django REST Framework)                         │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Django     │  │   Plugin     │  │  Background  │
│    Apps      │  │   System     │  │    Tasks     │
│              │  │              │  │   (Celery)   │
└──────────────┘  └──────────────┘  └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │    Redis     │  │  External    │
│   Database   │  │ Cache/Queue  │  │  Services    │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Backend Architecture

### Django Apps Structure

The backend is organized into modular Django apps, each responsible for a specific domain:

#### 1. **Authentication** (`apps.authentication`)
- User management and authentication
- Role-based access control (RBAC)
- API key management
- JWT token handling

**Models:**
- `User`: Custom user model with roles
- `APIKey`: API keys for programmatic access

#### 2. **Change Requests** (`apps.change_requests`)
- Change request lifecycle management
- Integration with ITSM systems
- Comments and attachments

**Models:**
- `ChangeRequest`: Main change request entity
- `ChangeRequestComment`: Comments on change requests
- `ChangeRequestAttachment`: File attachments

#### 3. **Security Analysis** (`apps.security_analysis`)
- Security analysis workflow
- Scan management
- Finding tracking

**Models:**
- `SecurityAnalysis`: Analysis session
- `ScanType`: Types of security scans
- `Scan`: Individual scan execution
- `Finding`: Security findings/vulnerabilities

#### 4. **Integrations** (`apps.integrations`)
- External system integrations
- Bidirectional sync
- Webhook management

**Models:**
- `Integration`: Integration configuration
- `SyncLog`: Sync operation logs
- `Webhook`: Webhook configurations

#### 5. **Dashboard** (`apps.dashboard`)
- Aggregated statistics
- User-specific dashboards
- Reporting endpoints

**No models** - Uses aggregated data from other apps

### Plugin System

The plugin system allows extending functionality without modifying core code.

**Plugin Types:**
- `IntegrationPlugin`: For external system integrations (Jira, ServiceNow, etc.)
- `ScannerPlugin`: For security scanners (SAST, DAST, SCA tools)
- `NotificationPlugin`: For notification channels (Email, Slack, etc.)

**Architecture:**
```python
BasePlugin (Abstract)
├── IntegrationPlugin
│   ├── JiraPlugin
│   ├── ServiceNowPlugin
│   └── GitHubPlugin
├── ScannerPlugin
│   ├── SonarQubePlugin
│   ├── SnykPlugin
│   └── CheckmarxPlugin
└── NotificationPlugin
    ├── EmailPlugin
    └── SlackPlugin
```

**Plugin Registry:**
- Centralized plugin management
- Dynamic loading/unloading
- Configuration management

## Frontend Architecture

### Technology Stack
- **React 18**: UI framework
- **TypeScript**: Type safety
- **React Router**: Client-side routing
- **React Query**: Server state management
- **Zustand**: Client state management
- **TailwindCSS**: Styling
- **Vite**: Build tool

### Component Structure
```
src/
├── components/       # Reusable UI components
├── pages/           # Page components
├── hooks/           # Custom React hooks
├── services/        # API service layer
├── store/           # Zustand stores
├── types/           # TypeScript types
└── utils/           # Utility functions
```

## Data Flow

### Change Request Workflow

```
1. External System (Jira/ServiceNow)
   │
   ▼
2. Integration Plugin fetches change request
   │
   ▼
3. ChangeRequest created in database
   │
   ▼
4. AppSec Engineer assigned
   │
   ▼
5. SecurityAnalysis created
   │
   ▼
6. Scans executed (via ScannerPlugins)
   │
   ▼
7. Findings created and tracked
   │
   ▼
8. Analysis completed
   │
   ▼
9. Results synced back to external system
```

## Security Architecture

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- API key support for integrations
- OAuth2/SAML support (planned)

### Security Measures
- **Input Validation**: All inputs validated and sanitized
- **SQL Injection Prevention**: Parameterized queries via Django ORM
- **XSS Prevention**: Content Security Policy headers
- **CSRF Protection**: Django CSRF middleware
- **Rate Limiting**: API rate limiting
- **Secrets Management**: Environment-based configuration
- **Audit Logging**: Comprehensive activity tracking

### OWASP Top 10 Compliance
- A01: Broken Access Control → RBAC implementation
- A02: Cryptographic Failures → Encrypted credentials
- A03: Injection → Parameterized queries
- A04: Insecure Design → Security-first architecture
- A05: Security Misconfiguration → Secure defaults
- A06: Vulnerable Components → Regular dependency updates
- A07: Authentication Failures → JWT + strong password policies
- A08: Software and Data Integrity → Code signing, integrity checks
- A09: Logging Failures → Comprehensive logging
- A10: SSRF → Input validation and allowlisting

## Database Schema

### Key Relationships

```
User ──┬── ChangeRequest (assigned_to)
       ├── SecurityAnalysis (analyst)
       ├── APIKey
       └── Integration (created_by)

ChangeRequest ──┬── SecurityAnalysis
                ├── ChangeRequestComment
                └── ChangeRequestAttachment

SecurityAnalysis ──── Scan ──── Finding

Integration ──── SyncLog
```

### Indexes
- `ChangeRequest`: external_id, status, priority
- `SecurityAnalysis`: status, analyst
- `Scan`: status, scan_type
- `Finding`: severity, status

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Session data in Redis
- Database connection pooling
- Load balancer ready

### Caching Strategy
- Redis for session storage
- Query result caching
- API response caching

### Background Processing
- Celery for async tasks
- Celery Beat for scheduled tasks
- Task queues for long-running operations

### Database Optimization
- Proper indexing
- Query optimization
- Connection pooling
- Read replicas (future)

## Deployment Architecture

### Docker Containers
- `backend`: Django application
- `frontend`: React application
- `postgres`: Database
- `redis`: Cache and message broker
- `celery`: Background worker
- `celery-beat`: Scheduled tasks

### Kubernetes Ready
- Stateless design
- Health check endpoints
- Graceful shutdown
- Environment-based configuration

## Monitoring & Observability

### Logging
- Structured logging
- Log aggregation ready
- Error tracking (Sentry integration)

### Metrics
- API response times
- Database query performance
- Celery task metrics
- Custom business metrics

### Health Checks
- `/health/`: Application health
- Database connectivity
- Redis connectivity
- External service status

## Future Enhancements

### Phase 2
- GraphQL API
- Real-time updates (WebSockets)
- Advanced reporting
- Multi-tenancy support

### Phase 3
- Machine learning for risk scoring
- Automated remediation suggestions
- Advanced analytics dashboard
- Mobile application

## Technology Decisions

### Why Django?
- Mature security features
- Built-in admin panel
- Strong ORM
- Large ecosystem
- Excellent documentation

### Why React?
- Component-based architecture
- Large ecosystem
- Strong TypeScript support
- Excellent developer experience

### Why PostgreSQL?
- ACID compliance
- JSON support
- Advanced indexing
- Proven scalability

### Why Redis?
- Fast in-memory storage
- Pub/Sub support
- Celery compatibility
- Session storage

## Development Workflow

### Git Workflow
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: Feature branches
- `hotfix/*`: Urgent fixes

### CI/CD Pipeline
1. Code push
2. Linting and formatting
3. Unit tests
4. Integration tests
5. Build Docker images
6. Deploy to staging
7. Manual approval
8. Deploy to production

## API Design Principles

- RESTful design
- Consistent naming conventions
- Versioning support
- Comprehensive documentation (OpenAPI)
- Pagination for list endpoints
- Filtering and search support
- Error handling with proper HTTP status codes
