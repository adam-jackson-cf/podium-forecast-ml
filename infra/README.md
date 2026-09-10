# Infrastructure

The local stack uses PostgreSQL 17.7, SeaweedFS S3-compatible storage and MLflow. MLflow uses a separate metadata database within the same PostgreSQL instance, with a local administrative database login only. It is a portable service foundation; it does not emulate Aurora, SageMaker, EventBridge or CloudWatch.

## Local service lifecycle

From the repository root, after dependency installation:

```sh
uv run python scripts/prepare_local.py
docker compose -f infra/local/compose.yaml up --build --wait
```

The stack uses its container network and exposes no host UI ports. Generated local credentials must remain ignored and must not be printed or copied into committed configuration. Use the single smoke entrypoint in the root README for disposable verification.

To stop the persistent stack while retaining its volumes:

```sh
docker compose -f infra/local/compose.yaml down
```

## AWS configuration boundary

Terraform modules define AWS resources independently of the local service launcher. Native Terraform tests use mocked providers to verify configuration assertions; they do not apply infrastructure and cannot prove cloud permissions, networking, service compatibility or model execution.

The source Podium snapshot supports alignment with Terraform 1.14.7, PostgreSQL 17.7 and AWS region eu-west-1. This is snapshot evidence, not inspection of a live AWS environment. Keep separate state and explicit configuration for each eventual AWS environment. Cloud service roles, IAM integration and environment deployment roots are deliberately not implemented. No cloud deployment is part of this scaffold.
