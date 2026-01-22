#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CIRCUITPY="/Volumes/CIRCUITPY"

if [[ ! -d "$CIRCUITPY" ]]; then
  echo "CIRCUITPY not found at $CIRCUITPY"
  exit 1
fi

# Sync entry file and libraries
# TODO: update this to take arbitrary sub-directories
rsync -av \
  --exclude ".git/" \
  --exclude "__pycache__/" \
  "$REPO_ROOT/memento/code.py" \
  "$REPO_ROOT/memento/lib/" \
  "$CIRCUITPY/"
