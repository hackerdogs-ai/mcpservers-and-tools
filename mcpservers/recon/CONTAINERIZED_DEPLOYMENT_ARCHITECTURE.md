# Containerized Deployment Architecture for Application Security MCP Servers

## Overview

This document extends the multi-server architecture to support:
1. **Docker Deployment**: Each MCP server runs in its own Docker container
2. **uvx Deployment**: Alternative deployment via uvx (Python package runner)
3. **Inter-Container Communication**: MCP servers called from another Docker container via stdio

## Architecture Requirements

### 1. Docker Support
- Each MCP server must have a Dockerfile
- Images published to container registry
- Support for stdio transport (no networking required)
- Volume mounts for accessing application_security tools

### 2. uvx Support
- Each MCP server must have `pyproject.toml`
- Installable as Python package
- Runnable via `uvx appsec-sast-mcp`

### 3. Inter-Container Communication
- MCP client runs in separate Docker container
- Communication via stdio (stdin/stdout)
- No network ports required
- Environment variables for configuration

## Directory Structure

```
mcpservers/
├── appsec_base/
│   ├── appsec_base_server.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
├── appsec_sast/
│   ├── appsec_sast_mcp.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── docker-compose.yml
│   ├── tools/
│   │   ├── semgrep_tool.py
│   │   ├── sonarqube_tool.py
│   │   ├── horusec_tool.py
│   │   └── bearer_tool.py
│   └── README.md
├── appsec_dast/
│   ├── appsec_dast_mcp.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── tools/
│       └── ...
└── docker-compose.all.yml  # Orchestrate all servers
```

## Docker Deployment

### Base Dockerfile Template

```dockerfile
# appsec_base/Dockerfile
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

# Set Python path to include application_security tools
# This assumes tools are mounted as volume or copied
ENV PYTHONPATH=/app:/app/tools:/app/application_security_tools

# Default command (can be overridden)
CMD ["python", "-m", "appsec_base_server"]
```

### Specialized Server Dockerfile

```dockerfile
# appsec_sast/Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install base dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy base server (or install as package)
COPY --from=appsec-base:latest /app/appsec_base_server.py /app/

# Copy server code
COPY appsec_sast_mcp.py .

# Copy tools
COPY tools/ ./tools/

# Set Python path
ENV PYTHONPATH=/app:/app/tools

# Environment variables
ENV APPSEC_TOOLS_PATH=/app/application_security_tools
ENV MCP_SERVER_NAME=appsec-sast-mcp

# Run server
CMD ["python", "appsec_sast_mcp.py"]
```

### Dockerfile with Application Security Tools

Since tools are in a different workspace, we have two options:

#### Option 1: Volume Mount (Recommended for Development)

```dockerfile
# appsec_sast/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY appsec_sast_mcp.py .
COPY tools/ ./tools/

# Set Python path (tools will be mounted at runtime)
ENV PYTHONPATH=/app:/app/tools:/app/application_security_tools

CMD ["python", "appsec_sast_mcp.py"]
```

**Docker Run:**
```bash
docker run -it --rm \
  -v /path/to/hd-cyberdefense/cyberdefense/tasks/application_security/tools:/app/application_security_tools:ro \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  appsec-sast-mcp:latest
```

#### Option 2: Multi-Stage Build (Recommended for Production)

```dockerfile
# appsec_sast/Dockerfile
FROM python:3.11-slim as builder

WORKDIR /build

# Copy application_security tools
COPY --from=appsec-tools:latest /tools /build/application_security_tools

# Copy server code
COPY appsec_sast_mcp.py .
COPY tools/ ./tools/

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy built artifacts
COPY --from=builder /build /app

ENV PYTHONPATH=/app:/app/tools:/app/application_security_tools

CMD ["python", "appsec_sast_mcp.py"]
```

### Docker Compose for Local Development

