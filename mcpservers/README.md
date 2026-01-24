# Application Security MCP Servers

This directory contains specialized MCP servers for application security tools, organized by category.

## Architecture

- **Base Server**: `appsec_base/` - Shared functionality for all servers
- **9 Specialized Servers**: Each server focuses on a specific security testing category

## Servers

1. **appsec_sast** - Static Application Security Testing (4 tools)
2. **appsec_dast** - Dynamic Application Security Testing (6 tools)
3. **appsec_secrets** - Secret Scanning (3 tools)
4. **appsec_container** - Container Security (2 tools)
5. **appsec_iac** - Infrastructure as Code Security (2 tools)
6. **appsec_sca** - Software Composition Analysis (3 tools)
7. **appsec_k8s** - Kubernetes Security (3 tools)
8. **appsec_supply_chain** - Supply Chain Security (1 tool)
9. **appsec_mobile** - Mobile Security (1 tool)

**Total: 25 tools across 9 servers**

## Quick Start

### Build All Servers

```bash
./build_all_servers.sh
```

### Test a Server

```bash
./test_appsec_sast.sh
```

### Run with Docker

```bash
cd appsec_sast
docker-compose up
```

### Run with uvx

```bash
uvx appsec-sast-mcp
```

## Deployment

All servers support:
- **Docker**: Each server has a Dockerfile
- **uvx**: Each server has pyproject.toml
- **Inter-container communication**: Via stdio transport

See [QUICKSTART.md](./QUICKSTART.md) for detailed instructions.

## Documentation

- [Architecture Summary](./recon/ARCHITECTURE_SUMMARY.md)
- [Containerized Deployment](./recon/CONTAINERIZED_DEPLOYMENT_ARCHITECTURE.md)
- [Implementation Status](./IMPLEMENTATION_STATUS.md)
