---
name: "testing-conventions"
description: "Use when adding or changing tests, verification gates, or smoke journeys to protect observable outcomes."
---

# Guidance

- Identify the behavioural rule before writing assertions. Extend the existing scenario when it already owns the rule.
- Assert observable outputs, persisted state and forbidden side effects. Do not encode incidental names, exact source text, private calls or one discovered example as the oracle.
- Use parameterised cases for meaningful partitions and boundary conditions; test both accepted and rejected inputs.
- Keep exception assertions around the intended failing operation so setup failures cannot satisfy the test. Verify that logged failures propagate and that asynchronous work has observable completion and failure handling.
- Use deterministic clocks and explicit input datasets where time or randomness matters. Keep synthetic fixtures confined to tests and label their purpose.
- Keep fast tests independent of network and services. Test doubles belong only at external boundaries and must not replace the behaviour under test.
- Maintain one opt-in slow smoke entrypoint spanning the real available infrastructure journey. Extend that journey as implementation becomes available; do not create parallel competing smoke suites.
- The smoke must verify tangible state changes through real services and clean up only its own resources. Service health alone is not a journey oracle.
- Missing smoke prerequisites are a failure with an actionable explanation, never a skipped pass.
- For ML implementation, protect forecast-time cut-offs, complete-race partitioning, untouched holdouts, failed-evaluation non-publication, lineage and preservation of operator changes.
- A scaffold smoke proves infrastructure interactions only. Do not claim extraction, training, approval or Nexus publication before those real stages exist and are exercised.
- Do not weaken thresholds or bypass checks to obtain a green result. Document which verification layer establishes each claim.
- For static-policy tests, include supported direct and import-alias cases plus permitted behaviour. Do not imply coverage of object aliases, runtime dataflow or dynamic dispatch unless the implementation actually analyses them.
