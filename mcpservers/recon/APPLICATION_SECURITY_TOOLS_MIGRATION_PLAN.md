# Application Security Tools Migration Plan

## Overview

This document outlines the strategy to migrate 24 application security tools from `tasks/application_security/tools/` into the recon MCP server framework **without modifying the existing tool code**.

## Key Principles

1. **Zero Code Modification**: Use existing tool code as-is
2. **Thin Wrapper Pattern**: Create minimal wrapper functions that import and call existing Scanner classes
3. **Plugin-Based**: Leverage the existing plugin discovery system
4. **Preserve Functionality**: Maintain all existing features, parameters, and return formats

## Tool Analysis Summary

### Tool Patterns Identified

All tools follow a consistent pattern:

1. **Scanner Class**: Each tool has a `*Scanner` class (e.g., `BearerScanner`, `GitleaksScanner`)
2. **Main Methods**: 
   - Most tools: `scan_repository(repo_url, ...)`
   - DAST tools: `scan_url(target_url, ...)` or `baseline_scan()`, `full_scan()`
   - Container tools: `scan_container(image_name, ...)`
3. **Initialization**: All accept Docker image, config_path, and optional github_token
4. **Output**: All return `Dict[str, Any]` with standardized structure
5. **Logging**: All use `hd_logging` package

### Tool Categories & Method Signatures

| Category | Tool | Main Method(s) | Parameters |
|----------|------|----------------|------------|
| **SAST** | Semgrep | `scan_repository()` | repo_url, github_token, output_format, timeout |
| | SonarQube | `scan_repository()` | repo_url, github_token, timeout |
| | Horusec | `scan_repository()` | repo_url, github_token, timeout |
| | Bearer | `scan_repository()` | repo_url, github_token, scan_options, timeout |
| **DAST** | ZAP | `baseline_scan()`, `full_scan()`, `api_scan()` | target_url, timeout |
| | Nikto | `scan_url()` | target_url, timeout |
| | SQLMap | `scan_url()` | target_url, timeout |
| | Wapiti | `scan_url()` | target_url, timeout |
| | Metasploit | `scan_url()` | target_url, timeout |
| | W3AF | `scan_url()` | target_url, timeout |
| **Container** | Grype | `scan_container()` | image_name, timeout |
| | Trivy | `scan_container()`, `scan_repository()` | image_name/repo_url, timeout |
| **IaC** | Checkov | `scan_repository()` | repo_url, github_token, timeout |
| | Terrascan | `scan_repository()` | repo_url, github_token, timeout |
| **Secret** | Gitleaks | `scan_repository()` | repo_url, github_token, scan_git_history, timeout |
| | TruffleHog | `scan_repository()` | repo_url, github_token, timeout |
| | GitGuardian | `scan_repository()` | repo_url, github_token, timeout |
| **SCA** | Syft | `scan_repository()` | repo_url, github_token, timeout |
| | Dependency-Check | `scan_repository()` | repo_url, github_token, timeout |
| | Retire.js | `scan_repository()` | repo_url, github_token, timeout |
| **K8s** | Kubescape | `scan_repository()` | repo_url, github_token, timeout |
| | Kube-Bench | `scan_container()` | image_name, timeout |
| | Kube-Hunter | `scan_url()` | target_url, timeout |
| **Supply Chain** | OpenSSF Scorecard | `scan_repository()` | repo_url, github_token, timeout |
| **Mobile** | MobSF | `scan_repository()` | repo_url, github_token, timeout |

## Migration Strategy

### Phase 1: Create Wrapper Generator Script

Create a script that automatically generates wrapper functions for all tools:

**File**: `mcpservers/recon/tools/generate_appsec_wrappers.py`

This script will:
1. Scan `tasks/application_security/tools/` directory
2. For each `*_scan.py` file:
   - Detect the Scanner class name
   - Detect main scan method(s)
   - Generate wrapper function(s) that:
     - Import the Scanner class
     - Initialize with default parameters
     - Call the scan method
     - Return results

### Phase 2: Wrapper Function Template

Each wrapper will follow this pattern:

