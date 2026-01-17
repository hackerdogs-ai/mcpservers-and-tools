# Recon MCP Server

A generic, plugin-based MCP server for reconnaissance tools. This server automatically discovers and exposes all tools within the `recon/tools` directory as MCP tools, supporting both pure Python tools and command-line application wrappers.

## Features

- **Automatic Plugin Discovery**: Automatically discovers and loads all Python tools from the `recon/tools` directory
- **Plugin Model**: Simply copy tool files to `recon/tools/` and they'll be automatically exposed
- **Python & CLI Support**: Supports both pure Python tools and tools that wrap command-line applications
- **Standardized Logging**: Uses `hd_logging` package for consistent logging across all tools
- **FastMCP Based**: Built on FastMCP following Hackerdogs standards

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install directly
pip install fastmcp>=2.12.5 hd-logging>=1.0.0
```

## Usage

### Running the Server

```bash
python recon_mcpserver.py
```

The server runs in stdio mode and can be connected to via MCP clients.

### Creating Plugin Tools

#### Pure Python Tools

Create a Python file in `recon/tools/` directory:

```python
# recon/tools/my_tool.py
from typing import Dict, Any
from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")

def my_recon_tool(target: str) -> Dict[str, Any]:
    """
    My custom recon tool.
    
    Args:
        target: Target to recon
        
    Returns:
        Dictionary with results
    """
    logger.info(f"Processing target: {target}")
    return {
        "status": "success",
        "target": target,
        "result": "Tool executed successfully"
    }
```

The function will be automatically discovered and exposed as an MCP tool named `my_recon_tool`.

#### Command-Line Tool Wrappers

Create a tool that wraps a command-line application:

```python
# recon/tools/nmap_tool.py
import subprocess
from typing import Dict, Any
from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")

def nmap_scan(target: str, ports: str = "1-1000") -> Dict[str, Any]:
    """
    Perform Nmap scan on target.
    
    Args:
        target: Target IP or hostname
        ports: Port range to scan (default: 1-1000)
        
    Returns:
        Dictionary with scan results
    """
    logger.info(f"[nmap_scan] Scanning {target} on ports {ports}")
    
    try:
        cmd = ["nmap", "-p", ports, target]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return {
            "status": "success" if result.returncode == 0 else "error",
            "target": target,
            "ports": ports,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        logger.error(f"[nmap_scan] Error: {e}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }
```

#### Async Tools

The server also supports async functions:

```python
# recon/tools/async_tool.py
import asyncio
from typing import Dict, Any

async def async_recon_tool(query: str) -> Dict[str, Any]:
    """
    Async recon tool example.
    
    Args:
        query: Query string
        
    Returns:
        Dictionary with results
    """
    await asyncio.sleep(0.1)  # Simulate async operation
    return {
        "status": "success",
        "query": query
    }
```

## Plugin Discovery Rules

The server automatically discovers tools based on these rules:

1. **File Location**: All `.py` files in `recon/tools/` directory
2. **File Naming**: Files starting with `_` or named `__init__.py` are ignored
3. **Function Discovery**: All non-private functions (not starting with `_`) are exposed as tools
4. **Tool Metadata**: Functions with docstrings are preferred, but any function will be exposed

## Logging

All tools should use `hd_logging` for consistent logging:

```python
from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")
```

Logs are written to:
- Server logs: `logs/recon_mcpserver.log`
- Tool logs: `logs/recon_tools.log`

## Example Tools

The `recon/tools/` directory includes example tools:

- `example_python_tool.py`: Demonstrates pure Python tools (sync and async)
- `example_cli_tool.py`: Demonstrates command-line tool wrappers (ping, nslookup)

## MCP Server Configuration

To use this server with MCP clients, configure it as a stdio server:

```json
{
  "mcp_servers": {
    "recon_mcp": {
      "type": "stdio",
      "command": "python3",
      "args": ["/path/to/recon_mcpserver.py"],
      "env": {
        "PYTHONPATH": "/path/to/mcpservers-and-tools"
      }
    }
  }
}
```

## Architecture

```
recon/
├── recon_mcpserver.py      # Main MCP server
├── requirements.txt        # Dependencies
├── README.md              # This file
└── tools/                 # Plugin directory
    ├── __init__.py
    ├── example_python_tool.py
    └── example_cli_tool.py
```

## Standards Compliance

This server follows Hackerdogs standards:

- ✅ Uses `hd_logging` for logging
- ✅ Follows FastMCP patterns from `modules/tools` directory
- ✅ Supports plugin-based architecture
- ✅ Comprehensive error handling
- ✅ Standardized tool interfaces

## Troubleshooting

### Tools Not Discovered

- Ensure tool files are in `recon/tools/` directory
- Check that files don't start with `_`
- Verify functions are not private (don't start with `_`)
- Check server logs for loading errors

### Import Errors

- Ensure all dependencies are installed
- Check `PYTHONPATH` includes the server directory
- Verify `hd_logging` is installed

### Command-Line Tools Not Found

- Ensure command-line tools are installed and in PATH
- Check tool-specific error messages in logs
- Verify command syntax for your operating system

## Contributing

To add new tools:

1. Create a Python file in `recon/tools/`
2. Define functions following the examples
3. Use `hd_logging` for logging
4. Test the tool by running the server
5. The tool will be automatically discovered and exposed

