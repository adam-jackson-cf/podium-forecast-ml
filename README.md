# Podium forecasting ML

This repository establishes a containerised local development and verification foundation for Workstream B - ML predictive forecasting. It contains infrastructure primitives and code-design gates; it does not yet contain the ML pipeline or Nexus integration.

The intended path is portable Python container jobs first, optional SageMaker local mode and selected AWS emulation later, then a real AWS development verification stage before promotion. See [the local solution assessment](docs/local-solution-assessment.md) for options, evidence and decision boundaries.

## Structure

```text
.agents/skills/        Selective Python, testing and infrastructure guidance
.agents/roles/         On-demand implementation and review briefs
containers/           Locked foundation runtime image
infra/local/          PostgreSQL, S3-compatible storage and MLflow Compose stack
infra/terraform/      AWS infrastructure modules and native configuration tests
src/podium_forecasting/
  domain/             Domain concepts and calculations
  ports/              Typed external capability contracts
  application/        Use-case coordination through ports
  adapters/           Concrete IO implementations
  entrypoints/        Configuration and assembly
verification/         Executable repository design checks
scripts/              Verification and local lifecycle entrypoints
tests/                Fast behavioural coverage and the opt-in real-service seam
docs/                 Assessment and baseline boundaries
```

The source layers establish import boundaries; their presence does not claim implemented forecasting behaviour. New folders should own a concrete responsibility rather than accumulate generic utilities.

## Setup and verification

Use the pinned Python/tool versions in the repository configuration, `uv`, and the Docker CLI with Docker Compose. The fast gate renders Compose configuration for static policy across every profile, so it requires the client and Compose plugin but does not require a running Docker daemon. Keep local credentials and state out of Git.

The normal Docker client configuration works. If the current process already uses `DOCKER_CONFIG` to select another client configuration directory, the verification scripts preserve it; keep that directory and its contents private.

```sh
uv sync --locked
uv run --frozen python scripts/bootstrap_tools.py
uv run pre-commit install
scripts/fast-checks.sh
```

The bootstrap installs the pinned verification binaries for macOS Apple Silicon or Linux x86-64; see [toolchain setup](tools/README.md).

The fast entrypoint runs the configured code and infrastructure gates. Its external-contract stage uses dependencies pinned by `uv.lock` to check package cycles and GitHub Actions, then renders every Compose profile and validates the resulting JSON without starting services. Individual checks are:

```sh
uv run python -m verification
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest tests/unit tests/integration
scripts/check-contracts.sh
```

The hosted quality workflow groups runs by workflow and Git ref and cancels a superseded run for the same ref. The manually dispatched foundation-seam workflow uses the same grouping but does not interrupt a running requested seam. These are configured scheduling semantics; see the resulting-tree evidence for what was executed locally.

The slower integration seam requires a working Docker Engine. Run it explicitly:

```sh
scripts/slow-seam.sh
```

That command owns an ephemeral stack, creates per-run credentials and cleans up its resources. It must fail when prerequisites or real interactions fail. Its scope is the available infrastructure journey, not model accuracy or publication readiness. See [verification boundaries](docs/README.md).

For a persistent local service stack, see [infrastructure operation](infra/README.md).

## Contribution boundaries

Root and scoped `AGENTS.md` files guide coding agents. User-facing procedures live in README files. Small skills and role briefs are loaded only when relevant; role briefs are not registered runtime agents.

`quality-policy.toml` and `pyproject.toml` are authoritative for numeric limits, naming constraints, import rules and enabled checks. Do not duplicate thresholds in guidance or weaken a gate to accept a change. A new executable language requires its corresponding verification layer before implementation.

Before implementing ML behaviour, agree the target, forecast cut-off, provenance-confirmed baseline and Nexus integration contract. Cloud deployment also requires explicit environment configuration and verification of AWS permissions and networking. No scaffold result resolves these decisions.
