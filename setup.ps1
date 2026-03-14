# Rohit Mobile - Setup Script for Windows PowerShell

function Show-Menu {
    Write-Host ""
    Write-Host "================================"
    Write-Host "Rohit Mobile - Setup Script"
    Write-Host "================================"
    Write-Host ""
    Write-Host "Setup Mode:"
    Write-Host "1) Docker Setup (Recommended)"
    Write-Host "2) Local Python Setup"
    Write-Host ""
}

function Setup-Docker {
    Write-Host "Starting Docker setup..."
    Write-Host ""
    
    # Check docker
    if ((Get-Command docker -ErrorAction SilentlyContinue) -eq $null) {
        Write-Host "Error: Docker is not installed or not in PATH"
        exit 1
    }
    
    # Copy env
    if (-not (Test-Path ".env")) {
        Write-Host "Creating .env file..."
        Copy-Item ".env.example" ".env"
        Write-Host "Warning: Please edit .env and add your API keys"
    }
    
    Write-Host "Building Docker images..."
    docker-compose build
    
    Write-Host "Starting services (this may take a minute)..."
    docker-compose up -d
    
    Write-Host "Waiting for web service to be ready..."
    Start-Sleep -Seconds 5
    
    Write-Host "Running migrations..."
    docker-compose exec -T web python manage.py migrate
    
    Write-Host ""
    Write-Host "Create superuser account (for admin panel):"
    docker-compose exec web python manage.py createsuperuser
    
    Write-Host ""
    Write-Host "Docker setup complete!"
    Write-Host ""
    Write-Host "Access the application:"
    Write-Host "  Customer Site: http://localhost"
    Write-Host "  Admin Dashboard: http://localhost/admin-dashboard/"
    Write-Host "  Django Admin: http://localhost/admin/"
    Write-Host "  API: http://localhost/api/products/"
    Write-Host ""
    Write-Host "Add sample data (optional):"
    Write-Host "  docker-compose exec web python manage.py shell < sample_data.py"
}

function Setup-Local {
    Write-Host "Starting Local Python setup..."
    Write-Host ""
    
    # Check Python
    if ((Get-Command python -ErrorAction SilentlyContinue) -eq $null) {
        Write-Host "Error: Python is not installed or not in PATH"
        exit 1
    }
    
    # Create venv
    if (-not (Test-Path "venv")) {
        Write-Host "Creating virtual environment..."
        python -m venv venv
    }
    
    Write-Host "Activating virtual environment..."
    & ".\venv\Scripts\Activate.ps1"
    
    # Copy env
    if (-not (Test-Path ".env")) {
        Write-Host "Creating .env file..."
        Copy-Item ".env.example" ".env"
        Write-Host "Warning: Please edit .env and add your API keys"
    }
    
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
    
    Write-Host "Running migrations..."
    python manage.py migrate
    
    Write-Host "Collecting static files..."
    python manage.py collectstatic --noinput
    
    Write-Host ""
    Write-Host "Create superuser account (for admin panel):"
    python manage.py createsuperuser
    
    Write-Host ""
    Write-Host "Local setup complete!"
    Write-Host ""
    Write-Host "To start the development server, run:"
    Write-Host "  .\venv\Scripts\Activate.ps1"
    Write-Host "  python manage.py runserver"
    Write-Host ""
    Write-Host "Then visit: http://localhost:8000"
    Write-Host ""
    Write-Host "Add sample data (optional):"
    Write-Host "  python manage.py shell < sample_data.py"
}

# Main
Show-Menu
$choice = Read-Host "Choose option (1 or 2)"

switch ($choice) {
    "1" { Setup-Docker }
    "2" { Setup-Local }
    default { 
        Write-Host "Invalid option"
        exit 1
    }
}

Write-Host ""
Write-Host "Setup guide: see QUICK_START.md"
