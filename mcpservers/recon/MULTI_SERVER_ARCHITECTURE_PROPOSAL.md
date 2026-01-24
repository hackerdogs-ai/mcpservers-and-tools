# Multi-Server Architecture Proposal for Application Security Tools

## Problem Statement

Having 24+ tools in a single MCP server presents several challenges:
1. **Tool Discovery**: MCP clients need to discover all tools at startup - 24+ tools can be slow
2. **Organization**: Hard for users to find relevant tools among many options
3. **Maintenance**: Updates to one category affect the entire server
4. **Deployment**: Can't deploy/update tools independently
5. **Resource Usage**: Loading all tool modules at once uses more memory
6. **User Experience**: Overwhelming tool list in MCP clients

## Proposed Solution: Category-Based MCP Servers

Split tools into **specialized MCP servers** based on their security testing category. This follows the **single responsibility principle** and makes the system more maintainable.

## Recommended Server Structure

### 1. **appsec_sast_mcp** - Static Application Security Testing
**Tools (4):**
- Semgrep
- SonarQube
- Horusec
- Bearer

**Use Case**: Code analysis, static scanning, data flow analysis  
**Target**: Source code repositories  
**Methods**: `scan_repository()`

---

### 2. **appsec_dast_mcp** - Dynamic Application Security Testing
**Tools (6):**
- ZAP (baseline_scan, full_scan, api_scan)
- Nikto
- SQLMap
- Wapiti
- Metasploit
- W3AF

**Use Case**: Runtime testing, web app scanning, penetration testing  
**Target**: Running applications/URLs  
**Methods**: `scan_url()`, `baseline_scan()`, `full_scan()`, `api_scan()`

---

### 3. **appsec_secrets_mcp** - Secret Scanning
**Tools (3):**
- Gitleaks
- TruffleHog
- GitGuardian

**Use Case**: Detect hardcoded secrets, API keys, credentials  
**Target**: Git repositories  
**Methods**: `scan_repository()`

---

### 4. **appsec_container_mcp** - Container Security
**Tools (2):**
- Grype
- Trivy (scan_container, scan_repository)

**Use Case**: Container image vulnerability scanning  
**Target**: Docker images, container registries  
**Methods**: `scan_container()`, `scan_repository()`

---

### 5. **appsec_iac_mcp** - Infrastructure as Code Security
**Tools (2):**
- Checkov
- Terrascan

**Use Case**: IaC misconfiguration detection  
**Target**: Terraform, CloudFormation, Kubernetes manifests  
**Methods**: `scan_repository()`

---

### 6. **appsec_sca_mcp** - Software Composition Analysis
**Tools (3):**
- Syft (SBOM generation)
- Dependency-Check
- Retire.js

**Use Case**: Dependency vulnerability scanning, SBOM generation  
**Target**: Source code repositories  
**Methods**: `scan_repository()`

---

### 7. **appsec_k8s_mcp** - Kubernetes Security
**Tools (3):**
- Kubescape
- Kube-Bench
- Kube-Hunter

**Use Case**: Kubernetes cluster security and compliance  
**Target**: K8s clusters, manifests, container images  
**Methods**: `scan_repository()`, `scan_container()`, `scan_url()`

---

### 8. **appsec_supply_chain_mcp** - Supply Chain Security
**Tools (1):**
- OpenSSF Scorecard

**Use Case**: Open-source project security scoring  
**Target**: GitHub repositories  
**Methods**: `scan_repository()`

---

### 9. **appsec_mobile_mcp** - Mobile Security (Optional)
**Tools (1):**
- MobSF

**Use Case**: Mobile application security testing  
**Target**: Mobile app repositories  
**Methods**: `scan_repository()`

---

## Server Distribution Summary

| Server | Tools | Primary Use Case | Complexity |
|--------|-------|------------------|------------|
| `appsec_sast_mcp` | 4 | Code analysis | Low |
| `appsec_dast_mcp` | 6 | Runtime testing | Medium |
| `appsec_secrets_mcp` | 3 | Secret detection | Low |
| `appsec_container_mcp` | 2 | Container scanning | Low |
| `appsec_iac_mcp` | 2 | IaC security | Low |
| `appsec_sca_mcp` | 3 | Dependency scanning | Low |
| `appsec_k8s_mcp` | 3 | K8s security | Medium |
| `appsec_supply_chain_mcp` | 1 | Supply chain | Low |
| `appsec_mobile_mcp` | 1 | Mobile security | Low |
| **TOTAL** | **25** | - | - |

