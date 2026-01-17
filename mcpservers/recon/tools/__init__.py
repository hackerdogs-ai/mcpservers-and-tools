"""
Recon Tools Plugin Directory

This directory contains plugin tools that are automatically discovered and exposed
by the recon_mcpserver. Any Python script placed in this directory will be scanned
for tool functions and automatically registered as MCP tools.

Plugin Requirements:
- Python files (not starting with _)
- Functions that should be exposed as tools
- Functions can be sync or async
- Functions can call command-line applications via subprocess
"""

