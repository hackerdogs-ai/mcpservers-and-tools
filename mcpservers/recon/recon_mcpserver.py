"""
Recon MCP Server - Generic Plugin-Based MCP Server

This MCP server provides a generic wrapper that dynamically discovers and exposes
all tools within the recon/tools directory as MCP tools. It supports both pure Python
tools and tools that call command-line applications.

Features:
- Automatic plugin discovery from recon/tools directory
- Support for Python scripts and command-line tool wrappers
- Standardized logging using hd_logging
- FastMCP-based implementation following Hackerdogs standards
"""

import sys
import importlib.util
import inspect
import subprocess
import json
from pathlib import Path
from typing import Any, Dict, Optional, Callable, List
from functools import wraps

try:
    from fastmcp import FastMCP
except ImportError:
    raise ImportError(
        "fastmcp is required for recon_mcpserver. "
        "Install with: pip install fastmcp"
    )

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

logger = setup_logger(__name__, log_file_path="logs/recon_mcpserver.log")

# Initialize FastMCP server
mcp = FastMCP(name='recon-mcpserver')


class PluginLoader:
    """Loads and manages plugin tools from the recon/tools directory."""
    
    def __init__(self, tools_dir: Path):
        """
        Initialize plugin loader.
        
        Args:
            tools_dir: Path to the directory containing plugin tools
        """
        self.tools_dir = Path(tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_plugins: Dict[str, Any] = {}
        logger.info(f"[PluginLoader] Initialized with tools directory: {self.tools_dir}")
    
    def discover_plugins(self) -> List[Path]:
        """
        Discover all Python plugin files in the tools directory.
        
        Returns:
            List of paths to Python plugin files
        """
        plugins = []
        if not self.tools_dir.exists():
            logger.warning(f"[PluginLoader] Tools directory does not exist: {self.tools_dir}")
            return plugins
        
        for file_path in self.tools_dir.glob("*.py"):
            # Skip __init__.py and files starting with _
            if file_path.name.startswith("_") or file_path.name == "__init__.py":
                continue
            plugins.append(file_path)
            logger.debug(f"[PluginLoader] Discovered plugin: {file_path.name}")
        
        logger.info(f"[PluginLoader] Discovered {len(plugins)} plugin(s)")
        return plugins
    
    def load_plugin(self, plugin_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load a plugin module and extract tool functions.
        
        Args:
            plugin_path: Path to the plugin Python file
            
        Returns:
            Dictionary mapping tool names to tool functions, or None if loading failed
        """
        try:
            module_name = plugin_path.stem
            
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, plugin_path)
            if spec is None or spec.loader is None:
                logger.error(f"[PluginLoader] Failed to create spec for {plugin_path}")
                return None
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # Discover tool functions
            tools = {}
            for name, obj in inspect.getmembers(module):
                # Look for functions that are marked as tools
                if inspect.isfunction(obj) and not name.startswith("_"):
                    # Check if function has tool metadata or looks like a tool
                    if self._is_tool_function(obj):
                        tools[name] = obj
                        logger.info(f"[PluginLoader] Found tool: {module_name}.{name}")
            
            if not tools:
                logger.warning(f"[PluginLoader] No tools found in {plugin_path.name}")
                return None
            
            self.loaded_plugins[module_name] = {
                'module': module,
                'tools': tools,
                'path': plugin_path
            }
            
            logger.info(f"[PluginLoader] Loaded {len(tools)} tool(s) from {plugin_path.name}")
            return tools
            
        except Exception as e:
            logger.error(f"[PluginLoader] Failed to load plugin {plugin_path}: {e}", exc_info=True)
            return None
    
    def _is_tool_function(self, func: Callable) -> bool:
        """
        Determine if a function should be exposed as an MCP tool.
        
        Args:
            func: Function to check
            
        Returns:
            True if function should be exposed as a tool
        """
        # Check for tool decorator or metadata
        if hasattr(func, '__tool__') or hasattr(func, '__mcp_tool__'):
            return True
        
        # Check docstring for tool indicators
        if func.__doc__:
            doc_lower = func.__doc__.lower()
            if any(keyword in doc_lower for keyword in ['tool', 'mcp', 'recon', 'function']):
                return True
        
        # Default: expose all non-private functions
        return True
    
    def load_all_plugins(self) -> Dict[str, Any]:
        """
        Load all discovered plugins.
        
        Returns:
            Dictionary mapping plugin names to their tool dictionaries
        """
        all_tools = {}
        plugins = self.discover_plugins()
        
        for plugin_path in plugins:
            tools = self.load_plugin(plugin_path)
            if tools:
                all_tools.update(tools)
        
        logger.info(f"[PluginLoader] Loaded {len(all_tools)} total tool(s) from {len(plugins)} plugin(s)")
        return all_tools


def create_mcp_tool_from_function(func: Callable, tool_name: str) -> Callable:
    """
    Create an MCP tool wrapper from a Python function.
    
    Args:
        func: The function to wrap
        tool_name: Name for the tool
        
    Returns:
        Wrapped function ready for MCP tool registration
    """
    # Preserve original function signature and metadata
    original_sig = inspect.signature(func)
    original_doc = func.__doc__ or f"Tool: {tool_name}"
    
    # Create wrapper that handles both sync and async functions
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                logger.debug(f"[{tool_name}] Executing with args={args}, kwargs={kwargs}")
                result = await func(*args, **kwargs)
                logger.info(f"[{tool_name}] Execution completed successfully")
                return result
            except Exception as e:
                logger.error(f"[{tool_name}] Execution failed: {e}", exc_info=True)
                return {
                    "status": "error",
                    "message": str(e),
                    "tool": tool_name
                }
        
        # Preserve signature and docstring
        async_wrapper.__signature__ = original_sig
        async_wrapper.__doc__ = original_doc
        async_wrapper.__name__ = tool_name
        
        return async_wrapper
    else:
        @wraps(func)
        async def sync_wrapper(*args, **kwargs):
            try:
                logger.debug(f"[{tool_name}] Executing with args={args}, kwargs={kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"[{tool_name}] Execution completed successfully")
                return result
            except Exception as e:
                logger.error(f"[{tool_name}] Execution failed: {e}", exc_info=True)
                return {
                    "status": "error",
                    "message": str(e),
                    "tool": tool_name
                }
        
        # Preserve signature and docstring
        sync_wrapper.__signature__ = original_sig
        sync_wrapper.__doc__ = original_doc
        sync_wrapper.__name__ = tool_name
        
        return sync_wrapper


def create_cli_tool_wrapper(tool_name: str, command: List[str], description: str = "") -> Callable:
    """
    Create an MCP tool wrapper for a command-line application.
    
    Args:
        tool_name: Name of the tool
        command: Base command to execute (e.g., ['nmap', '-sS'])
        description: Tool description
        
    Returns:
        Async function ready for MCP tool registration
    """
    @mcp.tool()
    async def cli_tool(*args: str, **kwargs: str) -> Dict[str, Any]:
        """
        Execute a command-line tool.
        
        Args:
            *args: Positional arguments to append to command
            **kwargs: Keyword arguments (converted to flags)
            
        Returns:
            Dictionary with execution results
        """
        try:
            # Build command
            cmd = command + list(args)
            
            # Add keyword arguments as flags
            for key, value in kwargs.items():
                if value is True or value == "":
                    cmd.append(f"--{key}")
                elif value is not None:
                    cmd.append(f"--{key}")
                    cmd.append(str(value))
            
            logger.info(f"[{tool_name}] Executing command: {' '.join(cmd)}")
            
            # Execute command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            return {
                "status": "success" if result.returncode == 0 else "error",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(cmd)
            }
            
        except subprocess.TimeoutExpired:
            logger.error(f"[{tool_name}] Command timed out")
            return {
                "status": "error",
                "message": "Command execution timed out",
                "tool": tool_name
            }
        except Exception as e:
            logger.error(f"[{tool_name}] Execution failed: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e),
                "tool": tool_name
            }
    
    # Set function name and docstring
    cli_tool.__name__ = tool_name
    cli_tool.__doc__ = description or f"Execute {tool_name} command-line tool"
    
    return cli_tool


def register_plugin_tools():
    """Discover and register all plugin tools with the MCP server."""
    # Determine tools directory
    server_dir = Path(__file__).parent
    tools_dir = server_dir / "tools"
    
    # Load plugins
    loader = PluginLoader(tools_dir)
    all_tools = loader.load_all_plugins()
    
    # Register each tool with FastMCP
    registered_count = 0
    for tool_name, tool_func in all_tools.items():
        try:
            # Create wrapper
            wrapped_func = create_mcp_tool_from_function(tool_func, tool_name)
            
            # Update the function name for better identification
            wrapped_func.__name__ = tool_name
            
            # Register with FastMCP using decorator pattern
            # Apply the @mcp.tool() decorator programmatically
            decorated_func = mcp.tool()(wrapped_func)
            
            # Store reference to prevent garbage collection
            setattr(mcp, f"_tool_{tool_name}", decorated_func)
            
            registered_count += 1
            logger.info(f"[recon_mcpserver] Registered tool: {tool_name}")
            
        except Exception as e:
            logger.error(f"[recon_mcpserver] Failed to register tool {tool_name}: {e}", exc_info=True)
    
    logger.info(f"[recon_mcpserver] Registered {registered_count} tool(s) with MCP server")


def main() -> None:
    """Run the Recon MCP server."""
    logger.info("Starting Recon MCP server...")
    
    # Register all plugin tools
    register_plugin_tools()
    
    logger.info("Recon MCP server ready. Starting stdio transport...")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()