```python
# mcpservers/recon/tools/gitleaks_tool.py
"""
Gitleaks Secret Scanner MCP Tool Wrapper
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add application_security tools to path
appsec_tools_path = Path(__file__).resolve().parents[4] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"
if str(appsec_tools_path) not in sys.path:
    sys.path.insert(0, str(appsec_tools_path))

from gitleaks.gitleaks_scan import GitleaksScanner
from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def gitleaks_scan_repository(
    repo_url: str,
    scan_git_history: bool = False,
    output_format: str = "json",
    save_output: bool = True,
    output_dir: Optional[str] = None,
    timeout: int = 300,
    github_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Scan a GitHub repository with Gitleaks for hardcoded secrets.
    
    Args:
        repo_url: GitHub repository URL
        scan_git_history: Whether to scan git history (default: False)
        output_format: Output format (default: "json")
        save_output: Whether to save output to file (default: True)
        output_dir: Custom output directory (optional)
        timeout: Scan timeout in seconds (default: 300)
        github_token: GitHub Personal Access Token for private repos (optional)
        
    Returns:
        Dictionary with scan results and metadata
    """
    try:
        logger.info(f"[gitleaks_scan_repository] Starting scan for: {repo_url}")
        
        # Initialize scanner with default image
        scanner = GitleaksScanner(github_token=github_token)
        
        # Execute scan
        result = scanner.scan_repository(
            repo_url=repo_url,
            scan_git_history=scan_git_history,
            output_format=output_format,
            save_output=save_output,
            output_dir=output_dir,
            timeout=timeout,
            github_token=github_token
        )
        
        logger.info(f"[gitleaks_scan_repository] Scan completed: success={result.get('success', False)}")
        return result
        
    except Exception as e:
        logger.error(f"[gitleaks_scan_repository] Error: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "tool": "gitleaks"
        }
```

### Phase 3: Special Cases Handling

#### Tools with Multiple Methods (ZAP)

```python
# mcpservers/recon/tools/zap_tool.py

def zap_baseline_scan(target_url: str, **kwargs) -> Dict[str, Any]:
    """ZAP baseline scan (passive scanning)."""
    scanner = ZAPScanner()
    return scanner.baseline_scan(target_url=target_url, **kwargs)

def zap_full_scan(target_url: str, **kwargs) -> Dict[str, Any]:
    """ZAP full scan (active scanning)."""
    scanner = ZAPScanner()
    return scanner.full_scan(target_url=target_url, **kwargs)

def zap_api_scan(target_url: str, **kwargs) -> Dict[str, Any]:
    """ZAP API scan (OpenAPI/Swagger)."""
    scanner = ZAPScanner()
    return scanner.api_scan(target_url=target_url, **kwargs)
```

#### Tools with Different Target Types (Trivy)

```python
# mcpservers/recon/tools/trivy_tool.py

def trivy_scan_container(image_name: str, **kwargs) -> Dict[str, Any]:
    """Scan Docker container image with Trivy."""
    scanner = TrivyScanner()
    return scanner.scan_container(image_name=image_name, **kwargs)

def trivy_scan_repository(repo_url: str, **kwargs) -> Dict[str, Any]:
    """Scan GitHub repository with Trivy."""
    scanner = TrivyScanner()
    return scanner.scan_repository(repo_url=repo_url, **kwargs)
```

## Implementation Steps

### Step 1: Create Wrapper Generator Script

**File**: `mcpservers/recon/tools/generate_appsec_wrappers.py`

This script will:
1. Parse each `*_scan.py` file using AST
2. Extract:
   - Scanner class name
   - `__init__` parameters
   - Main scan method(s) and their signatures
3. Generate wrapper Python files following the template

### Step 2: Generate All Wrappers

Run the generator to create all 24+ wrapper files in `mcpservers/recon/tools/`.

### Step 3: Test Integration

1. Start the recon MCP server
2. Verify all tools are discovered
3. Test a few tools to ensure they work correctly

### Step 4: Documentation

Update README.md with:
- List of all available tools
- Tool-specific usage examples
- Parameter documentation

## File Structure After Migration

