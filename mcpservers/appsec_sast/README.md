# Application Security SAST MCP Server

MCP server providing Static Application Security Testing (SAST) tools:
- **Semgrep**: Multi-language SAST with 1000+ rules
- **SonarQube**: Code quality + security analysis
- **Horusec**: Multi-language security orchestration
- **Bearer**: SAST with data flow analysis

## Deployment

### Docker

```bash
# Build
docker build -t appsec-sast-mcp:latest .

# Run
docker run -it --rm \
  -v /path/to/application_security/tools:/app/application_security_tools:ro \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  appsec-sast-mcp:latest
```

### uvx

```bash
# Install and run
uvx appsec-sast-mcp

# With environment
GITHUB_TOKEN=xxx uvx appsec-sast-mcp
```

### Docker Compose

```bash
docker-compose up
```

## MCP Client Configuration

```json
{
  "mcp_servers": {
    "appsec_sast": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run", "--rm", "-i", "--network", "none",
        "-e", "GITHUB_TOKEN={{env.GITHUB_TOKEN}}",
        "-v", "/path/to/tools:/app/application_security_tools:ro",
        "appsec-sast-mcp:latest"
      ]
    }
  }
}
```

## Tools

All tools support scanning GitHub repositories:
- `semgrep_scan_repository(repo_url, ...)`
- `sonarqube_scan_repository(repo_url, ...)`
- `horusec_scan_repository(repo_url, ...)`
- `bearer_scan_repository(repo_url, ...)`

See individual tool files for parameter details.