```yaml
# appsec_sast/docker-compose.yml
version: '3.8'

services:
  appsec-sast-mcp:
    build:
      context: .
      dockerfile: Dockerfile
    image: appsec-sast-mcp:latest
    volumes:
      # Mount application_security tools
      - ../../hd-cyberdefense/cyberdefense/tasks/application_security/tools:/app/application_security_tools:ro
      # Mount logs directory
      - ./logs:/app/logs
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - GITHUB_DEFAULT_TOKEN=${GITHUB_DEFAULT_TOKEN}
      - PYTHONPATH=/app:/app/tools:/app/application_security_tools
    stdin_open: true
    tty: true
    # No ports needed - uses stdio
```

### Docker Compose for All Servers

```yaml
# docker-compose.all.yml
version: '3.8'

services:
  appsec-sast-mcp:
    build:
      context: ./appsec_sast
      dockerfile: Dockerfile
    volumes:
      - ../hd-cyberdefense/cyberdefense/tasks/application_security/tools:/app/application_security_tools:ro
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    stdin_open: true
    tty: true

  appsec-dast-mcp:
    build:
      context: ./appsec_dast
      dockerfile: Dockerfile
    volumes:
      - ../hd-cyberdefense/cyberdefense/tasks/application_security/tools:/app/application_security_tools:ro
    stdin_open: true
    tty: true

  # ... other servers
```

## uvx Deployment

### pyproject.toml Template

```toml
# appsec_sast/pyproject.toml
[project]
name = "appsec-sast-mcp"
version = "0.1.0"
description = "SAST MCP Server for Application Security Tools"
requires-python = ">=3.11"
dependencies = [
    "fastmcp>=2.12.5",
    "hd-logging>=1.0.0",
]

[project.scripts]
appsec-sast-mcp = "appsec_sast_mcp:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

### Running with uvx

```bash
# Install and run
uvx appsec-sast-mcp

# Or with environment variables
GITHUB_TOKEN=xxx uvx appsec-sast-mcp

# Or from local directory
uvx --from ./appsec_sast appsec-sast-mcp
```

## Inter-Container Communication

### MCP Client Container Configuration

The MCP client (running in another Docker container) connects to MCP servers via stdio:

```json
{
  "mcp_servers": {
    "appsec_sast": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--network", "none",  # No network needed for stdio
        "-e", "GITHUB_TOKEN={{env.GITHUB_TOKEN}}",
        "-v", "/path/to/tools:/app/application_security_tools:ro",
        "appsec-sast-mcp:latest"
      ]
    }
  }
}
```

### Docker Network Setup

For inter-container communication, use Docker networks:

```yaml
# docker-compose.client.yml
version: '3.8'

services:
  mcp-client:
    build:
      context: ./mcp_client
    depends_on:
      - appsec-sast-mcp
      - appsec-dast-mcp
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    networks:
      - mcp-network

  appsec-sast-mcp:
    image: appsec-sast-mcp:latest
    volumes:
      - ../tools:/app/application_security_tools:ro
    stdin_open: true
    tty: true
    networks:
      - mcp-network

  appsec-dast-mcp:
    image: appsec-dast-mcp:latest
    volumes:
      - ../tools:/app/application_security_tools:ro
    stdin_open: true
    tty: true
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

### Updated Base Server for Container Support

