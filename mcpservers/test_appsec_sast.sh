#!/bin/bash
# Test appsec_sast MCP Server

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Testing appsec_sast MCP Server"
echo "=============================="

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed or not in PATH"
    exit 1
fi

# Check if image exists
if ! docker images | grep -q "appsec-sast-mcp"; then
    echo "Building appsec_sast image..."
    cd appsec_sast
    docker build -t appsec-sast-mcp:latest .
    cd ..
fi

# Resolve path to application_security tools
APPSEC_TOOLS_PATH=""
if [ -d "../../hd-cyberdefense/cyberdefense/tasks/application_security/tools" ]; then
    APPSEC_TOOLS_PATH="$(cd ../../hd-cyberdefense/cyberdefense/tasks/application_security/tools && pwd)"
elif [ -n "$APPSEC_TOOLS_PATH" ]; then
    APPSEC_TOOLS_PATH="$APPSEC_TOOLS_PATH"
else
    echo "⚠️  Could not find application_security tools path"
    echo "   Set APPSEC_TOOLS_PATH environment variable or ensure tools are in expected location"
    exit 1
fi

echo ""
echo "Application Security Tools Path: $APPSEC_TOOLS_PATH"
echo ""

# Test run
echo "Running appsec_sast MCP server..."
echo "Press Ctrl+C to stop"
echo ""

docker run -it --rm \
  -v "${APPSEC_TOOLS_PATH}:/app/application_security_tools:ro" \
  -e GITHUB_TOKEN="${GITHUB_TOKEN:-}" \
  -e GITHUB_DEFAULT_TOKEN="${GITHUB_DEFAULT_TOKEN:-}" \
  -e APPSEC_TOOLS_PATH="/app/application_security_tools" \
  appsec-sast-mcp:latest

