# Application Security Tools Migration Checklist

## Quick Reference: Tool-by-Tool Migration Details

This document provides a detailed checklist for migrating each of the 24 application security tools to the recon MCP server framework.

## Migration Pattern Summary

**Standard Pattern:**
1. Import Scanner class from existing tool
2. Create wrapper function with same signature as scan method
3. Initialize scanner with defaults
4. Call scan method
5. Return results

**No code changes needed to existing tools!**

---

## Tool Migration Details

### 1. Bearer (SAST - Data Flow Analysis)

**File**: `bearer/bearer_scan.py`  
**Class**: `BearerScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, scan_options=None, timeout=600)`  
**Parameters**: 
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[Path] = None`
- `scan_options: Optional[List[str]] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None` (via __init__)

**Wrapper Function**: `bearer_scan_repository()`

**Status**: ⬜ Not Started

---

### 2. Checkov (IaC Security)

**File**: `checkov/checkov_scan.py`  
**Class**: `CheckovScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None`

**Wrapper Function**: `checkov_scan_repository()`

**Status**: ⬜ Not Started

---

### 3. Dependency-Check (SCA)

**File**: `dependency_check/dependency_check_scan.py`  
**Class**: `DependencyCheckScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None`

**Wrapper Function**: `dependency_check_scan_repository()`

**Status**: ⬜ Not Started

---

### 4. Gitleaks (Secret Scanning)

**File**: `gitleaks/gitleaks_scan.py`  
**Class**: `GitleaksScanner`  
**Method**: `scan_repository(repo_url, scan_git_history=False, output_format="json", save_output=True, output_dir=None, timeout=300, github_token=None)`  
**Parameters**:
- `repo_url: str` (required)
- `scan_git_history: bool = False`
- `output_format: str = "json"`
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 300`
- `github_token: Optional[str] = None`

**Wrapper Function**: `gitleaks_scan_repository()`

**Status**: ⬜ Not Started

---

### 5. GitGuardian (Secret Scanning)

**File**: `gitguardian/gitguardian_scan.py`  
**Class**: `GitGuardianScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=300)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 300`
- `github_token: Optional[str] = None`

**Wrapper Function**: `gitguardian_scan_repository()`

**Status**: ⬜ Not Started

---

### 6. Grype (Container Security)

**File**: `grype/grype_scan.py`  
**Class**: `GrypeScanner`  
**Method**: `scan_container(image_name, save_output=True, output_dir=None, timeout=300)`  
**Parameters**:
- `image_name: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 300`

**Wrapper Function**: `grype_scan_container()`

**Status**: ⬜ Not Started

---

### 7. Horusec (SAST)

**File**: `horusec/horusec_scan.py`  
**Class**: `HorusecScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None`

**Wrapper Function**: `horusec_scan_repository()`

**Status**: ⬜ Not Started

---

### 8. Kube-Bench (Kubernetes Security)

**File**: `kube_bench/kube_bench_scan.py`  
**Class**: `KubeBenchScanner`  
**Method**: `scan_container(image_name, save_output=True, output_dir=None, timeout=300)`  
**Parameters**:
- `image_name: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 300`

**Wrapper Function**: `kube_bench_scan_container()`

**Status**: ⬜ Not Started

---

### 9. Kube-Hunter (Kubernetes Security)

**File**: `kube_hunter/kube_hunter_scan.py`  
**Class**: `KubeHunterScanner`  
**Method**: `scan_url(target_url, save_output=True, output_dir=None, timeout=300)`  
**Parameters**:
- `target_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 300`

**Wrapper Function**: `kube_hunter_scan_url()`

**Status**: ⬜ Not Started

---

### 10. Kubescape (Kubernetes Security)

**File**: `kubescape/kubescape_scan.py`  
**Class**: `KubescapeScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None`

**Wrapper Function**: `kubescape_scan_repository()`

**Status**: ⬜ Not Started

---

### 11. Metasploit (DAST - Penetration Testing)

