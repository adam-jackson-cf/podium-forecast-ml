# Local solution assessment

Assessment date: 10 September 2026. Scope: Workstream B - ML predictive forecasting.

## Evidence and decision status

The source is the Podium executive report, generated 9 September 2026, with report context as of 3 September 2026 and technical-debt context as of 9 September 2026. Its source location at assessment time was `/Users/adamjackson/Projects/tools/project-planning/podium/output/html/podium-executive-report.html`, section `workstream-b`, including architecture and training-platform choices. This assessment records the relevant content so the repository does not depend on that external file to explain its design.

The report proposes a new ML capability; it does not establish an approved training platform or implemented pipeline. Aurora remains the operational system of record. Immutable race-time snapshots go to versioned S3 datasets; data/model checks run outside Nexus; only approved predictions are published through GraphQL. Direct ML writes to Nexus would bypass its validation, authorization, audit and event behaviour. The target, forecast cut-off and provenance-confirmed baseline remain decisions, and the report explicitly requires delivery-team validation of its proposed approach.

The four-option assessment below preserves the recommendations shared before repository creation. AWS, LocalStack and MLflow documentation were reported checked in that discussion on 10 September 2026; the links retain that provenance rather than imply a fresh service-coverage audit by this document. Coverage and licensing should be rechecked when an option is adopted.

The concrete scaffold selects **Option 1**, with PostgreSQL, SeaweedFS S3-compatible object storage and MLflow. SeaweedFS is a local object-storage primitive, not an AWS emulator or an Aurora substitute. Option 2 and selective Option 3 remain later choices. Option 4 is the required real-AWS verification stage before promotion claims. No ML extraction, feature engineering, training, approval or Nexus publication is implemented by the scaffold.

## Recommendation

Build extraction, feature engineering, training, evaluation and prediction as real Python container jobs. Run the same release artifacts locally and in AWS. Combine portable compute with selected AWS integration checks rather than trying to reproduce every managed service locally.

“Promote when ready” means promoting tested code, images, models and infrastructure definitions. Local database state, emulator resources and local approval records must not automatically become production state.

## Options

| Option | Local arrangement | Path to AWS | Trade-off |
| --- | --- | --- | --- |
| 1. Portable container stack | Docker Compose, PostgreSQL, object storage, MLflow and real Python jobs | Run the same jobs in SageMaker or an agreed AWS container runtime | Simplest development foundation; AWS orchestration requires separate verification |
| 2. SageMaker local mode | SageMaker Python SDK executes supported steps in Docker alongside local dependencies | Reuse supported pipeline definitions through a managed SageMaker session | Closer to the owned SageMaker route, but only part of SageMaker runs locally |
| 3. LocalStack-centred AWS emulation | LocalStack represents selected AWS APIs alongside real PostgreSQL and ML containers | Reuse supported SDK calls and infrastructure definitions against AWS | Better integration coverage, subject to API gaps, licensing and behavioural differences |
| 4. Local compute plus real AWS development services | Local containers use development S3, registry, scheduling and other AWS resources | Smallest managed-service gap before deployment | Requires account access, connectivity and running costs |

Start with Option 1. Add Option 2 if SageMaker Pipelines is selected, selective Option 3 tests when their exact operations are supported, and Option 4 as the promotion checkpoint. These can be configurations of one implementation; they should not become separate versions of the ML logic.

### Important limits

SageMaker local mode is not a complete offline installation. The cited AWS page lists training, processing, transform, create-model, condition and fail steps, sequential execution and default S3 artifact use. Model registration is outside that supported step set. XGBoost needs script mode for local pipelines rather than the built-in algorithm route. Switching sessions does not remove the need for cloud configuration and unsupported-step handling. [AWS local-mode documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/pipelines-local-mode.html)

