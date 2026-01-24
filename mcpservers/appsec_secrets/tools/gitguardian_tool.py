"""
GitGuardian Secret Scanner MCP Tool Wrapper
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

def _get_appsec_tools_path():
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
    from gitguardian.gitguardian_scan import GitGuardianScanner
except ImportError as e:
    GitGuardianScanner = None
    import sys
    sys.stderr.write(f"Warning: Could not import GitGuardianScanner: {e}\n")

from hd_logging import setup_logger
logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def gitguardian_scan_repository(
    repo_url: str,
    github_token: Optional[str] = None,
    save_output: bool = True,
    output_dir: Optional[str] = None,
    timeout: int = 600,
    scan_mode: str = "path"
) -> Dict[str, Any]:
    """Scan a GitHub repository with GitGuardian for secrets."""
    if GitGuardianScanner is None:
        return {"success": False, "error": "GitGuardianScanner not available", "tool": "gitguardian"}
    try:
        logger.info(f"[gitguardian_scan_repository] Starting scan: {repo_url}")
        scanner = GitGuardianScanner()
        result = scanner.scan_repository(repo_url=repo_url, github_token=github_token, save_output=save_output, output_dir=output_dir, timeout=timeout, scan_mode=scan_mode)
        logger.info(f"[gitguardian_scan_repository] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[gitguardian_scan_repository] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "gitguardian"}

