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
  # Force system clang (ignore conda CC already in the shell).
  export CC="/usr/bin/clang"
  export CXX="/usr/bin/clang++"
  echo "macOS: using CC=$CC CXX=$CXX (needed to build geomad from source)"

  # geomad uses OpenMP (see geomad/setup.py: cimport openmp in pcm.pyx).
  # Xcode clang does NOT ship omp.h — install libomp via Homebrew.
  if ! command -v brew &>/dev/null; then
    echo "ERROR: Homebrew is required on macOS (for libomp / OpenMP)."
    echo "       Install from https://brew.sh then re-run: ./scripts/sync-env.sh"
    exit 1
  fi
  if ! brew list libomp &>/dev/null 2>&1; then
    echo "Installing libomp (OpenMP headers — required by geomad) ..."
    brew install libomp
  fi
  LIBOMP="$(brew --prefix libomp)"
  if [[ ! -f "${LIBOMP}/include/omp.h" ]]; then
    echo "ERROR: omp.h not found under ${LIBOMP}/include"
    echo "       Try: brew reinstall libomp"
    exit 1
  fi
  # geomad's setup.py hardcodes /usr/local/include; CPATH/CFLAGS cover Apple Silicon too.
  export CPATH="${LIBOMP}/include${CPATH:+:$CPATH}"
  export LIBRARY_PATH="${LIBOMP}/lib${LIBRARY_PATH:+:$LIBRARY_PATH}"
  export CFLAGS="-I${LIBOMP}/include -Xpreprocessor -fopenmp${CFLAGS:+ $CFLAGS}"
  export LDFLAGS="-L${LIBOMP}/lib -lomp${LDFLAGS:+ $LDFLAGS}"
  echo "macOS: OpenMP from ${LIBOMP}"
fi

# Harmless setuptools-scm warning during geomad compile on macOS (can ignore).
export PYTHONWARNINGS="${PYTHONWARNINGS:+$PYTHONWARNINGS,}ignore:No GlobalOverrides context is active:UserWarning"

uv python install 3.12
uv sync --frozen "$@"

echo
echo "Verify:"
uv run python -c "import llvmlite, geomad, numba; print('llvmlite', llvmlite.__version__, '| geomad', geomad.__version__, '| numba', numba.__version__)"
