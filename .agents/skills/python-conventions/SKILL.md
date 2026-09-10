---
name: "python-conventions"
description: "Use when writing or refactoring Python code to select names, object types, and dependency boundaries."
---

# Guidance

## Names

- Use precise domain names over generic names such as `manager`, `helper`, `utils`, `data`, `thing`, or `processor`.
- Name functions and methods by the action or question they perform.
- Name classes by the role or concept they model, not by implementation mechanics.
- Name protocols by the capability they require.
- Name modules and packages after cohesive responsibilities, not mixed tool buckets.

## Object choice and boundaries

- Start with a function for stateless behavior.
- Use a class when state and behavior belong together, lifecycle matters, or polymorphism is needed.
- Use a dataclass for structured data carriers with annotated fields.
- Use a Protocol for structural contracts across implementations.
- Use an Enum for a closed symbolic set.
- Keep domain calculations independent of filesystem, environment, database and AWS clients. Put those effects in adapters with typed inputs and outputs.
- The effect checker rejects configured known direct calls and import aliases; it does not track object aliases, dataflow or dynamic dispatch. Keep all effectful IO in adapters even when the checker cannot identify the call.
- Validate untyped external input at ingress before it enters core types. A cast is a type-checker assertion, not parsing or runtime validation; do not use one to obtain typed core data from `Any`.
- Preserve specific exception causes and propagate failure explicitly. Logging an exception alone does not turn a failed operation into a successful outcome.
- Await result-bearing asynchronous work or give each task explicit lifecycle ownership and failure observation. Assigning a task to a discarded name does not establish ownership.
- Refactor complexity by separating responsibilities. Do not split expressions into meaningless forwarding functions solely to satisfy a gate.
- Avoid nested scans when keyed lookup or a clearly named transformation expresses the same operation. Preserve ordering and duplicate semantics explicitly.
- Keep dependency direction one-way: domain contracts must not import orchestration or infrastructure adapters.
- Treat whole-package cycle checks as an additional invariant, not a replacement for the repository's allowed-layer hierarchy.
- Follow the repository's executable policy for limits and lint settings; do not introduce local suppressions or parallel thresholds.
