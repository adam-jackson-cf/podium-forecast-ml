# Verification and program guidance improvement plan

## Objective and scope

Implement the research improvements that have concrete value for the current scaffold, strengthen guidance for future implementation, and finish with the complete project baseline green. Preserve the research snapshot and existing gates. Do not implement the ML pipeline, introduce Nexus write authority, deploy AWS resources, or invent model/data contracts.

The starting implementation is commit `54b2c88`. The preceding research and its documentation index are already present as uncommitted work and must be retained. The source assessment is the research run `20260910T152622Z-coding-agent-lint-rules-and-codebase-inertia`.

## Design decisions

- Reuse pinned Ruff and mypy. Add narrow rules rather than `ALL`, a second general-purpose linter, or a blanket opinionated preset.
- Keep the current allowed-layer map canonical. Add Import Linter only for the missing whole-package cycle invariant, not a competing layer hierarchy.
- Enforce configured known direct IO calls and import aliases in the existing verification package. Allow `Path` construction and pure manipulation; reject configured effectful operations. Object/dataflow aliases and dynamic dispatch are outside this bounded static check. Do not claim complete effect analysis.
- Keep `unused-awaitable` and `exhaustive-match` global in mypy. Apply `disallow_any_expr`, `disallow_any_explicit` and `disallow_any_unimported` only to `podium_forecasting`, `podium_forecasting.domain`, `podium_forecasting.domain.*`, `podium_forecasting.ports`, `podium_forecasting.ports.*`, `podium_forecasting.application` and `podium_forecasting.application.*`. Do not obtain green by introducing unchecked casts.
- Keep shell orchestration thin. A shared, explicit entrypoint for the new external checks is acceptable only to let integration tests exercise the same blocking path as the fast runner. No generic dispatcher, plugin framework or additional slow suite.
- Use small Python checks on rendered Compose JSON. Do not add Rego/Conftest, an AWS deployment root or a speculative Terraform-plan policy in this increment.
- Keep current limits and coverage requirements. Fix findings; do not add suppressions, broad exemptions, report-only success, trivial regular-expression matches or manufactured test coverage.
- Keep human setup and execution procedures in README files; agent behaviour belongs in scoped AGENTS files, skills and role briefs.

## Activities and acceptance

| Activity | Implementation | Acceptance |
| --- | --- | --- |
| P1 | Review this plan with a KISS-focused subagent and resolve its material findings before code changes. | A retained review identifies unnecessary machinery, missing failure checks and scope drift; the revised plan is suitable for implementation. |
| P2 | Enable supported Ruff BLE001, DTZ, PT011/PT012 and G004; add the exact mypy optional checks and core module overrides listed above. Fix existing code/tests that violate the rules without incidental-value assertions or suppressions. | Run representative fixtures through the pinned tools and production configuration. Bad behaviours fail; meaningful valid cases pass. Extend parameterized scenarios instead of adding one microtest per diagnostic. |
| P3 | Extend the current architecture verifier with a bounded known-effect policy for domain, ports and application. Keep configuration canonical; test imports/aliases, permitted pure operations and adapter ownership. | Configured known direct calls/import aliases are rejected; the same owned capability in an adapter and pure `Path` manipulation remain valid. Unsupported object/dataflow aliases and dynamic dispatch are honestly documented. |
| P4 | Pin Import Linter 2.15 and zizmor 1.30.1 in the existing uv toolchain. Configure an acyclic-sibling contract at the existing package root. Use one fixed thin shell entrypoint, with at most one optional fixture-root argument, to require expected inputs and run Import Linter, strict/no-ignore zizmor and rendered Compose validation. Set both checkout steps to avoid credential persistence. | A complete isolated fixture root exercises the same entrypoint called by the fast gate. A cycle, risky workflow, malformed input and missing required input each fail; the valid fixture passes. No modes/plugins/dispatcher or SARIF-only success path. |
| P5 | Render all Compose profiles, including optional services, before checking JSON with the existing Python verification package. Cover privileged/host-network operation, direct Docker-socket mounts, external image digest pins, loopback-only published ports and the existing internal-network design. Allow explicitly locally built images and their consumers. | Safe current Compose passes without starting services. Unsafe overrides, including an unsafe service present only in an optional profile, and malformed/unknown required structures fail. Diagnostics do not dump configuration or secret values. Docker Compose availability is an explicit prerequisite. |
| P6 | Update progressive guidance and README documentation, including the research-to-implementation mapping and deferred controls. Exercise the complete fast gate and existing real-service slow seam, review the result and repair any failures. | All current and new mandatory checks pass, the real foundation journey and cleanup pass, and the final evidence describes the exact scope. No ML/Nexus/AWS readiness is implied. |

