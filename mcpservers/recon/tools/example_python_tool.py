"""
Example Python Tool Plugin

This is an example plugin that demonstrates how to create a pure Python tool
for the recon MCP server. Simply define functions and they will be automatically
discovered and exposed as MCP tools.
"""

from typing import Dict, Any
from hd_logging import setup_logger

logger = setup_logger(__name__, log_file_path="logs/recon_tools.log")


def example_ping_check(host: str, count: int = 4) -> Dict[str, Any]:
    """
    Example tool: Check if a host is reachable via ping.
    
    This is a pure Python example. For actual ping, you would typically
    use a command-line tool wrapper instead.
    
    Args:
        host: Hostname or IP address to check
        count: Number of ping attempts (default: 4)
        
    Returns:
        Dictionary with ping results
    """
    logger.info(f"[example_ping_check] Checking host: {host} with count={count}")
    
    # This is just an example - in practice you'd use subprocess to call ping
    # See example_cli_tool.py for command-line tool examples
    return {
        "status": "success",
        "host": host,
        "message": "This is an example tool. Use example_cli_tool.py for actual ping.",
        "count": count
    }


async def example_async_tool(query: str) -> Dict[str, Any]:
    """
    Example async tool: Demonstrates async function support.
    
    Args:
        query: Query string
        
    Returns:
        Dictionary with results
    """
    logger.info(f"[example_async_tool] Processing query: {query}")
    
    # Simulate async operation
    import asyncio
    await asyncio.sleep(0.1)
    
    return {
        "status": "success",
        "query": query,
        "result": f"Processed: {query}"
    }

