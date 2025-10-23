# AppSec Management Dashboard - Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (optional)

## Quick Start (Docker)

The easiest way to get started is using Docker:

```bash
# 1. Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Update backend/.env with your settings (optional for development)

# 3. Start all services
docker-compose up -d

# 4. Run migrations
docker-compose exec backend python manage.py migrate

# 5. Create superuser
docker-compose exec backend python manage.py createsuperuser

# 6. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api
# Admin Panel: http://localhost:8000/admin
# API Docs: http://localhost:8000/api/schema/swagger-ui/
```

## Local Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
# Required settings:
# - SECRET_KEY (generate a secure key)
# - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
# - REDIS_URL
# - CELERY_BROKER_URL

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env with your API URL
# VITE_API_URL=http://localhost:8000

# Start development server
npm run dev
```

### Celery Workers (Optional for background tasks)

In separate terminals:

```bash
# Terminal 1: Celery worker
cd backend
source venv/bin/activate
celery -A config worker -l info

# Terminal 2: Celery beat (for scheduled tasks)
cd backend
source venv/bin/activate
celery -A config beat -l info
```

## Database Setup

### PostgreSQL

```bash
# Create database
createdb appsec_dashboard

# Or using psql
psql -U postgres
CREATE DATABASE appsec_dashboard;
CREATE USER appsec_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE appsec_dashboard TO appsec_user;
\q
```

### Redis

```bash
# Start Redis (if not using Docker)
redis-server

# Or on macOS with Homebrew
brew services start redis
```

## Configuration

### Backend Environment Variables

Edit `backend/.env`:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=appsec_dashboard
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/1

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend Environment Variables

Edit `frontend/.env`:

```bash
VITE_API_URL=http://localhost:8000
```

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Building for Production

### Backend

```bash
cd backend
source venv/bin/activate

# Collect static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Frontend

```bash
cd frontend
npm run build

# The built files will be in the dist/ directory
```

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists: `psql -l`

### Redis Connection Issues

- Ensure Redis is running: `redis-cli ping`
- Check Redis URL in `.env`

### Port Already in Use

- Backend (8000): Change port in runserver command
- Frontend (3000): Change port in `vite.config.ts`

### Migration Issues

```bash
# Reset migrations (development only)
python manage.py migrate --fake-initial

# Or drop and recreate database
dropdb appsec_dashboard
createdb appsec_dashboard
python manage.py migrate
```

## Next Steps

1. **Configure Integrations**: Set up Jira, ServiceNow, or other integrations in the admin panel
2. **Create Scan Types**: Define security scan types (SAST, DAST, SCA)
3. **Set Up Users**: Create AppSec engineer accounts with appropriate roles
4. **Test Workflows**: Create a test change request and run through the security analysis workflow

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)

## Support

For issues and questions, please open an issue in the repository.
