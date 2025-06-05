#!/bin/bash

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <YANG_FILE>"
  exit 1
fi

YANG_FILE="$1"
MODULE_NAME=$(basename "$YANG_FILE" .yang)
PYBIND_OUTPUT="${MODULE_NAME}_bindings.py"
MCP_OUTPUT="mcp_${MODULE_NAME}_server.py"

echo "[INFO] Generating pyangbind Python class..."
PYTHONWARNINGS="ignore" pyang \
  --plugindir "$(python3 -c "import pyangbind; print(pyangbind.__path__[0] + '/plugin')")" \
  -f pybind -o "$PYBIND_OUTPUT" "$YANG_FILE"

echo "[INFO] Generating MCP server stub..."
python3 generate_mcp_server_stub.py --module "${MODULE_NAME}_bindings" --output "$MCP_OUTPUT"

echo "[✅ DONE] Generated:"
echo " - Python binding: $PYBIND_OUTPUT"
echo " - MCP server:     $MCP_OUTPUT"
