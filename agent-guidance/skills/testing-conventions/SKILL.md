---
name: "testing-conventions"
description: "Use when adding or changing tests, verification gates, or smoke journeys."
---

# Guidance

- **ALWAYS** state the behavioural rule before adding assertions.
- If an existing scenario protects the rule, **ALWAYS** extend it instead of adding a narrow one-off regression test.
- **NEVER** add or retain a regression test solely to prove deleted implementation remains deleted; test an enduring observable contract instead.
- Treat narrow regression tests as temporary evidence unless they protect durable observable behaviour; fold durable intent into the nearest broader scenario.
- **ALWAYS** name test functions and classes for the behaviour and expected outcome.
- Group related assertions into the smallest coherent scenario; add variants only for distinct contracts or boundaries.
- **ALWAYS** assert through a public output, persisted state, emitted event, or forbidden side effect.
- **NEVER** use private calls, exact source text, or one discovered value as the sole oracle.
- **NEVER** pin incidental ordering, private error wording, or overspecified mock call counts unless they are public contracts.
- If inputs have distinct accepted, rejected, or boundary classes, **ALWAYS** cover each class.
- **ALWAYS** place an exception assertion around only the operation expected to fail.
- If a failure is logged, **ALWAYS** assert that the failure also reaches the caller or an observable failure channel.
- If asynchronous work is created, **ALWAYS** assert completion and failure observation.
- If time or randomness affects behaviour, **ALWAYS** control the clock, seed, or input sequence.
- **ALWAYS** keep synthetic fixtures inside tests and state the behaviour each fixture activates.
- Create a shared fixture or test helper only when multiple retained tests benefit or it removes meaningful duplication.
- **NEVER** let a fast test call a network service.
- **ALWAYS** place test doubles at external boundaries; **NEVER** replace the behaviour under test with a double.
- **ALWAYS** verify a slow journey through a state change in the real available services.
- **NEVER** accept service health alone as a journey oracle.
- If a slow prerequisite is missing, **ALWAYS** fail with the missing prerequisite; **NEVER** skip or report success.
- **NEVER** skip, loosen, or bypass a failing test or gate to complete a change.
- Run the narrowest affected test command first, then the broader repository gate required for that surface.
- **ALWAYS** clean up only resources created by the test run.
- After deleting tests, **ALWAYS** remove unreachable fixtures, helpers, mocks, and test data.
- For forecast behaviour, **ALWAYS** test forecast cut-offs, complete-race partitions, untouched holdouts, failed-evaluation non-publication, lineage, and preservation of operator changes.
- **NEVER** claim extraction, training, approval, or Nexus publication until a test exercises that real stage.
- For bounded static policy, **ALWAYS** test supported rejection cases and permitted behaviour.
