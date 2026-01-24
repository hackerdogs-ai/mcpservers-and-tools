"""
Bearer SAST Scanner MCP Tool Wrapper
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

# Resolve application_security tools path
def _get_appsec_tools_path():
    """Get path to application_security tools."""
    env_path = os.environ.get("APPSEC_TOOLS_PATH")
    if env_path:
        path = Path(env_path)
        if path.exists():
            return path
    
    docker_path = Path("/app/application_security_tools")
    if docker_path.exists():
        return docker_path
    
    current_file = Path(__file__).resolve()
    relative_path = current_file.parents[4] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"
    if relative_path.exists():
        return relative_path
    
    raise RuntimeError("Could not resolve application_security tools path")

appsec_tools_path = _get_appsec_tools_path()
if str(appsec_tools_path) not in sys.path:
    sys.path.insert(0, str(appsec_tools_path))

try:
    from bearer.bearer_scan import BearerScanner
except ImportError as e:
    BearerScanner = None
    import sys
    sys.stderr.write(f"Warning: Could not import BearerScanner: {e}\n")

from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def bearer_scan_repository(
    repo_url: str,
    save_output: bool = True,
    output_dir: Optional[str] = None,
    scan_options: Optional[List[str]] = None,
    timeout: int = 600,
    github_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Scan a GitHub repository with Bearer for data flow analysis and sensitive data detection.
    
    Args:
        repo_url: GitHub repository URL
        save_output: Whether to save output to file (default: True)
        output_dir: Custom output directory (optional)
        scan_options: Additional Bearer CLI options (optional)
        timeout: Scan timeout in seconds (default: 600)
        github_token: GitHub Personal Access Token for private repos (optional)
        
    Returns:
        Dictionary with scan results and metadata
    """
    if BearerScanner is None:
        return {
            "success": False,
            "error": "BearerScanner not available - check application_security tools path",
            "tool": "bearer"
        }
    
    try:
        logger.info(f"[bearer_scan_repository] Starting scan for: {repo_url}")
        
        # Initialize scanner
        scanner = BearerScanner(github_token=github_token)
        
        # Execute scan
        result = scanner.scan_repository(
            repo_url=repo_url,
            save_output=save_output,
            output_dir=output_dir,
            scan_options=scan_options,
            timeout=timeout
        )
        
        logger.info(f"[bearer_scan_repository] Scan completed: success={result.get('success', False)}")
        return result
        
    except Exception as e:
        logger.error(f"[bearer_scan_repository] Error: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e),
            "tool": "bearer"
        }

