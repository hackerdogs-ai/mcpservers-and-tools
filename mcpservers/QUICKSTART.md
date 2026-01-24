# Application Security MCP Servers - Quick Start Guide

## What's Implemented

✅ **Base Infrastructure**: Container-aware base server class  
✅ **SAST Server**: First specialized server with 4 tools (Semgrep, SonarQube, Horusec, Bearer)  
✅ **Docker Support**: Dockerfiles and build scripts  
✅ **uvx Support**: pyproject.toml for package deployment  
✅ **Tool Wrappers**: Thin wrappers that use existing tool code as-is  

## Quick Start

### 1. Build the SAST Server

```bash
cd mcpservers
./build_all_servers.sh
```

Or build individually:

```bash
# Build from parent directory (includes appsec_base in context)
docker build -f appsec_sast/Dockerfile -t appsec-sast-mcp:latest .
```

### 2. Test the Server

```bash
./test_appsec_sast.sh
```

Or manually:

```bash
docker run -it --rm \
  -v /path/to/hd-cyberdefense/cyberdefense/tasks/application_security/tools:/app/application_security_tools:ro \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  appsec-sast-mcp:latest
```

### 3. Use with MCP Client

```json
{
  "mcp_servers": {
    "appsec_sast": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "--rm", "-i", "--network", "none",
        "-e", "GITHUB_TOKEN={{env.GITHUB_TOKEN}}",
        "-v", "/path/to/application_security/tools:/app/application_security_tools:ro",
        "appsec-sast-mcp:latest"
      ]
    }
  }
}
```

## Available Tools

The SAST server exposes these tools:
- `semgrep_scan_repository(repo_url, ...)`
- `sonarqube_scan_repository(repo_url, ...)`
- `horusec_scan_repository(repo_url, ...)`
- `bearer_scan_repository(repo_url, ...)`

## Path Resolution

The server automatically resolves the path to `application_security/tools` in this order:
1. `APPSEC_TOOLS_PATH` environment variable
2. Docker volume at `/app/application_security_tools`
3. Relative path (for local development)

## Next Steps

1. Test the SAST server implementation
2. Create remaining 8 servers following the same pattern
3. Deploy to container registry
4. Integrate with MCP clients

## Architecture

See detailed documentation:
- [Architecture Summary](./recon/ARCHITECTURE_SUMMARY.md)
- [Containerized Deployment](./recon/CONTAINERIZED_DEPLOYMENT_ARCHITECTURE.md)
- [Implementation Status](./IMPLEMENTATION_STATUS.md)