```python
# appsec_base/appsec_base_server.py
"""
Base MCP Server for Application Security Tools
Container-aware implementation
"""

import os
import sys
from pathlib import Path
from fastmcp import FastMCP
from typing import Dict, Any
from hd_logging import setup_logger

# Import plugin loader
sys.path.insert(0, str(Path(__file__).parent.parent / "recon"))
from recon_mcpserver import PluginLoader, create_mcp_tool_from_function

logger = setup_logger(__name__, log_file_path="logs/appsec_base.log")


class AppSecBaseServer:
    """Base class for all application security MCP servers."""
    
    def __init__(self, server_name: str, tools_dir: Path):
        """
        Initialize base server.
        
        Args:
            server_name: Name of the MCP server
            tools_dir: Directory containing tool plugins
        """
        self.server_name = server_name
        self.mcp = FastMCP(name=server_name)
        self.tools_dir = tools_dir
        
        # Resolve application_security tools path
        self.appsec_tools_path = self._resolve_appsec_tools_path()
        
        # Add to Python path
        if self.appsec_tools_path and str(self.appsec_tools_path) not in sys.path:
            sys.path.insert(0, str(self.appsec_tools_path))
            logger.info(f"[{server_name}] Added appsec tools to path: {self.appsec_tools_path}")
        
        logger.info(f"[{server_name}] Initialized")
        logger.info(f"[{server_name}] Python path: {sys.path}")
    
    def _resolve_appsec_tools_path(self) -> Path:
        """
        Resolve path to application_security tools.
        
        Priority:
        1. APPSEC_TOOLS_PATH environment variable
        2. Mounted volume at /app/application_security_tools
        3. Relative path from current file
        """
        # Check environment variable
        env_path = os.environ.get("APPSEC_TOOLS_PATH")
        if env_path:
            path = Path(env_path)
            if path.exists():
                logger.info(f"[{self.server_name}] Using APPSEC_TOOLS_PATH: {path}")
                return path
        
        # Check Docker volume mount
        docker_path = Path("/app/application_security_tools")
        if docker_path.exists():
            logger.info(f"[{self.server_name}] Using Docker volume: {docker_path}")
            return docker_path
        
        # Try relative path (for local development)
        current_file = Path(__file__).resolve()
        # Navigate: mcpservers/appsec_base -> mcpservers -> hd-cyberdefense/cyberdefense/tasks/application_security/tools
        relative_path = current_file.parents[3] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"
        if relative_path.exists():
            logger.info(f"[{self.server_name}] Using relative path: {relative_path}")
            return relative_path
        
        logger.warning(f"[{self.server_name}] Could not resolve appsec tools path")
        return None
    
    def register_tools(self):
        """Register all tools from tools directory."""
        if not self.tools_dir.exists():
            logger.error(f"[{self.server_name}] Tools directory does not exist: {self.tools_dir}")
            return
        
        loader = PluginLoader(self.tools_dir)
        all_tools = loader.load_all_plugins()
        
        registered_count = 0
        for tool_name, tool_func in all_tools.items():
            try:
                wrapped_func = create_mcp_tool_from_function(tool_func, tool_name)
                wrapped_func.__name__ = tool_name
                decorated_func = self.mcp.tool()(wrapped_func)
                setattr(self.mcp, f"_tool_{tool_name}", decorated_func)
                registered_count += 1
                logger.info(f"[{self.server_name}] Registered tool: {tool_name}")
            except Exception as e:
                logger.error(f"[{self.server_name}] Failed to register {tool_name}: {e}", exc_info=True)
        
        logger.info(f"[{self.server_name}] Registered {registered_count} tool(s)")
    
    def run(self):
        """Run the MCP server."""
        self.register_tools()
        logger.info(f"[{self.server_name}] Starting stdio transport...")
        self.mcp.run(transport='stdio')
```

## Tool Wrapper Updates for Container Support

Each tool wrapper must handle path resolution:

```python
# appsec_sast/tools/semgrep_tool.py
"""
Semgrep SAST Scanner MCP Tool Wrapper
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Resolve application_security tools path
def _get_appsec_tools_path():
    """Get path to application_security tools."""
    # Check environment variable
    env_path = os.environ.get("APPSEC_TOOLS_PATH")
    if env_path:
        return Path(env_path)
    
    # Check Docker volume
    docker_path = Path("/app/application_security_tools")
    if docker_path.exists():
        return docker_path
    
    # Try relative path
    current_file = Path(__file__).resolve()
    relative_path = current_file.parents[5] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"
    if relative_path.exists():
        return relative_path
    
    raise RuntimeError("Could not resolve application_security tools path")

appsec_tools_path = _get_appsec_tools_path()
if str(appsec_tools_path) not in sys.path:
    sys.path.insert(0, str(appsec_tools_path))

from semgrep.semgrep_scan import SemgrepScanner
from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def semgrep_scan_repository(
    repo_url: str,
    output_format: str = "json",
    save_output: bool = True,
    output_dir: Optional[str] = None,
    timeout: int = 600,
    github_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Scan a GitHub repository with Semgrep.
    
    Args:
        repo_url: GitHub repository URL
        output_format: Output format (default: "json")
        save_output: Whether to save output to file (default: True)
        output_dir: Custom output directory (optional)
        timeout: Scan timeout in seconds (default: 600)
        github_token: GitHub Personal Access Token for private repos (optional)
        
    Returns:
        Dictionary with scan results and metadata
    """
    try:
        logger.info(f"[semgrep_scan_repository] Starting scan for: {repo_url}")
        
        # Initialize scanner
        scanner = SemgrepScanner(github_token=github_token)
        
        # Execute scan
        result = scanner.scan_repository(
            repo_url=repo_url,
            output_format=output_format,
            save_output=save_output,
            output_dir=output_dir,
            timeout=timeout,
            github_token=github_token
        )
        
        logger.info(f"[semgrep_scan_repository] Scan completed: success={result.get('success', False)}")
        return result
        
    except Exception as e:
        logger.error(f"[semgrep_scan_repository] Error: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "tool": "semgrep"
        }
```