## Work ownership

GPT Sol low-reasoning implementation workers will have non-overlapping ownership:

1. **Python policy worker:** all `verification/**`, `quality-policy.toml`, Python policy unit tests, `pyproject.toml`, `uv.lock`, Import Linter configuration/dependencies and necessary existing Python repairs. Own both the effect policy and the rendered Compose JSON checker. Coordinate its CLI contract with worker 2.
2. **External/infrastructure worker:** thin shell external-check entrypoint, fast-runner integration, workflows and external integration fixtures/tests. No Python policy-module edits and no changes to the model/service behaviour of the slow seam.
3. **Guidance worker:** root/scoped agent guidance, focused skills/role briefs, README procedures and implementation-status documentation. Preserve existing research artifacts and historical baseline evidence.

The orchestrator owns sequencing, review decisions, integration verification and the final account. Workers must not revert one another's edits. Shared file changes require coordination with their named owner.

## Research mapping and intentional deferrals

| Research candidates | This increment |
| --- | --- |
| C01, C02, C04, C07, C08, C20 | Add the supported narrow lint/type protections and guidance. Full job failure-state propagation and structured ML event schemas remain dependent on real job implementation. |
| C03, C05 | Add known-effect ownership and whole-package cycle protection while retaining existing layer rules. |
| C17, C23 | Add workflow security and meaningful failure/input-coverage tests for the actual external-check entrypoint. |
| C19 | Implement local rendered-Compose policy only. AWS plan policy awaits an actual environment root and approved deployment contract. |
| C06 | Document production/dev dependency separation; adopt dependency-use validation with the first production package. The current container is a development foundation. |
| C09–C12 | Retain as advisory designs. Do not add dead-code, clone or abstraction/coupling thresholds without representative product code. |
| C13–C16, C18, C21 | Defer runtime data, lifecycle, extraction and migration controls to the first owned implementation and agreed domain contracts. Do not create placeholder implementations. |
| C22 | Apply behavioural test discipline to this work. Do not add a property-testing framework solely to increase the tool count. |

## Verification and completion boundary

Retain the existing fast command as the authoritative aggregate gate and the existing single slow seam as the on-demand real-service journey. New external integration tests must use real installed checkers and the production gate entrypoint against isolated fixtures; mocking a successful scanner is not acceptance evidence. Keep those tests independent of a running service stack and network access after dependency preparation.

Run a KISS-focused completion review after implementation. Finish only when the full fast gate and slow seam pass on the resulting tree, cleanup is confirmed, and documentation matches implementation. Preserve historical baseline evidence and record a new dated resulting-tree run. Hosted CI and AWS execution remain unverified. Record limitations and deferred items as scope boundaries rather than treating them as completed controls.

## KISS review disposition

The Sol low-reasoning KISS subagent returned PASS WITH REQUIRED CHANGES. All six required changes are incorporated: all-profile Compose rendering and its negative case; bounded effect claims without blanket `Path` prohibition; non-overlapping ownership; exact mypy overrides; a fixed shared shell entrypoint tested end-to-end; and historical/new evidence separation. The review found Import Linter proportionate for the missing cycle invariant and rejected a broader verification framework or another slow suite.

## Status

- P1 complete: KISS review passed after the six required changes were incorporated.
- P2–P5 complete: Sol low-reasoning workers implemented the reviewed controls and real-checker failure tests. Existing rules and thresholds were retained.
- P6 complete: the full fast gate passed 156 tests with 93.68% branch-inclusive verification coverage; all three Terraform tests passed; the existing real-service seam passed and removed its containers, volumes and network. KISS source review passed.
- The broader offline workflow audit also passed after explicit job names and concurrency policies were added. No application/runtime service behaviour changed.
- New dated evidence is retained under `.local/evidence/verification-improvements-20260910T193145Z/`, with the resulting baseline documented in `docs/README.md`. Historical evidence and research remain intact.
- Hosted CI, live AWS behaviour and the intentionally deferred ML-specific controls are not verified by this baseline.
