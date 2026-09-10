# Assessment and verification boundaries

[Local solution assessment](local-solution-assessment.md) records the four options, the selected portable foundation, promotion principles and report provenance. It distinguishes observed source evidence, recommendations and later implementation requirements.

## Available foundation and future work

| Area | Available foundation | Not established by this scaffold |
| --- | --- | --- |
| Agent guidance | Short root routing, scoped instructions, three focused skills and role briefs | Runtime registration of custom agents |
| Python design | Typed package boundaries and executable quality policy | Extraction, features, training, evaluation or prediction |
| Local services | PostgreSQL, S3-compatible storage and MLflow configuration | Nexus schema, approved production extracts or Aurora parity |
| AWS IaC | Terraform storage configuration with native assertions | Applied AWS environment or permission/network correctness |
| Slow seam | One opt-in real-service foundation journey | Actual Nexus publication, operator acceptance or model quality |
| Promotion | Assessment of artifact and configuration boundaries | Approved model, release manifest lifecycle or production deployment |

## Verification matrix

| Layer | Control | Claim it supports |
| --- | --- | --- |
| Python formatting and lint | Ruff configured in pyproject.toml | Selected naming, complexity and code conventions |
| Type checking | Strict mypy configuration | Static agreement with declared types |
| Bespoke policy | verification package and quality-policy.toml | Architectural import direction, deterministic design rules and prohibited bypasses |
| Fast behavioural tests | Unit/integration tests | Gate behaviour on accepted and rejected structures |
| Container, shell and CI checks | Hadolint, ShellCheck, actionlint and yamllint through the fast-checks entrypoint | Dockerfile, shell, workflow and YAML constraints |
| SQL checks | SQLFluff with the PostgreSQL dialect | SQL syntax/style constraints |
| Infrastructure and secrets checks | TFLint, Trivy configuration scanning and redacted Gitleaks | Selected Terraform risks and potential committed-secret patterns |
| Terraform validation/tests | Native provider-backed validation and mocked test assertions | Valid configuration and declared storage controls, without cloud execution |
| Real-service smoke | Single slow-seam entrypoint | Tangible interaction with the actual local foundation services |
| Skill validation | Frontmatter validation and behaviour-guidance checklist | Discoverable, bounded instructions without unresolved scaffold content |

Exact enabled rules and thresholds live in executable configuration. Passing static checks alone does not establish runtime behaviour. Passing local runtime checks does not establish AWS compatibility. The final baseline evidence should identify commands actually executed and their results; unavailable checks remain unverified.

## First subsequent implementation boundary

The next product slice is one approved dataset, a simple baseline, one CatBoost candidate, evaluation evidence, an approval boundary, batch prediction and real Nexus publication. Entry decisions are target, forecast cut-off, baseline provenance, schema/API availability and execution runtime. The same tested release must then pass AWS development verification. This work is intentionally outside foundation scaffolding.

## Baseline evidence — 10 September 2026

The final fast-check entrypoint completed with exit code 0. Its local execution log is `.local/evidence/fast-checks.log` (ignored runtime evidence, not a committed artifact).

| Executed check | Result |
| --- | --- |
| Fast behavioural tests | 103 passed in 0.77 seconds |
| Verification-code coverage | 96.03%; configured coverage gate passed |
| Strict mypy | Passed across 19 source files |
| Ruff lint and formatting | Passed |
| Bespoke architecture, design, instruction and path checks | Passed |
| YAML, SQLFluff, actionlint, ShellCheck and Hadolint | Passed |
| Terraform formatting, validation and native tests | Passed; 3 native tests passed |
| TFLint | Passed |
| Trivy configuration scan | Passed; no HIGH or CRITICAL findings |
| Redacted Gitleaks scan | Passed |
| Independent completion review | PASS; no findings remaining after repairs |

These results establish the configured foundation controls on this local checkout. They do not establish ML quality, Nexus integration, live AWS behaviour or a production-ready release. The final real-service smoke completed with exit code 0: one test passed in 3.12 seconds. Its own containers, volumes and network were removed, with a separate scoped Docker listing confirming no remaining resources. The ignored local log is `.local/evidence/slow-seam.log`.

The local runtime image ID was `sha256:69a5edb9f7d161cbccbbc34688e07f85de96d39d7a62c5d0799cfa40dac486d2` on `linux/arm64` with uv 0.10.0. This establishes the real local foundation journey on that architecture. Live AWS, hosted CI and Linux x86-64 runtime execution were not run; verification of Linux tool archives is not runtime verification. No ML pipeline code or model-quality claim is included.