## Deployment Requirements

### Containerized Deployment

All MCP servers must support:
1. **Docker Deployment**: Each server runs in its own Docker container
2. **uvx Deployment**: Alternative deployment via uvx (Python package runner)
3. **Inter-Container Communication**: Servers called from another Docker container via stdio

See [CONTAINERIZED_DEPLOYMENT_ARCHITECTURE.md](./CONTAINERIZED_DEPLOYMENT_ARCHITECTURE.md) for detailed implementation.

## Implementation Strategy

### Option A: Shared Base Server (Recommended)

Create a **base MCP server class** that all specialized servers inherit from:

```
mcpservers/
├── appsec_base/
│   ├── appsec_base_server.py      # Base server with plugin loader
│   ├── Dockerfile                  # Base Docker image
│   ├── pyproject.toml              # For uvx deployment
│   ├── requirements.txt
│   └── README.md
├── appsec_sast/
│   ├── appsec_sast_mcp.py          # Inherits from base
│   ├── Dockerfile                  # Docker image for this server
│   ├── pyproject.toml              # For uvx deployment
│   ├── docker-compose.yml          # Local development
│   ├── requirements.txt
│   └── tools/
│       ├── semgrep_tool.py
│       ├── sonarqube_tool.py
│       ├── horusec_tool.py
│       └── bearer_tool.py
├── appsec_dast/
│   ├── appsec_dast_mcp.py
│   ├── tools/
│   │   ├── zap_tool.py
│   │   ├── nikto_tool.py
│   │   ├── sqlmap_tool.py
│   │   ├── wapiti_tool.py
│   │   ├── metasploit_tool.py
│   │   └── w3af_tool.py
│   └── requirements.txt
├── appsec_secrets/
│   ├── appsec_secrets_mcp.py
│   ├── tools/
│   │   ├── gitleaks_tool.py
│   │   ├── trufflehog_tool.py
│   │   └── gitguardian_tool.py
│   └── requirements.txt
├── appsec_container/
│   ├── appsec_container_mcp.py
│   ├── tools/
│   │   ├── grype_tool.py
│   │   └── trivy_tool.py
│   └── requirements.txt
├── appsec_iac/
│   ├── appsec_iac_mcp.py
│   ├── tools/
│   │   ├── checkov_tool.py
│   │   └── terrascan_tool.py
│   └── requirements.txt
├── appsec_sca/
│   ├── appsec_sca_mcp.py
│   ├── tools/
│   │   ├── syft_tool.py
│   │   ├── dependency_check_tool.py
│   │   └── retire_js_tool.py
│   └── requirements.txt
├── appsec_k8s/
│   ├── appsec_k8s_mcp.py
│   ├── tools/
│   │   ├── kubescape_tool.py
│   │   ├── kube_bench_tool.py
│   │   └── kube_hunter_tool.py
│   └── requirements.txt
├── appsec_supply_chain/
│   ├── appsec_supply_chain_mcp.py
│   ├── tools/
│   │   └── openssf_scorecard_tool.py
│   └── requirements.txt
└── appsec_mobile/
    ├── appsec_mobile_mcp.py
    ├── tools/
    │   └── mobsf_tool.py
    └── requirements.txt
```

### Base Server Implementation

```python
# appsec_base/appsec_base_server.py
"""
Base MCP Server for Application Security Tools
Provides shared functionality for all appsec MCP servers
"""

from fastmcp import FastMCP
from pathlib import Path
import sys
from typing import Dict, Any
from hd_logging import setup_logger

# Import plugin loader from recon server
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
        logger.info(f"[{server_name}] Initialized")
    
    def register_tools(self):
        """Register all tools from tools directory."""
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

### Specialized Server Example

```python
# appsec_sast/appsec_sast_mcp.py
"""
SAST MCP Server - Static Application Security Testing Tools
"""

import sys
from pathlib import Path

# Add base server to path
base_path = Path(__file__).parent.parent / "appsec_base"
if str(base_path) not in sys.path:
    sys.path.insert(0, str(base_path))

