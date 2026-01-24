"""
TruffleHog Secret Scanner MCP Tool Wrapper
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
    from trufflehog.trufflehog_scan import TruffleHogScanner
except ImportError as e:
    TruffleHogScanner = None
    import sys
    sys.stderr.write(f"Warning: Could not import TruffleHogScanner: {e}\n")

from hd_logging import setup_logger
logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def trufflehog_scan_repository(
    repo_url: str,
    github_token: Optional[str] = None,
    verify_secrets: bool = True,
    scan_since_commit: Optional[str] = None,
    save_output: bool = True,
    output_dir: Optional[str] = None,
    scan_id: Optional[str] = None,
    timeout: int = 600
) -> Dict[str, Any]:
    """Scan a Git repository with TruffleHog for secrets."""
    if TruffleHogScanner is None:
        return {"success": False, "error": "TruffleHogScanner not available", "tool": "trufflehog"}
    try:
        logger.info(f"[trufflehog_scan_repository] Starting scan: {repo_url}")
        scanner = TruffleHogScanner()
        result = scanner.scan_repository(repo_url=repo_url, github_token=github_token, verify_secrets=verify_secrets, scan_since_commit=scan_since_commit, save_output=save_output, output_dir=output_dir, scan_id=scan_id, timeout=timeout)
        logger.info(f"[trufflehog_scan_repository] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[trufflehog_scan_repository] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "trufflehog"}

