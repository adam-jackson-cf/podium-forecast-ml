# Assessment and verification boundaries

## Coding-agent linting research

The [coding-agent linting and codebase inertia report](../.enaible/deep-topic-research/20260910T152622Z-coding-agent-lint-rules-and-codebase-inertia/report.md) and its [candidate matrix](../.enaible/deep-topic-research/20260910T152622Z-coding-agent-lint-rules-and-codebase-inertia/rule-matrix.md) are the immutable assessment of the starting implementation at commit `54b2c88`. The [verification improvement plan](verification-improvement-plan.md) records the approved implementation scope and acceptance boundary for selected candidates.

| Research candidates | Current implementation status | Remaining boundary |
| --- | --- | --- |
| C02, C07 | Implemented through selected Ruff time and exception-test rules | Runtime forecast semantics still require real domain behaviour |
| C03, C05 | Implemented for configured known direct effects, import aliases and whole-package cycles | Effect analysis does not track object aliases, dataflow or dynamic dispatch; the cycle contract supplements the canonical layer policy |
| C17, C23 | Implemented through blocking Zizmor and external-entrypoint failure coverage | Local execution does not establish hosted CI behaviour |
| C19 | Partially implemented through bounded all-profile policy over normalized Compose JSON | Local rendering checks configured known capabilities; it is not a complete service-purity or runtime-security proof. AWS plan policy remains deferred until an environment root and deployment contract exist |
| C01, C04, C08, C20 | Partially implemented through selected Ruff and mypy rules plus agent guidance | No real job failure type, structured ML event schema or runtime task lifecycle exists; untyped external payloads still require validation at ingress |
| C06 | Deferred until the first production package | The current container remains a development foundation |
| C09–C12 | Deferred advisory heuristics | Representative product code and false-positive evidence are required before adopting thresholds |
| C13–C16, C18, C21 | Deferred until the repository owns the corresponding data, model, extraction, publication or migration contract | No placeholder model, data, SQL or migration implementation is present |
| C22 | Applied as behavioural test discipline for new gates; no property-testing framework added | Add transformation properties with the first real feature slice |

[Local solution assessment](local-solution-assessment.md) records the four options, the selected portable foundation, promotion principles and report provenance. It distinguishes observed source evidence, recommendations and later implementation requirements.

## Available foundation and future work

| Area | Available foundation | Not established by this scaffold |
| --- | --- | --- |
| Agent guidance | Root conditional routing, scoped instructions, three focused skills and three on-demand agent contracts | Runtime registration of custom agents |
| Python design | Typed package boundaries and executable quality policy | Extraction, features, training, evaluation or prediction |
| Local services | PostgreSQL, S3-compatible storage and MLflow configuration | Nexus schema, approved production extracts or Aurora parity |
| AWS IaC | Terraform storage configuration with native assertions | Applied AWS environment or permission/network correctness |
| Slow seam | One opt-in real-service foundation journey | Actual Nexus publication, operator acceptance or model quality |
| Promotion | Assessment of artifact and configuration boundaries | Approved model, release manifest lifecycle or production deployment |

## Verification matrix

| Layer | Control | Claim it supports |
| --- | --- | --- |
| Python formatting and lint | Ruff configured in pyproject.toml | Selected naming, complexity, time, exception and logging conventions |
| Type checking | Strict mypy configuration | Static agreement with declared types, checks for discarded awaitable results and stronger `Any` restrictions in core packages |
| Bespoke policy | verification package and quality-policy.toml | Architectural import direction, configured known direct effects, deterministic design rules and prohibited bypasses |
| Package graph | Import Linter | Whole-package sibling cycles in addition to the canonical layer policy |
| GitHub Actions security | Zizmor through the external-contract entrypoint | Selected workflow risks with strict blocking results |
| Rendered local configuration | Bounded all-profile Compose JSON policy through the external-contract entrypoint | Selected known capabilities in normalized configuration without starting services; not complete service-purity or runtime-security proof |
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

## Resulting-tree evidence — 10 September 2026

The completed implementation run was `verification-improvements-20260910T193145Z`. The full fast gate completed with exit code 0; its ignored local log is `.local/evidence/verification-improvements-20260910T193145Z/fast-final.log`.

| Executed check | Result |
| --- | --- |
| Fast behavioural tests | 156 passed in 13.41 seconds |
| Branch-inclusive verification coverage | 93.68%; existing configured coverage gate passed |
| Strict mypy | Passed across 23 source files |
| Ruff lint and formatting | Passed |
| Bespoke design policy | Passed |
| Import Linter | Current root-package contract passed with 1 file and 0 dependencies; isolated negative fixtures proved cycle rejection |
| Zizmor | Mandatory regular-persona scan passed with 0 findings; independent offline auditor scan also passed with 0 findings after workflow job-name and concurrency corrections |
| Rendered Compose policy | Every profile passed the bounded normalized-JSON policy without starting services |
| Terraform and infrastructure checks | 3 native Terraform tests, TFLint, Trivy with 0 HIGH or CRITICAL findings, and redacted Gitleaks passed |

The real-service slow seam completed with exit code 0: one journey passed in 2.50 seconds. Its ignored local log is `.local/evidence/verification-improvements-20260910T193145Z/slow.log`. The seam removed all scoped containers, volumes and its network; a separate scoped listing found none remaining.

The resulting image was `sha256:21a2d65614bbaaf7e42bfe62040766a4da8381adb952ecdb33672f9bbf89ddea` on `linux/arm64`. These results establish the configured controls and available local foundation journey on the resulting tree. Hosted CI, AWS execution, ML behaviour, model quality and Nexus integration were not executed or established.
