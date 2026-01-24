"""
Base MCP Server for Application Security Tools
Provides shared functionality for all appsec MCP servers with container support
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from fastmcp import FastMCP

try:
    from hd_logging import setup_logger
except ImportError:
    import logging
    def setup_logger(name, log_file_path=None):
        logger = logging.getLogger(name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

logger = setup_logger(__name__, log_file_path="logs/appsec_base.log")


class AppSecBaseServer:
    """Base class for all application security MCP servers."""
    
    def __init__(self, server_name: str, tools_dir: Path):
        """
        Initialize base server.
        
        Args:
            server_name: Name of the MCP server
            tools_dir: Directory containing tool plugins
        """
        self.server_name = server_name
        self.mcp = FastMCP(name=server_name)
        self.tools_dir = Path(tools_dir)
        
        # Resolve application_security tools path
        self.appsec_tools_path = self._resolve_appsec_tools_path()
        
        # Add to Python path
        if self.appsec_tools_path and str(self.appsec_tools_path) not in sys.path:
            sys.path.insert(0, str(self.appsec_tools_path))
            logger.info(f"[{server_name}] Added appsec tools to path: {self.appsec_tools_path}")
        
        logger.info(f"[{server_name}] Initialized")
        logger.debug(f"[{server_name}] Python path: {sys.path}")
    
    def _resolve_appsec_tools_path(self) -> Optional[Path]:
        """
        Resolve path to application_security tools.
        
        Priority:
        1. APPSEC_TOOLS_PATH environment variable
        2. Docker volume mount at /app/application_security_tools
        3. Relative path from current file (for local development)
        
        Returns:
            Path to application_security tools or None if not found
        """
        # Check environment variable
        env_path = os.environ.get("APPSEC_TOOLS_PATH")
        if env_path:
            path = Path(env_path)
            if path.exists():
                logger.info(f"[{self.server_name}] Using APPSEC_TOOLS_PATH: {path}")
                return path
            else:
                logger.warning(f"[{self.server_name}] APPSEC_TOOLS_PATH set but path does not exist: {path}")
        
        # Check Docker volume mount
        docker_path = Path("/app/application_security_tools")
        if docker_path.exists():
            logger.info(f"[{self.server_name}] Using Docker volume: {docker_path}")
            return docker_path
        
        # Try relative path (for local development)
        # Navigate: mcpservers/appsec_base -> mcpservers -> hd-cyberdefense/cyberdefense/tasks/application_security/tools
        current_file = Path(__file__).resolve()
        relative_path = current_file.parents[2] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"
        if relative_path.exists():
            logger.info(f"[{self.server_name}] Using relative path: {relative_path}")
            return relative_path
        
        # Try alternative relative path (if mcpservers is in different location)
        alt_path = current_file.parents[3] / "hd-cyberdefense" / "cyberdefense" / "tasks" / "application_security" / "tools"
        if alt_path.exists():
            logger.info(f"[{self.server_name}] Using alternative relative path: {alt_path}")
            return alt_path
        
        logger.warning(f"[{self.server_name}] Could not resolve appsec tools path")
        logger.warning(f"[{self.server_name}] Tried: APPSEC_TOOLS_PATH={env_path}, /app/application_security_tools, {relative_path}, {alt_path}")
        return None
    
    def register_tools(self):
        """Register all tools from tools directory."""
        if not self.tools_dir.exists():
            logger.error(f"[{self.server_name}] Tools directory does not exist: {self.tools_dir}")
            return
        
        # Import plugin loader from recon server
        recon_path = Path(__file__).parent.parent / "recon"
        if str(recon_path) not in sys.path:
            sys.path.insert(0, str(recon_path))
        
        try:
            from recon_mcpserver import PluginLoader, create_mcp_tool_from_function
        except ImportError:
            logger.error(f"[{self.server_name}] Failed to import plugin loader from recon_mcpserver")
            return
        
        loader = PluginLoader(self.tools_dir)
        all_tools = loader.load_all_plugins()
        
        registered_count = 0
        for tool_name, tool_func in all_tools.items():
            try:
                wrapped_func = create_mcp_tool_from_function(tool_func, tool_name)
                wrapped_func.__name__ = tool_name
                decorated_func = self.mcp.tool()(wrapped_func)
                setattr(self.mcp, f"_tool_{tool_name}", decorated_func)
                registered_count += 1
                logger.info(f"[{self.server_name}] Registered tool: {tool_name}")
            except Exception as e:
                logger.error(f"[{self.server_name}] Failed to register {tool_name}: {e}", exc_info=True)
        
        logger.info(f"[{self.server_name}] Registered {registered_count} tool(s)")
    
    def run(self):
        """Run the MCP server."""
        self.register_tools()
        logger.info(f"[{self.server_name}] Starting stdio transport...")
        self.mcp.run(transport='stdio')

