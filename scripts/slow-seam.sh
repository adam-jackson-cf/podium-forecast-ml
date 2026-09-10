#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v docker >/dev/null
command -v uv >/dev/null
docker compose version >/dev/null
LOCAL_SECRETS_DIR=$(mktemp -d)
export LOCAL_SECRETS_DIR
FOUNDATION_IMAGE_TAG="seam-$$"
export FOUNDATION_IMAGE_TAG
compose=(docker compose -p "podium-seam-$$" -f infra/local/compose.yaml)
cleanup() {
  result=$?
  trap - EXIT
  if ! "${compose[@]}" down --volumes --remove-orphans >/dev/null; then
    printf '%s\n' 'Container teardown failed; inspect the named seam project.' >&2
    result=1
  fi
  uv run --frozen python -c 'import os; from pathlib import Path; p=Path(os.environ["LOCAL_SECRETS_DIR"]); (p/"postgres_password").unlink(missing_ok=True); (p/"s3_config.json").unlink(missing_ok=True); p.rmdir()'
  exit "$result"
}
trap cleanup EXIT
uv run --frozen python scripts/prepare_local.py
"${compose[@]}" build --quiet
"${compose[@]}" up --wait postgres object-store mlflow
"${compose[@]}" run --rm seam
