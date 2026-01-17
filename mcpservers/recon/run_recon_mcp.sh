#!/bin/bash
# Run Recon MCP Server
# This script runs the recon MCP server with proper Python path setup

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set Python path to include the mcpservers directory
export PYTHONPATH="${SCRIPT_DIR}/..:${PYTHONPATH}"

# Run the server
python3 "${SCRIPT_DIR}/recon_mcpserver.py"

