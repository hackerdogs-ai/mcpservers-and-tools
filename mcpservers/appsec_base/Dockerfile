# Base Dockerfile for Application Security MCP Servers
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy base server code
COPY appsec_base_server.py .

# Set Python path
ENV PYTHONPATH=/app:/app/tools:/app/application_security_tools

# Default command (can be overridden by child images)
CMD ["python", "-c", "print('Base server - use specialized server')"]

