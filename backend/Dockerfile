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

# Ensure entrypoint is executable and will run migrations at container start
RUN chmod +x entrypoint.sh

# Expose FastAPI port
EXPOSE 8000

# Use entrypoint to run migrations then start API
ENTRYPOINT ["./entrypoint.sh"]
