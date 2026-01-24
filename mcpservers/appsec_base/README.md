# Application Security Base MCP Server

Base server class for all application security MCP servers. Provides shared functionality including:
- Plugin loading and registration
- Path resolution for application_security tools
- Container support (Docker and uvx)
- Logging setup

## Usage

This is a base class - use specialized servers like `appsec_sast_mcp` instead.

