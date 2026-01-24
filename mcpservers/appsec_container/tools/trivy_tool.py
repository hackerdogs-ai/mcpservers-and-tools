"""
Trivy Container Vulnerability Scanner MCP Tool Wrapper
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
    from trivy.trivy_scan import TrivyScanner
except ImportError as e:
    TrivyScanner = None
    import sys
    sys.stderr.write(f"Warning: Could not import TrivyScanner: {e}\n")

from hd_logging import setup_logger
logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def trivy_scan_container(
    image_name: str,
    output_format: str = "json",
    save_output: bool = True,
    output_dir: Optional[str] = None,
    timeout: int = 300
) -> Dict[str, Any]:
    """Scan a Docker container image with Trivy for vulnerabilities."""
    if TrivyScanner is None:
        return {"success": False, "error": "TrivyScanner not available", "tool": "trivy"}
    try:
        logger.info(f"[trivy_scan_container] Starting scan: {image_name}")
        scanner = TrivyScanner()
        result = scanner.scan_container(image_name=image_name, output_format=output_format, save_output=save_output, output_dir=output_dir)
        logger.info(f"[trivy_scan_container] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[trivy_scan_container] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "trivy"}


def trivy_scan_repository(
    repo_url: str,
    output_format: str = "json",
    save_output: bool = True,
    output_dir: Optional[str] = None,
    timeout: int = 300,
    github_token: Optional[str] = None
) -> Dict[str, Any]:
    """Scan a GitHub repository with Trivy for container vulnerabilities."""
    if TrivyScanner is None:
        return {"success": False, "error": "TrivyScanner not available", "tool": "trivy"}
    try:
        logger.info(f"[trivy_scan_repository] Starting scan: {repo_url}")
        scanner = TrivyScanner(github_token=github_token)
        result = scanner.scan_repository(repo_url=repo_url, output_format=output_format, save_output=save_output, output_dir=output_dir)
        logger.info(f"[trivy_scan_repository] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[trivy_scan_repository] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "trivy"}

