#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if [ -f .venv/bin/python ]; then PY=.venv/bin/python; else PY=.venv/Scripts/python; fi
echo "Open http://localhost:${PORT:-5000}"
$PY src/app.py