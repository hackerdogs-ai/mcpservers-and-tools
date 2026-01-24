"""
Metasploit Penetration Testing Framework MCP Tool Wrapper
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

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
    from metasploit.metasploit_scan import MetasploitScanner
except ImportError as e:
    MetasploitScanner = None
    import sys
    sys.stderr.write(f"Warning: Could not import MetasploitScanner: {e}\n")

from hd_logging import setup_logger
logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def metasploit_scan_web_target(
    target_url: str,
    save_output: bool = True,
    output_dir: Optional[str] = None,
    timeout: int = 120,
    scan_modules: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Scan a web target with Metasploit for vulnerabilities (SAFE MODE ONLY)."""
    if MetasploitScanner is None:
        return {"success": False, "error": "MetasploitScanner not available", "tool": "metasploit"}
    try:
        logger.info(f"[metasploit_scan_web_target] Starting scan: {target_url}")
        scanner = MetasploitScanner()
        result = scanner.scan_web_target(target_url=target_url, save_output=save_output, output_dir=output_dir, timeout=timeout, scan_modules=scan_modules)
        logger.info(f"[metasploit_scan_web_target] Scan completed: success={result.get('success', False)}")
        return result
    except Exception as e:
        logger.error(f"[metasploit_scan_web_target] Error: {e}", exc_info=True)
        return {"success": False, "error": str(e), "tool": "metasploit"}

