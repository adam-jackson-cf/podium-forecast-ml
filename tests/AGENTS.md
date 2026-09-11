# Test instructions

- **ALWAYS** place fast behavioural tests under `tests/unit` or `tests/integration`.
- **ALWAYS** place the real-service journey under `tests/seams` and invoke it through `scripts/slow-seam.sh`.
- If a real pipeline stage is added, **ALWAYS** extend the existing slow journey; **NEVER** add a parallel smoke entrypoint.