LocalStack provides partial emulation. The cited SageMaker page describes a subset, excludes GPU models and marks persistence unsupported. Plan availability is distinct from API completeness. Verify the exact operations before relying on it to execute an ML lifecycle. [SageMaker coverage](https://docs.localstack.cloud/aws/services/sagemaker/) and [licensing](https://docs.localstack.cloud/aws/licensing/)

## Service mapping

| Report component | Local representation | Portable contract and verification boundary |
| --- | --- | --- |
| Aurora PostgreSQL | PostgreSQL using the relevant Nexus schema, migrations and approved extract; read-only extraction role | SQL/schema/extraction logic can carry over. Aurora extensions and infrastructure behaviour require AWS checks. The scaffold does not include the Nexus schema or extract |
| Versioned S3 datasets | S3-compatible storage in the initial stack; optional LocalStack S3 later | Preserve object layout, Parquet, checksums, schema, lineage and immutable manifests. Do not use cloud version IDs as the sole portable dataset identity |
| Feature engineering and quality gates | Real Python job containers when implemented | Identical executable code and contracts in both environments |
| CatBoost / XGBoost training | CPU custom training containers; SageMaker local mode if selected | Same code/dependencies; verify target CPU architecture and move larger runs to AWS |
| Back-testing and evaluation | Dedicated job producing machine-readable evidence | Same race partitions, cut-offs, baseline comparisons and acceptance rules |
| MLflow | MLflow server with PostgreSQL metadata and object-storage artifacts | Tracking conventions and artifacts carry over; actual cloud authentication and storage configuration need verification |
| SageMaker Model Registry | Local model package and evaluation evidence; actual AWS registration in integration testing | MLflow records do not establish SageMaker registration or environment approval |
| EventBridge | Explicit local invocation initially; supported LocalStack trigger tests later | Keep event payloads identical; validate actual retries, targets and permissions in AWS |
| Batch inference | One-shot prediction container when implemented | Promote image and approved model; configure the cloud executor |
| GraphQL publication and operator review | Actual Nexus API and necessary application components when available | A substitute API can support contract tests but cannot establish Nexus integration |
| CloudWatch | Structured container logs initially; cloud log and metric checks later | Preserve correlation IDs and log fields; delivery, permissions and alarms require AWS checks |
| Terraform / GitHub Actions | Terraform AWS resources, Compose service lifecycle and blocking automated checks | Separate environment configuration and state; Compose remains a local launcher |

MLflow supports the database/object-storage tracking arrangement. [MLflow self-hosted architecture](https://mlflow.org/docs/latest/self-hosting/architecture/overview/)

The selected object-storage primitive supplies an S3-compatible API. This is a concrete implementation choice within Option 1, replacing the initial assessment's suggested LocalStack S3 representation for the first scaffold; it does not assert complete S3 behavioural parity. [SeaweedFS official repository](https://github.com/seaweedfs/seaweedfs)

## Intended pipeline, after the scaffold

```text
Local Nexus PostgreSQL -- read-only extraction
  -> versioned Parquet + dataset manifest
  -> quality gates -> features -> training -> back-test
  -> model + evaluation evidence
  -> explicit approval
  -> trigger -> batch prediction -> domain checks -> Nexus GraphQL
  -> operator review + outcomes
```

A model that fails evaluation retains its evidence and stops before publication. Every runner from one race stays in the same partition. The newest complete period is an untouched out-of-time holdout. Evaluate numeric price error, odds-ladder distance, race-level coherence, segment performance and whether users keep or change the suggestion. A repeatable no-go finding remains a valid outcome.

## Promotion design

1. One implementation per ML stage. Configuration supplies endpoints, database connections, tracking location and execution settings; feature logic and acceptance rules remain identical.
2. Build release images once and identify them by digest. Verify the intended AWS CPU architecture. An Apple Silicon development build alone does not verify an x86 release.
3. A portable release manifest records source revision, image digest, dataset checksums, feature schema, parameters, model checksum and evaluation results.
4. One authoritative approval location per environment. Proposed division: MLflow owns experiment evidence; SageMaker Model Registry owns cloud release approval if selected. Avoid competing approval states.
5. Terraform provisions AWS with separate environment state. Roles, account IDs, networking, encryption and sizing are environment-specific. Local emulation cannot prove these controls correct.

```text
Local behavioural checks
  -> AWS development run using release images
  -> model registration + cloud integration checks
  -> staging prediction + Nexus publication acceptance
  -> approval of the tested release for its target environment
```

Infrastructure readiness and model readiness are separate. A functioning pipeline may reach staging while its model remains unsuitable for publication.

## Iteration after the verified scaffold

The first product slice should contain one approved dataset with complete races and forecast-time evidence, one simple baseline, one CatBoost candidate, extraction through evaluation, reproducible artifacts and tracking, an explicit approval gate, batch prediction and actual local Nexus publication. The same release then runs in AWS development.

Acceptance must protect leakage prevention, race-aware partitions, rejected-model non-publication, duplicate-trigger handling, operator-change preservation and traceability to model and input snapshot.

Before dependent ML implementation, settle the exact target, forecast cut-off, provenance-confirmed baseline, local Nexus/schema availability, and SageMaker Pipelines versus a general container-job runtime. Canvas/Autopilot remain optional AWS challenger experiments, not prerequisites for the owned local pipeline. These decisions are not resolved by green scaffold checks.

## Existing Podium infrastructure alignment

A supplied Podium infrastructure snapshot was inspected during scaffold creation: `podium-aws-infrastructure-modernisation-main` in the report's source workspace. Its `.terraform-version` specifies Terraform 1.14.7; the development provider configuration requires `~> 1.14`; the Aurora module's engine-version default is 17.7; and the development, staging and production region settings are `eu-west-1`.

These are source-snapshot observations, not verification of deployed AWS resources. They inform tool and PostgreSQL compatibility choices without importing existing environment state, credentials or deployment authority. The new scaffold remains separate from Nexus's operational database.
