#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

python -m venv .venv
if [ -f .venv/bin/python ]; then PY=.venv/bin/python; else PY=.venv/Scripts/python; fi
$PY -m pip install -q -r requirements.txt

mkdir -p data
if [ ! -f data/activity_net.json ]; then
  $PY src/download_data.py || echo "Download failed; the app will use data/sample.json instead."
fi
echo "Setup complete. Now run: bash run.sh"