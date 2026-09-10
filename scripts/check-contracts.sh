#!/usr/bin/env bash
set -euo pipefail

if (( $# > 1 )); then
  printf 'Usage: %s [fixture-root]\n' "$0" >&2
  exit 2
fi

project_root="$(cd "$(dirname "$0")/.." && pwd -P)"
target_root="${1:-$project_root}"
if [[ ! -d "$target_root" ]]; then
  printf 'External-check root is not a directory.\n' >&2
  exit 1
fi
target_root="$(cd "$target_root" && pwd -P)"

package_dir="$target_root/src/podium_forecasting"
config_file="$target_root/pyproject.toml"
workflow_dir="$target_root/.github/workflows"
compose_file="$target_root/infra/local/compose.yaml"

if [[ ! -d "$package_dir" ]] ||
  ! find "$package_dir" -type f -name '*.py' -size +0c -print -quit | grep -q .; then
  printf 'External-check root requires a nonempty podium_forecasting Python package.\n' >&2
  exit 1
fi
if [[ ! -s "$config_file" ]]; then
  printf 'External-check root requires a nonempty pyproject.toml.\n' >&2
  exit 1
fi
if [[ ! -d "$workflow_dir" ]] ||
  ! find "$workflow_dir" -type f \( -name '*.yaml' -o -name '*.yml' \) -size +0c -print -quit |
    grep -q .; then
  printf 'External-check root requires a workflow directory with nonempty YAML input.\n' >&2
  exit 1
fi
if [[ ! -s "$compose_file" ]]; then
  printf 'External-check root requires a nonempty Compose file.\n' >&2
  exit 1
fi

command -v uv >/dev/null || { printf 'Required tool missing: uv\n' >&2; exit 1; }
command -v docker >/dev/null || { printf 'Required tool missing: docker\n' >&2; exit 1; }
docker compose version >/dev/null

(
  cd "$target_root"
  PYTHONPATH="$target_root/src" \
    uv run --project "$project_root" --frozen --no-sync lint-imports \
      --config pyproject.toml \
      --no-cache
)
uv run --project "$project_root" --frozen --no-sync zizmor \
  --collect=workflows \
  --strict-collection \
  --persona=regular \
  --no-ignores \
  --offline \
  --format=plain \
  --no-progress \
  "$target_root"
docker compose \
  --project-directory "$target_root" \
  --file "$compose_file" \
  --profile '*' \
  config \
  --format json |
  (
    cd "$project_root"
    uv run --frozen --no-sync python -m verification.compose_policy
  )
