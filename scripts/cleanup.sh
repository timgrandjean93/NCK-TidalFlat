#!/usr/bin/env bash
# Remove local tutorial artefacts (keeps source notebooks and tide_models/).
#
# Usage (from repo root):
#   ./scripts/cleanup.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "NCK-TidalFlat cleanup — repo: $ROOT"
echo

# Kernel must be removed while .venv still exists (if possible).
if [[ -d .venv ]]; then
  echo "Removing Jupyter kernel 'nck' ..."
  uv run jupyter kernelspec uninstall -y nck 2>/dev/null || true
else
  echo "Removing Jupyter kernel 'nck' (no .venv — trying system jupyter) ..."
  jupyter kernelspec uninstall -y nck 2>/dev/null || true
fi

if [[ -d .venv ]]; then
  echo "Removing .venv/ ..."
  rm -rf .venv
fi

if [[ -d cache ]]; then
  echo "Removing cache/ ..."
  rm -rf cache
fi

echo "Removing notebook outputs (*.png, *.nc, *.tif in repo root) ..."
rm -f ./*.png ./*.nc ./*.tif 2>/dev/null || true

if [[ -d _build ]]; then
  echo "Removing _build/ ..."
  rm -rf _build
fi

if [[ -d .ipynb_checkpoints ]]; then
  echo "Removing .ipynb_checkpoints/ ..."
  rm -rf .ipynb_checkpoints
fi

echo
echo "Done."
echo "  Kept: notebooks, tide_models/, git history"
echo "  Optional: rm -rf tide_models/   — remove FES2022 files"
echo "  Optional: cd .. && rm -rf $(basename "$ROOT")   — remove entire repo"