from appsec_base_server import AppSecBaseServer

def main():
    """Run SAST MCP server."""
    server_dir = Path(__file__).parent
    tools_dir = server_dir / "tools"
    
    server = AppSecBaseServer("appsec-sast-mcp", tools_dir)
    server.run()

if __name__ == "__main__":
    main()
```

## Benefits of Multi-Server Architecture

### 1. **Better Organization**
- Users can connect only to relevant servers
- Clear separation of concerns
- Easier to understand tool categories

### 2. **Improved Performance**
- Faster tool discovery (fewer tools per server)
- Lower memory footprint (only load needed tools)
- Independent server startup times

### 3. **Easier Maintenance**
- Update one category without affecting others
- Independent versioning and deployment
- Smaller codebases to maintain

### 4. **Better User Experience**
- Focused tool lists in MCP clients
- Clearer tool naming (no need for prefixes)
- Easier tool discovery

### 5. **Scalability**
- Easy to add new tools to appropriate server
- Can deploy servers independently
- Better resource allocation

### 6. **Flexibility**
- Users can enable/disable entire categories
- Different teams can use different servers
- Can run servers on different machines

## Configuration Example

### MCP Client Configuration

```json
{
  "mcp_servers": {
    "appsec_sast": {
      "type": "stdio",
      "command": "python3",
      "args": ["/path/to/appsec_sast/appsec_sast_mcp.py"]
    },
    "appsec_dast": {
      "type": "stdio",
      "command": "python3",
      "args": ["/path/to/appsec_dast/appsec_dast_mcp.py"]
    },
    "appsec_secrets": {
      "type": "stdio",
      "command": "python3",
      "args": ["/path/to/appsec_secrets/appsec_secrets_mcp.py"]
    }
  }
}
```

### Crew Configuration

```json
{
  "agents": [{
    "id": "sast_analyst",
    "tools": [
      {
        "tool_name": "semgrep_scan",
        "is_mcp_server": true,
        "mcp_server": "appsec_sast",
        "mcp_tool_name": "semgrep_scan_repository"
      }
    ]
  }, {
    "id": "dast_tester",
    "tools": [
      {
        "tool_name": "zap_baseline",
        "is_mcp_server": true,
        "mcp_server": "appsec_dast",
        "mcp_tool_name": "zap_baseline_scan"
      }
    ]
  }]
}
```

## Migration Path

### Phase 1: Create Base Server (Week 1)
1. Extract plugin loader from recon_mcpserver
2. Create appsec_base_server.py
3. Test with one tool

### Phase 2: Create First 3 Servers (Week 2)
1. appsec_sast_mcp (4 tools)
2. appsec_dast_mcp (6 tools)
3. appsec_secrets_mcp (3 tools)

### Phase 3: Create Remaining Servers (Week 3)
4. appsec_container_mcp (2 tools)
5. appsec_iac_mcp (2 tools)
6. appsec_sca_mcp (3 tools)
7. appsec_k8s_mcp (3 tools)
8. appsec_supply_chain_mcp (1 tool)
9. appsec_mobile_mcp (1 tool)

### Phase 4: Testing & Documentation (Week 4)
- Integration testing
- Documentation
- Deployment guides

## Alternative: Consolidated Server with Categories

If you prefer a single server, we could organize tools with **category prefixes**:

- `sast_semgrep_scan_repository()`
- `dast_zap_baseline_scan()`
- `secrets_gitleaks_scan_repository()`

But this is **not recommended** because:
- Still loads all 24+ tools
- Longer tool names
- Harder to maintain
- No independent deployment

## Recommendation

**✅ Use Multi-Server Architecture**

**Reasons:**
1. Better separation of concerns
2. Improved performance and scalability
3. Easier maintenance and updates
4. Better user experience
5. Follows microservices principles
6. Allows independent deployment

**Implementation Effort:**
- Similar effort to single server (shared base class)
- Better long-term maintainability
- More flexible for future growth

## Next Steps

1. ✅ Review and approve architecture
2. Create base server class
3. Create first 3 servers (SAST, DAST, Secrets)
4. Test and iterate
5. Create remaining servers
6. Documentation and deployment

