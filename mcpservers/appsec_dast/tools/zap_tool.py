"""
ZAP DAST Scanner MCP Tool Wrapper
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
    from zap.zap_scan import ZAPScanner
except ImportError as e:
    ZAPScanner = None
    import sys
    sys.stderr.write(f"Warning: Could not import ZAPScanner: {e}\n")

from hd_logging import setup_logger
logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def zap_baseline_scan(
    target_url: str,
    save_output: bool = True,
    output_dir: Optional[str] = None,
    scan_id: Optional[str] = None,
    timeout: int = 600
) -> Dict[str, Any]:
    """ZAP baseline scan (passive scanning)."""
    if ZAPScanner is None:
        return {"success": False, "error": "ZAPScanner not available", "tool": "zap"}
    try:
        logger.info(f"[zap_baseline_scan] Starting scan: {target_url}")
        scanner = ZAPScanner()
        result = scanner.baseline_scan(target_url=target_url, save_output=save_output, output_dir=output_dir, scan_id=scan_id, timeout=timeout)
        logger.info(f"[zap_baseline_scan] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[zap_baseline_scan] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "zap"}


def zap_full_scan(
    target_url: str,
    save_output: bool = True,
    output_dir: Optional[str] = None,
    scan_id: Optional[str] = None,
    timeout: int = 1800
) -> Dict[str, Any]:
    """ZAP full scan (active scanning)."""
    if ZAPScanner is None:
        return {"success": False, "error": "ZAPScanner not available", "tool": "zap"}
    try:
        logger.info(f"[zap_full_scan] Starting scan: {target_url}")
        scanner = ZAPScanner()
        result = scanner.full_scan(target_url=target_url, save_output=save_output, output_dir=output_dir, scan_id=scan_id, timeout=timeout)
        logger.info(f"[zap_full_scan] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[zap_full_scan] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "zap"}


def zap_api_scan(
    target_url: str,
    save_output: bool = True,
    output_dir: Optional[str] = None,
    scan_id: Optional[str] = None,
    timeout: int = 600
) -> Dict[str, Any]:
    """ZAP API scan (OpenAPI/Swagger)."""
    if ZAPScanner is None:
        return {"success": False, "error": "ZAPScanner not available", "tool": "zap"}
    try:
        logger.info(f"[zap_api_scan] Starting scan: {target_url}")
        scanner = ZAPScanner()
        # Check if api_scan method exists
        if hasattr(scanner, 'api_scan'):
            result = scanner.api_scan(target_url=target_url, save_output=save_output, output_dir=output_dir, scan_id=scan_id, timeout=timeout)
        else:
            result = {"success": False, "error": "api_scan method not available in ZAPScanner", "tool": "zap"}
        logger.info(f"[zap_api_scan] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[zap_api_scan] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "zap"}

