#!/bin/bash
# Build all Application Security MCP Servers

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Building Application Security MCP Servers..."
echo "=========================================="

# Build base server first
echo ""
echo "Building appsec_base..."
cd appsec_base
docker build -t appsec-base-mcp:latest .
cd ..

# Build specialized servers (build from parent directory for proper context)
SERVERS=(
    "appsec_sast"
    "appsec_dast"
    "appsec_secrets"
    "appsec_container"
    "appsec_iac"
    "appsec_sca"
    "appsec_k8s"
    "appsec_supply_chain"
    "appsec_mobile"
)

for server in "${SERVERS[@]}"; do
    if [ -d "$server" ]; then
        echo ""
        echo "Building $server..."
        # Build from parent directory to include appsec_base in context
        docker build -f "${server}/Dockerfile" -t "appsec-${server}-mcp:latest" .
        echo "✅ $server built successfully"
    else
        echo "⚠️  $server directory not found, skipping"
    fi
done

echo ""
echo "=========================================="
echo "All servers built successfully!"
echo ""
echo "Available images:"
docker images | grep "appsec-.*-mcp" || echo "No appsec images found"

