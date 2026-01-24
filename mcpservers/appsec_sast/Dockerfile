# SAST MCP Server Dockerfile
# Build from parent directory: docker build -f appsec_sast/Dockerfile -t appsec-sast-mcp:latest .
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY appsec_sast/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy base server code
COPY appsec_base/appsec_base_server.py ./appsec_base/

# Copy server code
COPY appsec_sast/appsec_sast_mcp.py .

# Copy tools
COPY appsec_sast/tools/ ./tools/

# Set Python path
ENV PYTHONPATH=/app:/app/tools:/app/application_security_tools

# Environment variables
ENV MCP_SERVER_NAME=appsec-sast-mcp

# Create logs directory
RUN mkdir -p /app/logs

# Run server
CMD ["python", "appsec_sast_mcp.py"]

