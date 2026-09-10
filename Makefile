.PHONY: check smoke bootstrap
check:
	./scripts/fast-checks.sh
smoke:
	./scripts/slow-seam.sh
bootstrap:
	uv sync --frozen
	uv run --frozen python scripts/bootstrap_tools.py
