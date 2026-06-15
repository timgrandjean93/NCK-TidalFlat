#!/usr/bin/env bash
# Live preview (jupyter book start) WITH notebook execution.
#
# Usage (from repo root):
#   ./scripts/start-site-execute.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# shellcheck source=_jupyter-env.sh
source "$ROOT/scripts/_jupyter-env.sh"

if [[ ! -d "$ROOT/.venv" ]]; then
  echo "Missing .venv — run:  uv sync --frozen"
  exit 1
fi

echo "Registering nck Jupyter kernel ..."
(cd "$ROOT" && uv run python -m ipykernel install --user --name nck --display-name "Python 3 (NCK)")

echo "Starting Jupyter server from .venv on port ${NCK_JUPYTER_PORT} ..."
print_jupyter_connection

(cd "$ROOT" && uv run python -m jupyter server \
  --IdentityProvider.token="$NCK_JUPYTER_TOKEN" \
  --ServerApp.port="$NCK_JUPYTER_PORT" \
  --ServerApp.allow_origin='http://localhost:3000' \
  --ServerApp.disable_check_xsrf=True) &
JPID=$!
trap "kill $JPID 2>/dev/null" EXIT INT TERM

sleep 3

export JUPYTER_BASE_URL="http://127.0.0.1:${NCK_JUPYTER_PORT}"
export JUPYTER_TOKEN="$NCK_JUPYTER_TOKEN"

echo "Starting site preview with --execute ..."
cd "$ROOT"

if command -v jupyter-book >/dev/null 2>&1; then
  jupyter book start --execute
elif [[ -x "$ROOT/.venv/bin/jupyter-book" ]]; then
  "$ROOT/.venv/bin/jupyter" book start --execute
else
  echo "jupyter-book not found. Install:  uv tool install jupyter-book"
  exit 1
fi
