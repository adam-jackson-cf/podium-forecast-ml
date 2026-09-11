---
name: "python-conventions"
description: "Use when writing or refactoring Python code to guide naming, package structure, object choice, and runtime behavior."
---

# Guidance
Complements Ruff's enabled [`pep8-naming` (`N`) rules](https://docs.astral.sh/ruff/rules/#pep8-naming-n) and repository AST checks; it does not replace deterministic linting.

## Names

- **ALWAYS** choose precise domain terms that state what a name owns, represents, does, or answers.
- **ALWAYS** name a function or method for the action it performs or the question it answers.
- **ALWAYS** name a class for the role or concept it models, not its implementation mechanics.
- **ALWAYS** name a protocol for the capability it requires.

## Package structure

- **ALWAYS** group folders by responsibility and import boundary, not incidental file type.
- **ALWAYS** give each module or package one cohesive responsibility.
- Add a package only when it owns a stable concept, API boundary, or workflow slice.
- **NEVER** create a catch-all directory unless the repository already defines that specific convention.

## Object choice

- For stateless behavior, **ALWAYS** start with a function.
- Use a class when state and behavior share a lifecycle or implementations require polymorphism.
- Use a dataclass for a structured data carrier with annotated fields.
- Use a `Protocol` when callers require structural typing across implementations.
- Use an `Enum` when values form a closed symbolic set.
- **NEVER** create a god class that centralizes unrelated workflows.

## Python behaviour

- **NEVER** convert `Any` into a core type with `cast`; validate the runtime value at ingress.
- **ALWAYS** preserve the original exception as the cause when translating failures.
- **NEVER** treat logging an exception as successful completion.
- **ALWAYS** await result-bearing asynchronous work or retain an owner that observes completion and failure.
- **NEVER** add forwarding functions only to reduce a complexity score.
- If keyed lookup replaces a nested scan, **ALWAYS** preserve ordering and duplicate semantics.
- **NEVER** add local lint suppressions or local copies of repository thresholds.
