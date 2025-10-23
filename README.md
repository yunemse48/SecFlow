# AppSec Management Dashboard

> API-first Application Security Orchestration Platform

## Overview

AppSec Management Dashboard is a comprehensive platform designed to centralize and streamline application security workflows. It provides bidirectional integrations with ITSM tools, vulnerability scanners, and ticketing systems to help AppSec teams efficiently manage security analysis processes.

## Features (MVP)

- **Change Request Management**: Bidirectional integration with ITSM tools (Jira, ServiceNow)
- **Security Analysis Workflow**: Start/end analysis, select scan types (SAST, DAST, SCA)
- **Dashboard & Metrics**: Track pending, in-progress, and completed security reviews
- **Authentication & Authorization**: OAuth2/SAML, role-based access control
- **API-First Design**: RESTful API with comprehensive documentation

## Tech Stack

### Backend
- **Framework**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL 16
- **Cache/Queue**: Redis 7
- **Task Queue**: Celery
- **API Documentation**: drf-spectacular (OpenAPI 3)

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: TailwindCSS + shadcn/ui
- **State Management**: React Query + Zustand
- **Build Tool**: Vite

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes-ready
- **CI/CD**: GitHub Actions

## Security

We take security seriously. Here are the security measures implemented in this project:

### Secret Management
- **Environment Variables**: All sensitive configuration is managed through environment variables
- **`.env` File Protection**: `.env` is in `.gitignore` to prevent accidental commits of secrets
- **`.env.example`**: Template for required environment variables

### Git Security
- **git-secrets**: Prevents committing sensitive data (API keys, tokens, credentials)
- **`.gitattributes`**: Prevents accidental commits of sensitive files
- **`SECURITY.md`**: Security policy and reporting guidelines

### Pre-commit Hooks
- **git-secrets**: Scans for sensitive data before commits
- **Pattern Matching**: Blocks commits containing potential secrets or sensitive data

### Secure Configuration
- **Docker Security**: Non-root user in containers, minimal base images
- **Database Security**: Password authentication, encrypted connections
- **API Security**: CORS, rate limiting, CSRF protection

### Dependencies
- **Dependabot**: Automated dependency updates
- **Vulnerability Scanning**: Regular security audits

To report security vulnerabilities, please see our [SECURITY.md](SECURITY.md) file.

## Security

### Git Secrets Protection

This repository uses [git-secrets](https://github.com/awslabs/git-secrets) to prevent accidental commits of sensitive information like API keys and credentials.

#### Setup

1. Install git-secrets:
   ```bash
   # For macOS
   brew install git-secrets
   
   # For Linux
   git clone https://github.com/awslabs/git-secrets.git
   cd git-secrets
   sudo make install
   ```

2. Run the setup script:
   ```bash
   ./scripts/setup-git-secrets.sh
   ```

#### How It Works

- The pre-commit hook will block any commits containing sensitive patterns
- Common patterns like AWS keys, API tokens, and private keys are detected
- False positives can be allowed by adding them to `.gitallowed`

#### Testing the Setup

To verify the setup is working:
```bash
echo "SECRET_KEY=test123" > test.txt
git add test.txt
git commit -m "Test commit"  # This should be blocked
```

## Project Structure

```
.
├── backend/                 # Django application
│   ├── apps/               # Django apps (modular components)
│   ├── config/             # Project settings
│   ├── plugins/            # Plugin system architecture
│   └── manage.py
├── frontend/               # React application
│   ├── src/
│   ├── public/
│   └── package.json
├── docker/                 # Docker configurations
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

### Quick Start with Docker

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api
# Admin Panel: http://localhost:8000/admin
```

### Local Development Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Start development server
npm run dev
```

## Security

This project is built with security-first principles:

- **OWASP Top 10 Compliance**: Protection against common vulnerabilities
- **Input Validation**: Comprehensive sanitization and validation
- **Parameterized Queries**: SQL injection prevention
- **CSRF Protection**: Built-in Django CSRF middleware
- **XSS Prevention**: Content Security Policy headers
- **Secrets Management**: Environment-based configuration
- **Audit Logging**: Comprehensive activity tracking

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- ReDoc: http://localhost:8000/api/schema/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

TBD

## Roadmap

### Phase 1 (MVP) - Current
- [x] Project setup
- [ ] Authentication & authorization
- [ ] Change request integration (Jira)
- [ ] Security analysis workflow
- [ ] Basic dashboard

### Phase 2
- [ ] Vulnerability management
- [ ] Additional ITSM integrations (ServiceNow)
- [ ] Advanced reporting
- [ ] Webhook support

### Phase 3
- [ ] CNAPP integrations
- [ ] Container & cloud security dashboard
- [ ] 3rd party product security tracking
- [ ] Infrastructure inventory

## Support

For questions and support, please open an issue in the repository.
