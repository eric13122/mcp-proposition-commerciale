#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required. Install it from https://python.org" >&2
    exit 1
fi

# Install dependencies if needed (first run)
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "First run — installing dependencies..." >&2
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install -q -r "$SCRIPT_DIR/requirements.txt"
fi

# Run the server
exec "$VENV_DIR/bin/python" "$SCRIPT_DIR/server.py" "$@"
