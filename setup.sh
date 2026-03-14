#!/bin/bash

# Rohit Mobile - Setup Script
# This script sets up the project for development or production

set -e

echo "================================"
echo "Rohit Mobile - Setup Script"
echo "================================"
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✓ Docker is installed"
    use_docker=true
else
    echo "⚠ Docker not found. Will setup for local development."
    use_docker=false
fi

echo ""
echo "Setup Mode:"
echo "1) Docker Setup (Recommended)"
echo "2) Local Python Setup"
read -p "Choose option (1 or 2): " setup_mode

if [ "$setup_mode" = "1" ]; then
    echo ""
    echo "Starting Docker setup..."
    
    # Check docker-compose
    if ! command -v docker-compose &> /dev/null; then
        echo "Error: docker-compose is required"
        exit 1
    fi
    
    # Copy env if not exists
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        echo "⚠ Please edit .env and add your API keys"
    fi
    
    # Build and start
    echo "Building Docker images..."
    docker-compose build
    
    echo "Starting services (this may take a minute)..."
    docker-compose up -d
    
    # Wait for web service
    echo "Waiting for web service to be ready..."
    sleep 5
    
    # Run migrations
    echo "Running migrations..."
    docker-compose exec -T web python manage.py migrate
    
    # Create superuser prompt
    echo ""
    echo "Create superuser account (for admin panel):"
    docker-compose exec web python manage.py createsuperuser
    
    echo ""
    echo "✅ Docker setup complete!"
    echo ""
    echo "Access the application:"
    echo "  Customer Site: http://localhost"
    echo "  Admin Dashboard: http://localhost/admin-dashboard/"
    echo "  Django Admin: http://localhost/admin/"
    echo "  API: http://localhost/api/products/"
    
elif [ "$setup_mode" = "2" ]; then
    echo ""
    echo "Starting Local Python setup..."
    
    # Check Python
    if ! command -v python &> /dev/null & ! command -v python3 &> /dev/null; then
        echo "Error: Python is required"
        exit 1
    fi
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate venv
    source venv/bin/activate
    
    # Copy env if not exists
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        echo "⚠ Please edit .env and add your API keys"
    fi
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    # Run migrations
    echo "Running migrations..."
    python manage.py migrate
    
    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    
    # Create superuser
    echo ""
    echo "Create superuser account (for admin panel):"
    python manage.py createsuperuser
    
    echo ""
    echo "✅ Local setup complete!"
    echo ""
    echo "To start the development server, run:"
    echo "  source venv/bin/activate"
    echo "  python manage.py runserver"
    echo ""
    echo "Then visit: http://localhost:8000"
    
else
    echo "Invalid option"
    exit 1
fi

echo ""
echo "Add sample data (optional):"
if [ "$setup_mode" = "1" ]; then
    echo "  docker-compose exec web python manage.py shell < sample_data.py"
else
    echo "  python manage.py shell < sample_data.py"
fi

echo ""
echo "Setup guide: see QUICK_START.md"
