# Use official Python slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Set the environment variable dynamically
ARG ENVIRONMENT=local
ENV ENVIRONMENT=${ENVIRONMENT}

# Copy the correct .env file
COPY .env.${ENVIRONMENT} .env.${ENVIRONMENT}

# Run migrations
RUN alembic upgrade head

# Expose FastAPI port
EXPOSE 8000

# Set the default command
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
