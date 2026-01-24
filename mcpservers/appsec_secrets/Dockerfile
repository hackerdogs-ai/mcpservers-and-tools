# Secrets MCP Server Dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY appsec_secrets/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY appsec_base/appsec_base_server.py ./appsec_base/
COPY appsec_secrets/appsec_secrets_mcp.py .
COPY appsec_secrets/tools/ ./tools/

ENV PYTHONPATH=/app:/app/tools:/app/application_security_tools
ENV MCP_SERVER_NAME=appsec-secrets-mcp

RUN mkdir -p /app/logs

CMD ["python", "appsec_secrets_mcp.py"]

