"""
DAST MCP Server - Dynamic Application Security Testing Tools

Provides MCP tools for:
- ZAP (baseline, full, API scans)
- Nikto
- SQLMap
- Wapiti
- Metasploit
- W3AF
"""

import sys
from pathlib import Path

# Add base server to path
base_path = Path(__file__).parent.parent / "appsec_base"
if str(base_path) not in sys.path:
    sys.path.insert(0, str(base_path))

# Import base server
try:
    from appsec_base_server import AppSecBaseServer
except ImportError:
    import importlib.util
    base_server_path = base_path / "appsec_base_server.py"
    if base_server_path.exists():
        spec = importlib.util.spec_from_file_location("appsec_base_server", base_server_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            AppSecBaseServer = module.AppSecBaseServer
    else:
        raise ImportError(f"Could not find appsec_base_server.py at {base_server_path}")

from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/appsec_dast_mcp.log")


def main():
    """Run DAST MCP server."""
    server_dir = Path(__file__).parent
    tools_dir = server_dir / "tools"
    
    logger.info("Starting DAST MCP Server...")
    logger.info(f"Tools directory: {tools_dir}")
    
    server = AppSecBaseServer("appsec-dast-mcp", tools_dir)
    server.run()


if __name__ == "__main__":
    main()