```
mcpservers/recon/
├── recon_mcpserver.py              # Main server (unchanged)
├── tools/
│   ├── __init__.py
│   ├── example_python_tool.py      # Examples (keep)
│   ├── example_cli_tool.py         # Examples (keep)
│   ├── generate_appsec_wrappers.py # Generator script (new)
│   ├── bearer_tool.py              # Generated wrapper
│   ├── checkov_tool.py              # Generated wrapper
│   ├── dependency_check_tool.py    # Generated wrapper
│   ├── gitleaks_tool.py             # Generated wrapper
│   ├── gitguardian_tool.py          # Generated wrapper
│   ├── grype_tool.py                # Generated wrapper
│   ├── horusec_tool.py              # Generated wrapper
│   ├── kube_bench_tool.py           # Generated wrapper
│   ├── kube_hunter_tool.py          # Generated wrapper
│   ├── kubescape_tool.py            # Generated wrapper
│   ├── metasploit_tool.py            # Generated wrapper
│   ├── mobsf_tool.py                # Generated wrapper
│   ├── nikto_tool.py                # Generated wrapper
│   ├── openssf_scorecard_tool.py    # Generated wrapper
│   ├── retire_js_tool.py             # Generated wrapper
│   ├── semgrep_tool.py               # Generated wrapper
│   ├── sonarqube_tool.py             # Generated wrapper
│   ├── sqlmap_tool.py                # Generated wrapper
│   ├── syft_tool.py                  # Generated wrapper
│   ├── terrascan_tool.py             # Generated wrapper
│   ├── trivy_tool.py                 # Generated wrapper
│   ├── trufflehog_tool.py           # Generated wrapper
│   ├── w3af_tool.py                  # Generated wrapper
│   ├── wapiti_tool.py                # Generated wrapper
│   └── zap_tool.py                   # Generated wrapper (multiple methods)
```

## Advantages of This Approach

1. **Zero Code Changes**: Existing tool code remains untouched
2. **Automatic Discovery**: Plugin system automatically finds all wrappers
3. **Maintainability**: Tool updates automatically available (no wrapper changes needed)
4. **Consistency**: All tools follow same MCP interface pattern
5. **Extensibility**: Easy to add new tools by generating new wrappers
6. **Type Safety**: Wrappers preserve function signatures for FastMCP

## Path Resolution Strategy

Since tools are in a different workspace, we need to handle path resolution:

```python
# In each wrapper file
import sys
from pathlib import Path

# Calculate path to application_security/tools
# From: mcpservers/recon/tools/gitleaks_tool.py
# To:   hd-cyberdefense/cyberdefense/tasks/application_security/tools

current_file = Path(__file__).resolve()
# Navigate: recon/tools -> mcpservers/recon -> mcpservers-and-tools -> 
#           hd-cyberdefense/cyberdefense/tasks/application_security/tools

# Option 1: Relative path (if workspaces are siblings)
appsec_tools_path = current_file.parents[4] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"

# Option 2: Environment variable
appsec_tools_path = Path(os.environ.get("APPSEC_TOOLS_PATH", "/path/to/tasks/application_security/tools"))

# Option 3: Configuration file
# Store base path in recon_mcpserver config

if str(appsec_tools_path) not in sys.path:
    sys.path.insert(0, str(appsec_tools_path))
```

## Testing Strategy

1. **Unit Tests**: Test each wrapper independently
2. **Integration Tests**: Test MCP server discovers all tools
3. **Functional Tests**: Test a few tools end-to-end
4. **Regression Tests**: Ensure existing tool functionality unchanged

## Rollout Plan

1. **Week 1**: Create generator script and test with 2-3 tools
2. **Week 2**: Generate all wrappers and test integration
3. **Week 3**: Documentation and final testing
4. **Week 4**: Production deployment

## Risk Mitigation

1. **Path Issues**: Use environment variables or config for tool paths
2. **Import Errors**: Add try/except with helpful error messages
3. **Method Signature Changes**: Generator script can be re-run to update wrappers
4. **Performance**: Wrappers add minimal overhead (just import + call)

## Next Steps

1. ✅ Review and approve this plan
2. Create wrapper generator script
3. Generate wrappers for all 24 tools
4. Test integration
5. Update documentation
6. Deploy

