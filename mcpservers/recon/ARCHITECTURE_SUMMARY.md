# Application Security MCP Servers - Architecture Summary

## Overview

This document summarizes the complete architecture for deploying 24+ application security tools as MCP servers with Docker and uvx support.

## Key Requirements

✅ **Multi-Server Architecture**: Split into 9 category-based servers (not one large server)  
✅ **Docker Deployment**: Each server runs in its own Docker container  
✅ **uvx Deployment**: Alternative deployment via uvx (Python package runner)  
✅ **Inter-Container Communication**: Servers called from another Docker container via stdio  
✅ **Zero Code Changes**: Use existing tool code as-is with thin wrappers  

## Architecture Documents

1. **[MULTI_SERVER_ARCHITECTURE_PROPOSAL.md](./MULTI_SERVER_ARCHITECTURE_PROPOSAL.md)**
   - Why split into multiple servers
   - Server categories and organization
   - Base server implementation

2. **[CONTAINERIZED_DEPLOYMENT_ARCHITECTURE.md](./CONTAINERIZED_DEPLOYMENT_ARCHITECTURE.md)**
   - Docker deployment details
   - uvx deployment setup
   - Inter-container communication
   - Path resolution in containers

3. **[TOOL_MIGRATION_CHECKLIST.md](./TOOL_MIGRATION_CHECKLIST.md)**
   - Tool-by-tool migration details
   - Method signatures
   - Implementation status

4. **[SINGLE_VS_MULTI_SERVER_COMPARISON.md](./SINGLE_VS_MULTI_SERVER_COMPARISON.md)**
   - Detailed comparison
   - Performance analysis
   - Decision matrix

## Server Structure

### 9 Specialized MCP Servers

| Server | Tools | Docker Image | uvx Package |
|--------|-------|--------------|-------------|
| `appsec_sast_mcp` | 4 | `appsec-sast-mcp:latest` | `appsec-sast-mcp` |
| `appsec_dast_mcp` | 6 | `appsec-dast-mcp:latest` | `appsec-dast-mcp` |
| `appsec_secrets_mcp` | 3 | `appsec-secrets-mcp:latest` | `appsec-secrets-mcp` |
| `appsec_container_mcp` | 2 | `appsec-container-mcp:latest` | `appsec-container-mcp` |
| `appsec_iac_mcp` | 2 | `appsec-iac-mcp:latest` | `appsec-iac-mcp` |
| `appsec_sca_mcp` | 3 | `appsec-sca-mcp:latest` | `appsec-sca-mcp` |
| `appsec_k8s_mcp` | 3 | `appsec-k8s-mcp:latest` | `appsec-k8s-mcp` |
| `appsec_supply_chain_mcp` | 1 | `appsec-supply-chain-mcp:latest` | `appsec-supply-chain-mcp` |
| `appsec_mobile_mcp` | 1 | `appsec-mobile-mcp:latest` | `appsec-mobile-mcp` |

## Deployment Methods

### 1. Docker Deployment

```bash
# Build
docker build -t appsec-sast-mcp:latest ./appsec_sast

# Run
docker run -it --rm \
  -v /path/to/tools:/app/application_security_tools:ro \
  -e GITHUB_TOKEN="${GITHUB_TOKEN}" \
  appsec-sast-mcp:latest
```

### 2. uvx Deployment

```bash
# Install and run
uvx appsec-sast-mcp

# With environment
GITHUB_TOKEN=xxx uvx appsec-sast-mcp
```

### 3. MCP Client Configuration

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

## Implementation Phases

### Phase 1: Base Infrastructure (Week 1)
- [ ] Create `appsec_base_server.py` with container support
- [ ] Create base Dockerfile
- [ ] Create base pyproject.toml
- [ ] Test path resolution in containers

### Phase 2: First 3 Servers (Week 2)
- [ ] `appsec_sast_mcp` (4 tools)
- [ ] `appsec_dast_mcp` (6 tools)
- [ ] `appsec_secrets_mcp` (3 tools)
- [ ] Test Docker and uvx deployment
- [ ] Test inter-container communication

### Phase 3: Remaining Servers (Week 3)
- [ ] `appsec_container_mcp` (2 tools)
- [ ] `appsec_iac_mcp` (2 tools)
- [ ] `appsec_sca_mcp` (3 tools)
- [ ] `appsec_k8s_mcp` (3 tools)
- [ ] `appsec_supply_chain_mcp` (1 tool)
- [ ] `appsec_mobile_mcp` (1 tool)

### Phase 4: Production Readiness (Week 4)
- [ ] Build scripts for all servers
- [ ] Push to container registry
- [ ] Documentation
- [ ] Integration testing
- [ ] Performance testing

## Key Implementation Details

### Path Resolution

The base server automatically resolves the path to `application_security/tools`:

1. **Environment Variable**: `APPSEC_TOOLS_PATH`
2. **Docker Volume**: `/app/application_security_tools`
3. **Relative Path**: For local development

### Tool Wrapper Pattern

Each tool wrapper:
- Imports existing Scanner class (no code changes)
- Handles path resolution
- Preserves all method signatures
- Returns standardized results

### Container Communication

- **Transport**: stdio (stdin/stdout)
- **Network**: None required (uses Docker's stdio)
- **Volumes**: Mount application_security tools as read-only
- **Environment**: Pass tokens and configuration via env vars

## Benefits

✅ **Performance**: Faster tool discovery (2-6 tools/server vs 24+)  
✅ **Organization**: Clear categorization  
✅ **Maintenance**: Independent updates per category  
✅ **Deployment**: Docker and uvx support  
✅ **Scalability**: Scale only needed servers  
✅ **Flexibility**: Teams use only relevant servers  

## Next Steps

1. Review architecture documents
2. Create base server with container support
3. Implement first server (appsec_sast_mcp) as proof of concept
4. Test Docker and uvx deployment
5. Scale to remaining servers

## Questions?

See detailed documentation:
- [Multi-Server Architecture](./MULTI_SERVER_ARCHITECTURE_PROPOSAL.md)
- [Containerized Deployment](./CONTAINERIZED_DEPLOYMENT_ARCHITECTURE.md)
- [Tool Migration Checklist](./TOOL_MIGRATION_CHECKLIST.md)

