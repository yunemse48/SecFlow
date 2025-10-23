#!/bin/bash

# Database initialization script

echo "🗄️  Initializing database..."

cd backend

# Activate virtual environment
source venv/bin/activate

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser
echo ""
echo "Creating superuser..."
python manage.py createsuperuser

echo ""
echo "✅ Database initialized successfully!"
