# Quick Start Guide

Get the AppSec Management Dashboard running in 5 minutes!

## Option 1: Docker (Recommended)

```bash
# 1. Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Start all services
docker-compose up -d

# 3. Wait for services to be ready (30 seconds)
sleep 30

# 4. Run migrations
docker-compose exec backend python manage.py migrate

# 5. Create superuser
docker-compose exec backend python manage.py createsuperuser

# 6. Open your browser
# Frontend: http://localhost:3000
# API: http://localhost:8000/api
# Admin: http://localhost:8000/admin
# API Docs: http://localhost:8000/api/schema/swagger-ui/
```

## Option 2: Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+

### Backend

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and set DEBUG=True

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Frontend

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Start dev server
npm run dev
```

## First Steps

1. **Login to Admin Panel**: http://localhost:8000/admin
2. **Create a Scan Type**: Add SAST, DAST, or SCA scan types
3. **Create an Integration**: Configure Jira or ServiceNow
4. **Create Users**: Add AppSec engineers
5. **Test the API**: Visit http://localhost:8000/api/schema/swagger-ui/

## Common Issues

### Port Already in Use
```bash
# Change backend port
python manage.py runserver 8001

# Change frontend port (edit vite.config.ts)
```

### Database Connection Error
```bash
# Check PostgreSQL is running
pg_isready

# Or use Docker
docker-compose up postgres -d
```

### Redis Connection Error
```bash
# Check Redis is running
redis-cli ping

# Or use Docker
docker-compose up redis -d
```

## Next Steps

- Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup
- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system
- Check [README.md](README.md) for features and roadmap
