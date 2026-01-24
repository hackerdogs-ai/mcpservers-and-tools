"""
Wapiti Web Vulnerability Scanner MCP Tool Wrapper
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
    from wapiti.wapiti_scan import WapitiScanner
except ImportError as e:
    WapitiScanner = None
    import sys
    sys.stderr.write(f"Warning: Could not import WapitiScanner: {e}\n")

from hd_logging import setup_logger
logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def wapiti_scan_url(
    target_url: str,
    save_output: bool = True,
    output_dir: Optional[str] = None,
    timeout: int = 600
) -> Dict[str, Any]:
    """Scan a URL with Wapiti for web application vulnerabilities."""
    if WapitiScanner is None:
        return {"success": False, "error": "WapitiScanner not available", "tool": "wapiti"}
    try:
        logger.info(f"[wapiti_scan_url] Starting scan: {target_url}")
        scanner = WapitiScanner()
        result = scanner.scan_url(target_url=target_url, save_output=save_output, output_dir=output_dir, timeout=timeout)
        logger.info(f"[wapiti_scan_url] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[wapiti_scan_url] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "wapiti"}

