# DAST MCP Server Dockerfile
# Build from parent directory: docker build -f appsec_dast/Dockerfile -t appsec-dast-mcp:latest .
FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY appsec_dast/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY appsec_base/appsec_base_server.py ./appsec_base/
COPY appsec_dast/appsec_dast_mcp.py .
COPY appsec_dast/tools/ ./tools/

ENV PYTHONPATH=/app:/app/tools:/app/application_security_tools
ENV MCP_SERVER_NAME=appsec-dast-mcp

RUN mkdir -p /app/logs

CMD ["python", "appsec_dast_mcp.py"]

