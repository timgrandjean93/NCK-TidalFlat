#!/usr/bin/env bash
# Install the locked tutorial environment with platform-safe compiler settings.
#
# Usage (from repo root):
#   ./scripts/sync-env.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ "$(uname -s)" == "Darwin" ]]; then
  # Anaconda/conda clang often breaks geomad Cython builds (_Float16 SDK errors).
  # Apple system clang from Xcode Command Line Tools is reliable.
  export CC="${CC:-/usr/bin/clang}"
  export CXX="${CXX:-/usr/bin/clang++}"
  echo "macOS: using CC=$CC CXX=$CXX (needed to build geomad from source)"
fi

uv python install 3.12
uv sync --frozen "$@"

echo
echo "Verify:"
uv run python -c "import llvmlite, geomad, numba; print('llvmlite', llvmlite.__version__, '| geomad', geomad.__version__, '| numba', numba.__version__)"
