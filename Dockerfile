FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files (or skip if it fails - will collect on first run)
RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Create media directory
RUN mkdir -p /app/media

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn rohit_mobile_project.wsgi --bind 0.0.0.0:8000 --workers 4"]