## Build and Deployment Scripts

### Build Script

```bash
#!/bin/bash
# build_all_servers.sh

set -e

SERVERS=(
    "appsec_sast"
    "appsec_dast"
    "appsec_secrets"
    "appsec_container"
    "appsec_iac"
    "appsec_sca"
    "appsec_k8s"
    "appsec_supply_chain"
    "appsec_mobile"
)

for server in "${SERVERS[@]}"; do
    echo "Building $server..."
    docker build -t "appsec-${server}-mcp:latest" "./${server}"
done

echo "All servers built successfully!"
```

### Push Script

```bash
#!/bin/bash
# push_all_servers.sh

REGISTRY="your-registry.com"
VERSION="${1:-latest}"

SERVERS=(
    "appsec_sast"
    "appsec_dast"
    # ... other servers
)

for server in "${SERVERS[@]}"; do
    echo "Pushing appsec-${server}-mcp:${VERSION}..."
    docker tag "appsec-${server}-mcp:latest" "${REGISTRY}/appsec-${server}-mcp:${VERSION}"
    docker push "${REGISTRY}/appsec-${server}-mcp:${VERSION}"
done
```

## Configuration Examples

### MCP Client Configuration (Docker)

```json
{
  "mcp_servers": {
    "appsec_sast": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--network", "none",
        "-e", "GITHUB_TOKEN={{env.GITHUB_TOKEN}}",
        "-v", "/host/path/to/tools:/app/application_security_tools:ro",
        "your-registry.com/appsec-sast-mcp:latest"
      ]
    },
    "appsec_dast": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--network", "none",
        "your-registry.com/appsec-dast-mcp:latest"
      ]
    }
  }
}
```

### MCP Client Configuration (uvx)

```json
{
  "mcp_servers": {
    "appsec_sast": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "appsec-sast-mcp"
      ],
      "env": {
        "GITHUB_TOKEN": "{{env.GITHUB_TOKEN}}",
        "APPSEC_TOOLS_PATH": "/path/to/application_security/tools"
      }
    }
  }
}
```

## Testing

### Test Docker Deployment

```bash
# Build image
docker build -t appsec-sast-mcp:test ./appsec_sast

# Run with volume mount
docker run -it --rm \
  -v $(pwd)/../hd-cyberdefense/cyberdefense/tasks/application_security/tools:/app/application_security_tools:ro \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  appsec-sast-mcp:test
```

### Test uvx Deployment

```bash
# Install and run
uvx --from ./appsec_sast appsec-sast-mcp

# With environment
GITHUB_TOKEN=xxx APPSEC_TOOLS_PATH=/path/to/tools uvx --from ./appsec_sast appsec-sast-mcp
```

## Summary

This architecture supports:
- ✅ **Docker deployment** with Dockerfiles for each server
- ✅ **uvx deployment** with pyproject.toml for each server
- ✅ **Inter-container communication** via stdio (no networking required)
- ✅ **Volume mounts** for accessing application_security tools
- ✅ **Environment variable** configuration
- ✅ **Path resolution** that works in containers and locally

The stdio transport is perfect for Docker containers as it requires no network configuration and works seamlessly with Docker's stdin/stdout handling.

