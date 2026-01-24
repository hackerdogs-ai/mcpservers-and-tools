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
        path = Path(env_path)
        if path.exists():
            return path
    
    # Check Docker volume
    docker_path = Path("/app/application_security_tools")
    if docker_path.exists():
        return docker_path
    
    # Try relative path
    current_file = Path(__file__).resolve()
    # Navigate: mcpservers/appsec_sast/tools -> mcpservers -> hd-cyberdefense/cyberdefense/tasks/application_security/tools
    relative_path = current_file.parents[4] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"
    if relative_path.exists():
        return relative_path
    
    raise RuntimeError("Could not resolve application_security tools path")

appsec_tools_path = _get_appsec_tools_path()
if str(appsec_tools_path) not in sys.path:
    sys.path.insert(0, str(appsec_tools_path))

try:
    from semgrep.semgrep_scan import SemgrepScanner
except ImportError as e:
    SemgrepScanner = None
    import sys
    sys.stderr.write(f"Warning: Could not import SemgrepScanner: {e}\n")

from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def semgrep_scan_repository(
    repo_url: str,
    rule_set: str = "auto",
    severity_threshold: Optional[str] = None,
    output_format: str = "json",
    save_output: bool = True,
    output_dir: Optional[str] = None,
    timeout: int = 600,
    github_token: Optional[str] = None,
    scan_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Scan a GitHub repository with Semgrep for security vulnerabilities.
    
    Args:
        repo_url: GitHub repository URL (e.g., https://github.com/user/repo)
        rule_set: Semgrep rule set (auto, p/security-audit, p/owasp-top-10, p/secrets)
        severity_threshold: Filter by severity (ERROR, WARNING, INFO)
        output_format: Output format (json, sarif, text)
        save_output: Whether to save output to file (default: True)
        output_dir: Custom output directory (optional)
        timeout: Scan timeout in seconds (default: 600)
        github_token: GitHub Personal Access Token for private repos (optional)
        scan_id: Optional ULID for this scan (optional)
        
    Returns:
        Dictionary with scan results and metadata
    """
    if SemgrepScanner is None:
        return {
            "success": False,
            "error": "SemgrepScanner not available - check application_security tools path",
            "tool": "semgrep"
        }
    
    try:
        logger.info(f"[semgrep_scan_repository] Starting scan for: {repo_url}")
        
        # Initialize scanner
        scanner = SemgrepScanner(github_token=github_token)
        
        # Execute scan
        result = scanner.scan_repository(
            repo_url=repo_url,
            rule_set=rule_set,
            severity_threshold=severity_threshold,
            output_format=output_format,
            save_output=save_output,
            output_dir=output_dir,
            timeout=timeout,
            github_token=github_token,
            scan_id=scan_id
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

