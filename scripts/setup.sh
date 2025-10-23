#!/bin/bash

# Setup script for AppSec Management Dashboard

echo "🚀 Setting up AppSec Management Dashboard..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 20 or higher."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Backend setup
echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your configuration"
fi

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Copy environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update backend/.env with your database and Redis configuration"
echo "2. Run: cd backend && source venv/bin/activate"
echo "3. Run: python manage.py migrate"
echo "4. Run: python manage.py createsuperuser"
echo "5. Run: python manage.py runserver"
echo ""
echo "In another terminal:"
echo "6. Run: cd frontend && npm run dev"
echo ""
echo "Or use Docker:"
echo "docker-compose up -d"