**File**: `metasploit/metasploit_scan.py`  
**Class**: `MetasploitScanner`  
**Method**: `scan_url(target_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `target_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`

**Wrapper Function**: `metasploit_scan_url()`

**Status**: ⬜ Not Started

---

### 12. MobSF (Mobile Security)

**File**: `mobsf/mobsf_scan.py`  
**Class**: `MobSFScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=1800)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 1800`
- `github_token: Optional[str] = None`

**Wrapper Function**: `mobsf_scan_repository()`

**Status**: ⬜ Not Started

---

### 13. Nikto (DAST - Web Server Scanner)

**File**: `nikto/nikto_scan.py`  
**Class**: `NiktoScanner`  
**Method**: `scan_url(target_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `target_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`

**Wrapper Function**: `nikto_scan_url()`

**Status**: ⬜ Not Started

---

### 14. OpenSSF Scorecard (Supply Chain Security)

**File**: `openssf_scorecard/scorecard_scan.py`  
**Class**: `ScorecardScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None`

**Wrapper Function**: `openssf_scorecard_scan_repository()`

**Status**: ⬜ Not Started

---

### 15. Retire.js (SCA - JavaScript)

**File**: `retire_js/retire_js_scan.py`  
**Class**: `RetireJSScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=300)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 300`
- `github_token: Optional[str] = None`

**Wrapper Function**: `retire_js_scan_repository()`

**Status**: ⬜ Not Started

---

### 16. Semgrep (SAST)

**File**: `semgrep/semgrep_scan.py`  
**Class**: `SemgrepScanner`  
**Method**: `scan_repository(repo_url, output_format="json", save_output=True, output_dir=None, timeout=600, github_token=None)`  
**Parameters**:
- `repo_url: str` (required)
- `output_format: str = "json"`
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None`

**Wrapper Function**: `semgrep_scan_repository()`

**Status**: ⬜ Not Started

---

### 17. SonarQube (SAST)

**File**: `sonarqube/sonarqube_scan.py`  
**Class**: `SonarQubeScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None`

**Wrapper Function**: `sonarqube_scan_repository()`

**Status**: ⬜ Not Started

---

### 18. SQLMap (DAST - SQL Injection)

**File**: `sqlmap/sqlmap_scan.py`  
**Class**: `SQLMapScanner`  
**Method**: `scan_url(target_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `target_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`

**Wrapper Function**: `sqlmap_scan_url()`

**Status**: ⬜ Not Started

---

### 19. Syft (SCA - SBOM Generation)

**File**: `syft/syft_scan.py`  
**Class**: `SyftScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=300)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 300`
- `github_token: Optional[str] = None`

**Wrapper Function**: `syft_scan_repository()`

**Status**: ⬜ Not Started

---

### 20. Terrascan (IaC Security)

**File**: `terrascan/terrascan_scan.py`  
**Class**: `TerrascanScanner`  
**Method**: `scan_repository(repo_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `repo_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`
- `github_token: Optional[str] = None`

**Wrapper Function**: `terrascan_scan_repository()`

**Status**: ⬜ Not Started

---

### 21. Trivy (Container Security)

**File**: `trivy/trivy_scan.py`  
**Class**: `TrivyScanner`  
**Methods**: 
- `scan_container(image_name, save_output=True, output_dir=None, timeout=300)`
- `scan_repository(repo_url, save_output=True, output_dir=None, timeout=300)`

**Wrapper Functions**: 
- `trivy_scan_container()`
- `trivy_scan_repository()`

**Status**: ⬜ Not Started

---

### 22. TruffleHog (Secret Scanning)

**File**: `trufflehog/trufflehog_scan.py`  
**Class**: `TruffleHogScanner`  
**Method**: `scan_repository(repo_url, github_token=None, save_output=True, output_dir=None, timeout=300)`  
**Parameters**:
- `repo_url: str` (required)
- `github_token: Optional[str] = None`
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 300`

**Wrapper Function**: `trufflehog_scan_repository()`

**Status**: ⬜ Not Started

---

### 23. W3AF (DAST - Web Application Audit)

**File**: `w3af/w3af_scan.py`  
**Class**: `W3AFScanner`  
**Method**: `scan_url(target_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `target_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`

**Wrapper Function**: `w3af_scan_url()`

**Status**: ⬜ Not Started

---

### 24. Wapiti (DAST - Web Vulnerability Scanner)

**File**: `wapiti/wapiti_scan.py`  
**Class**: `WapitiScanner`  
**Method**: `scan_url(target_url, save_output=True, output_dir=None, timeout=600)`  
**Parameters**:
- `target_url: str` (required)
- `save_output: bool = True`
- `output_dir: Optional[str] = None`
- `timeout: int = 600`

**Wrapper Function**: `wapiti_scan_url()`

**Status**: ⬜ Not Started

---

### 25. ZAP (DAST - OWASP ZAP) ⚠️ SPECIAL CASE

**File**: `zap/zap_scan.py`  
**Class**: `ZAPScanner`  
**Methods**: 
- `baseline_scan(target_url, save_output=True, output_dir=None, scan_id=None, timeout=600)`
- `full_scan(target_url, save_output=True, output_dir=None, scan_id=None, timeout=1800)`
- `api_scan(target_url, save_output=True, output_dir=None, scan_id=None, timeout=600)`

**Wrapper Functions**: 
- `zap_baseline_scan()`
- `zap_full_scan()`
- `zap_api_scan()`

**Status**: ⬜ Not Started

---

## Migration Statistics

- **Total Tools**: 25 (24 + ZAP with 3 methods)
- **Tools with `scan_repository()`**: 18
- **Tools with `scan_url()`**: 5
- **Tools with `scan_container()`**: 2
- **Tools with multiple methods**: 2 (Trivy, ZAP)

## Implementation Priority

### Phase 1: High-Value Tools (Week 1)
1. ✅ Gitleaks (Secret Scanning - Most Used)
2. ✅ Semgrep (SAST - Most Popular)
3. ✅ Trivy (Container Security - Critical)
4. ✅ ZAP (DAST - Industry Standard)

### Phase 2: Core Tools (Week 2)
5. ✅ Checkov (IaC - Critical)
6. ✅ Grype (Container Security)
7. ✅ TruffleHog (Secret Scanning)
8. ✅ Nikto (DAST)

### Phase 3: Remaining Tools (Week 3)
9-25. All remaining tools

## Wrapper Template

```python
# mcpservers/recon/tools/{tool_name}_tool.py
"""
{Tool Name} MCP Tool Wrapper
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add application_security tools to path
appsec_tools_path = Path(__file__).resolve().parents[4] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"
if str(appsec_tools_path) not in sys.path:
    sys.path.insert(0, str(appsec_tools_path))

from {tool_name}.{tool_name}_scan import {ToolName}Scanner
from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def {tool_name}_{method_name}(
    {parameters}
) -> Dict[str, Any]:
    """
    {Tool description}.
    
    Args:
        {parameter_docs}
        
    Returns:
        Dictionary with scan results and metadata
    """
    try:
        logger.info(f"[{tool_name}_{method_name}] Starting scan")
        
        # Initialize scanner
        scanner = {ToolName}Scanner()
        
        # Execute scan
        result = scanner.{method_name}(
            {parameter_calls}
        )
        
        logger.info(f"[{tool_name}_{method_name}] Scan completed: success={result.get('success', False)}")
        return result
        
    except Exception as e:
        logger.error(f"[{tool_name}_{method_name}] Error: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "tool": "{tool_name}"
        }
```

## Next Steps

1. ✅ Review migration plan
2. ⬜ Create wrapper generator script
3. ⬜ Generate wrappers for Phase 1 tools
4. ⬜ Test integration
5. ⬜ Generate remaining wrappers
6. ⬜ Final testing and documentation

