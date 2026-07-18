#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE_ROOT="${SOURCE_ROOT:-"$ROOT_DIR/../eshop-sut"}"
OUTPUT_DIR="${OUTPUT_DIR:-"$ROOT_DIR/src/semgrep/output"}"
RESULT_JSON="${RESULT_JSON:-"$OUTPUT_DIR/semgrep_results.json"}"

if [ ! -d "$SOURCE_ROOT" ]; then
  echo "Không tìm thấy source root: $SOURCE_ROOT" >&2
  echo "Đặt SOURCE_ROOT=/path/to/source rồi chạy lại." >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

if [ -f /opt/homebrew/etc/ca-certificates/cert.pem ]; then
  export SSL_CERT_FILE="${SSL_CERT_FILE:-/opt/homebrew/etc/ca-certificates/cert.pem}"
fi

echo "==> Semgrep scan: $SOURCE_ROOT"
semgrep scan \
  --config "p/owasp-top-ten" \
  --config "p/nodejs" \
  --exclude node_modules \
  --exclude dist \
  --exclude build \
  --exclude .next \
  --json \
  -o "$RESULT_JSON" \
  "$SOURCE_ROOT"

echo "==> AI triage output: $OUTPUT_DIR"
python "$ROOT_DIR/src/semgrep/semgrep_ai_triage.py" \
  "$RESULT_JSON" \
  --source-root "$SOURCE_ROOT" \
  --output-dir "$OUTPUT_DIR"
