# Shared settings for local notebook execution (sourced by start/build scripts).
# Override if needed:  NCK_JUPYTER_PORT=8889 ./scripts/start-site-execute.sh

NCK_JUPYTER_PORT="${NCK_JUPYTER_PORT:-8888}"
NCK_JUPYTER_TOKEN="${NCK_JUPYTER_TOKEN:-nck-local-execute}"

print_jupyter_connection() {
  echo ""
  echo "=============================================="
  echo "  Jupyter server (for notebook execution)"
  echo "  URL:    http://127.0.0.1:${NCK_JUPYTER_PORT}"
  echo "  Token:  ${NCK_JUPYTER_TOKEN}"
  echo "  Full:   http://127.0.0.1:${NCK_JUPYTER_PORT}/?token=${NCK_JUPYTER_TOKEN}"
  echo "=============================================="
  echo "  Tutorial site preview:  http://localhost:3000"
  echo "  (open 3000 in your browser — not 8888)"
  echo "=============================================="
  echo ""
}
