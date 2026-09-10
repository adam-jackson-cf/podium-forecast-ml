#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$PWD/.tools/bin:$PATH"
for tool in uv terraform tflint trivy actionlint shellcheck hadolint gitleaks; do
  command -v "$tool" >/dev/null || { printf 'Required tool missing: %s\n' "$tool" >&2; exit 1; }
done
uv sync --frozen
uv run --frozen python -m verification
uv run --frozen ruff check .
uv run --frozen ruff format --check .
uv run --frozen mypy .
uv run --frozen pytest tests/unit tests/integration --cov=verification --cov-report=term-missing
uv run --frozen yamllint .
uv run --frozen sqlfluff lint . --dialect postgres
actionlint
shellcheck scripts/*.sh
find containers -maxdepth 1 -type f \( -name Dockerfile -o -name '*.Dockerfile' \) -exec hadolint {} +
terraform fmt -check -recursive infra/terraform
terraform -chdir=infra/terraform/modules/storage init -backend=false -input=false -lockfile=readonly
terraform -chdir=infra/terraform/modules/storage validate
terraform -chdir=infra/terraform/modules/storage test
tflint --chdir=infra/terraform/modules/storage --config="$PWD/.tflint.hcl"
trivy config --exit-code 1 --severity HIGH,CRITICAL \
  --tf-vars "$PWD/infra/terraform/modules/storage/tests/security.tfvars" infra/terraform
gitleaks dir --redact --no-banner --exit-code 1 .
